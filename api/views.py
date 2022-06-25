from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from users.models import Service, SubService
from users.serializers import ServiceSerializer, SubserviceListSerializer, AllServiceListSerializer


class TestView(APIView):
    """
    A Test View for testing Authentication is working.
    """
    permission_classes = [IsAuthenticated, ]  # for protected routes

    def get(self, request):
        return Response(data={"Test": "Done"}, status=status.HTTP_200_OK)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT claims
    """

    @classmethod
    def get_token(cls, user):
        """
        Token Generation process
        """
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email
        # token['mobile'] = str(user.mobile_no)
        # token['gender'] = str(user.gender)
        # token['role'] = user.role
        # token['pic_url'] = str(user.profile_pic_url)
        # token['verified'] = user.is_verified
        # token['last_login'] = user.last_login
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    A View made for Custom claiming in JWT Token
    """
    serializer_class = MyTokenObtainPairSerializer


class ListServiceView(ListAPIView):
    """
    A View to List Only Services
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ListSubserviceView(ListAPIView):
    """
    A View to List all Services & Subservices.
    """
    serializer_class = SubserviceListSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return SubService.objects.all()


class AllServicesListView(ListAPIView):
    """
    A View to List Both Services & SubServices
    """
    queryset = Service.objects.all()
    serializer_class = AllServiceListSerializer
    permission_classes = [AllowAny, ]
