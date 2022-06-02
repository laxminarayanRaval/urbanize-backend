from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from users.models import Service, SubService
from .models import User


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
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields don't match"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user
