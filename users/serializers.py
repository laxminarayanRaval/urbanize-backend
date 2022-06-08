from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password

from users.models import Service, SubService
from .models import User

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


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class SubserviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
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
