from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
        # token['last_login'] = user.last_login
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ListServiceSubserviceView(ListAPIView):
    """
    A View to List all Services & Subservices.
    """
    pass
