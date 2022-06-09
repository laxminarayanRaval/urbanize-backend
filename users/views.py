from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import SignupSerializer, ChangeUserPasswordSerializer, ForgetPasswordSerializer, \
    ResetPasswordSerializer, DeactivateAccountSerializer, UpdateContactDetailsSerializer


class SignupAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class ChangeUserPasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        serializer = ChangeUserPasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'message': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = ForgetPasswordSerializer(data=request.data)
        # print("===================", request, request.data)
        if serializer.is_valid():
            return Response({'message': 'Password Reset Link Send, please Check Your Email.'},
                            status=status.HTTP_200_OK)
        return Response({'message': 'Email Not Found, Please Check it or Signup instead.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        print(request.data, uid, token)
        serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            return Response({"message": 'Password Reset Successful.'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = DeactivateAccountSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Your Account is Deactivated."}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpdateContactDetailsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        serializer = UpdateContactDetailsSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'message': 'Contact Details Updated'}, status=status.HTTP_200_OK)
        return Response({'message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
