from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import User


class SignupAPIView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    # serializer_class =
