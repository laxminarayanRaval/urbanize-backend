import json

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password

from users.models import Service, SubService
from .models import User, ProfessionalUser, ContactUsQuery, ProfessionalUserService, Service, SubService, \
    HireProfessionalRequest

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Email
from api.utils import Util
from django.template.loader import get_template
from django.template import Context


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class SubserviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = '__all__'


class ContactusSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUsQuery
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, min_length=8, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # fields = ('full_name', 'email', 'password')
        # extra_kwargs = {'password': {'write_only': True}}
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already Registered."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'error': "Password fields don't match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Send Mail
        mail_template = 'emails/welcome_email.html'
        mail_sub = f"Congratulations {user.full_name}, Your Account is created successfully."
        mail_body = get_template(mail_template).render(
            {'user': user.full_name})
        data = {
            'mail_sub': mail_sub, 'mail_body': mail_body, 'to_email': user.email
        }
        Util.send_mail(data)
        return user


class ChangeUserPasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)
    password2 = serializers.CharField(max_length=255, required=True, write_only=True)

    class Meta:
        fields = ['oldpassword', 'password', 'password2']

    def validate(self, attrs):
        # print("-" * 10)
        oldpassword = attrs.get('oldpassword')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        user = User.objects.get(email=user)
        if not user.check_password(oldpassword):
            raise serializers.ValidationError("Old Password isn't correct. Fail to Update.")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match.")
        user.set_password(password)
        user.save()
        return attrs  # super().validate(attrs)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        # print("-------------------------------------", attrs)
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:3000/api/auth/reset_pass/{uid}/{token}/'
            print(f'Password Reset Link : {link}')
            # Send Mail
            mail_template = 'emails/send_verification_mail.html'
            mail_sub = f"Attention {user.full_name}!, You Requested Password Reset Link."
            mail_body = get_template(mail_template).render(
                {'user': user.full_name, 'link': link})
            data = {
                'mail_sub': mail_sub, 'mail_body': mail_body, 'to_email': user.email
            }
            Util.send_mail(data)
            return attrs
        else:
            raise serializers.ValidationError('Email Not Found as Registered.')


class ResetPasswordSerializer(serializers.Serializer):
    # uid =
    # token =
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            enc_uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            uid = smart_str(urlsafe_base64_decode(enc_uid))
            user = User.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or expired.")
            user.set_password()
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            # PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is Not valid or Expired.')


class DeactivateAccountSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=255, required=True, write_only=True)
    password = serializers.CharField(max_length=255, required=True, write_only=True)

    class Meta:
        fields = ['uid', 'password']

    def validate(self, attrs):
        """
        Validating if User Password is correct, make it's is_active field false.
        """
        uid = attrs.get('uid')
        password = attrs.get('password')
        user = User.objects.get(pk=uid)
        if not user.check_password(password):
            raise serializers.ValidationError("Given Password did not Matched with Actual one.")
        user.is_active = False
        user.save()
        return attrs


class UpdateUserContactDetailsSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)
    mobile = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields = ['email', 'mobile']

    def validate(self, attrs):
        # self.super()
        user = User.objects.get(email=self.context.get('user'))
        email = attrs.get('email')
        mobile = attrs.get('mobile')
        password = attrs.get('password')

        if not user.check_password(password):
            raise serializers.ValidationError('Password is not correct, Fail to update.')
        if not email == user.email and not user.mobile_no == mobile:
            raise serializers.ValidationError('Nothing to update.')

        user.email = email
        user.mobile_no = mobile
        user.save()

        # print(user.full_name, user.email, user.mobile_no)
        return attrs


class ProfessionalUserServiceSerializer(serializers.ModelSerializer):
    """
    A professional users listing as services provider.
    """

    class Meta:
        model = ProfessionalUserService
        fields = ['id', 'service_id', 'subservice_ids', 'prof_id', 'description', 'proof_img_url',
                  'charges', 'estimate_time', 'payment_modes', 'is_active', 'reviews_set']

    def create(self, validated_data):
        data = {**validated_data, "is_active": True}

        pu_service = ProfessionalUserService.objects.create(**data)
        user = self.context.get('user')
        user.role = 'prof'
        user.save()
        pu_service.save()
        return pu_service


class ProfessionalUserSerializer(serializers.ModelSerializer):
    # cities = serializers.CharField(max_length=255, required=True)
    startsTime = serializers.CharField(max_length=255, required=True)
    endsTime = serializers.CharField(max_length=255, required=True)
    professionaluserservice_set = ProfessionalUserServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ProfessionalUser
        # fields = '__all__'
        fields = ['id', 'cities', 'startsTime', 'endsTime', 'address', 'professionaluserservice_set', 'user_id',
                  'is_active']

    def validate(self, attrs):
        # cities = attrs.get('cities')
        startsTime = attrs.get('startsTime')
        endsTime = attrs.get('endsTime')
        # address = attrs.get('address')
        user = self.context.get('user')
        # print('*'*10, '\n\tuser', user, '\n\tattrs data', attrs)
        if user.role == 'prof':
            raise serializers.ValidationError("User is already a Professional")
        if startsTime == endsTime:
            raise serializers.ValidationError("You must select different end time than start time")

        print("validating :", startsTime, endsTime)
        return attrs

    def create(self, validated_data):
        user = self.context.get('user')
        # print('='*30, '\n\tuser', user, '\n\tvalidated data', validated_data)
        # cities = validated_data['cities'].split(',')
        # print("save  --> create :", validated_data, user.id, cities)
        # pu : professional user
        add_pu = {"user_id": user, **validated_data}
        print(add_pu)
        prof_user = ProfessionalUser.objects.create(**add_pu)
        # user.role = 'prof'  # no need to update here
        # user.save() #  this should be updated at service listing
        # prof_user.save()
        return prof_user


class HireProfessionalRequestSerializer(serializers.ModelSerializer):
    # prof_id = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = HireProfessionalRequest
        fields = '__all__'  # ['id', 'pus_id', 'sub_service_id', 'user_id', 'hire_date', 'descriptive_msg', 'status']

    def create(self, validated_data):
        print("\n validated_data:", validated_data)
        hpr = HireProfessionalRequest.objects.create(validated_data)
        print("\n hpr     ::::::: ", hpr)
        return hpr


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User's all details with nested if he is prof
    """

    # professionaluser_set = ProfessionalUserSerializer(many=True, read_only=True)
    # hireprofessionalrequest_set = HireProfessionalRequestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'email', 'role', 'full_name', 'date_of_birth', 'gender', 'profile_pic_url', 'is_verified',
                  'is_active', 'mobile_no', 'professionaluser_set']


class AllServiceListSerializer(serializers.ModelSerializer):
    subservice_set = SubserviceListSerializer(many=True, read_only=True)
    professionaluserservice_set = ProfessionalUserServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'service_name', 'description', 'img_url', 'is_active', 'subservice_set',
                  'professionaluserservice_set']
