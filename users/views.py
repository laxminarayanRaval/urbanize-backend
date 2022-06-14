from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import SignupSerializer, ChangeUserPasswordSerializer, ForgetPasswordSerializer, \
    ResetPasswordSerializer, DeactivateAccountSerializer, UpdateContactDetailsSerializer, ProfessionalUserSerializer
from .models import User, ProfessionalUser


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


class ContactDetailsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        serializer = UpdateContactDetailsSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'message': 'Contact Details Updated'}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = User.objects.get(email=request.user)
        return Response({'message': {'email': user.email, 'mobile': user.mobile_no}}, status=status.HTTP_200_OK)


class ProfessionalUserView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    # serializer_class = ProfessionalUserSerializer

    def post(self, request):
        serializer = ProfessionalUserSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'congratulations you\'ve completed on step for being a Professional'},
                            status=status.HTTP_202_ACCEPTED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, uid=''):
        if uid != '':
            user = User.objects.get(pk=uid)
        else:
            user = User.objects.get(email=request.user)
            if user.role != 'prof': return Response({'message': 'This user is not a Professional'})
        if user:
            if user.role == 'user':
                return Response({'message': f'This user {user.full_name} ({user.email}) is not a Professional'})
        else:
            return Response({'message': 'User Not Found'}, status=status.HTTP_204_NO_CONTENT)
