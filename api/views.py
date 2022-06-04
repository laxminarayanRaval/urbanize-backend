from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from users.models import Service, SubService
from users.serializers import ServiceListSerializer, SubserviceListSerializer, ChangeUserPasswordSerializer, \
    ForgetPasswordSerializer


class TestView(APIView):
    permission_classes = (IsAuthenticated,)  # for protected routes

    def get(self, request):
        return Response(data={"Test": "Done"}, status=status.HTTP_200_OK)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['role'] = user.role
        token['pic_url'] = str(user.profile_pic_url)
        token['verified'] = user.is_verified
        # token['last_login'] = user.last_login
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ListServiceView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer


class ListSubserviceView(ListAPIView):
    """
    A View to List all Services & Subservices.
    """
    serializer_class = SubserviceListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return SubService.objects.all()


class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangeUserPasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    def post(self, request, format=None):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password Reset Link Send, please Check Your Email.'},
                            status=status.HTTP_200_OK)
        return Response({'error': 'Email Not Found, Please Check it or Signup instead.'},
                        status=status.HTTP_400_BAD_REQUEST)
