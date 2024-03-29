from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, BasePermission
from rest_framework.response import Response
from .serializers import SignupSerializer, ContactusSerializers, ChangeUserPasswordSerializer, ForgetPasswordSerializer, \
    ResetPasswordSerializer, DeactivateAccountSerializer, UpdateUserContactDetailsSerializer, \
    ProfessionalUserSerializer, UserDetailsSerializer, ProfessionalUserServiceSerializer, \
    UserRequirementSerializer, FlaggedProfessionalUserReportSerializer, FavouriteUserSerializer
# HireProfessionalRequestSerializer
from .models import User, ContactUsQuery, ProfessionalUser, ProfessionalUserService, FlaggedProfessionalUserReport, \
    UserRequirement, FavouriteUser
# HireProfessionalRequest


class SignupAPIView(CreateAPIView):
    """
    User Signup process handling View.
    """

    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class WriteOnly(BasePermission):
    """
    A WriteOnly Custom Permission for only POST method call check.
    """

    def has_permission(self, request, view):
        return request.method == 'POST'


class ContactusView(APIView):
    """
    A View for Handling strange users contact queries. Only Admin can Read, Update or Delete.
    """
    permission_classes = [IsAdminUser | WriteOnly, ]

    def get_object(self, pk):
        """to get parameter specific data"""
        try:
            return ContactUsQuery.objects.get(pk=pk)
        except ContactUsQuery.DoesNotExist:
            raise ValueError('Data Not Found')

    def get(self, request, pk=None, format=None):
        """only Admin can Read"""
        if pk:
            qs = self.get_object(pk)
            serializer = ContactusSerializers(qs)
        else:
            qs = ContactUsQuery.objects.all()
            serializer = ContactusSerializers(qs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Random Person can make contact query."""
        serializer = ContactusSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    # def put(self, request):
    #     """Admin will mark query solved"""
    #     serializer = ContactusSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     return Response()


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


class UserDetailsView(ListAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request, uid=None):
        if uid:
            user = User.objects.get(pk=uid)
        else:
            user = request.user
        if user:
            serializer = UserDetailsSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Please Provide User ID.'})


class ContactDetailsView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        serializer = UpdateUserContactDetailsSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'message': 'Contact Details Updated'}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = User.objects.get(email=request.user)
        return Response({'message': {'email': user.email, 'mobile': user.mobile_no}}, status=status.HTTP_200_OK)


class ProfessionalUserView(APIView):
    """
    User to Professional, role change
    """
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    # serializer_class = ProfessionalUserSerializer

    def post(self, request):
        # print('_'*30, '\n\trequest.user', request.user, '\n\trequest.data', {**request.data})

        serializer = ProfessionalUserSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'congratulations you\'ve completed on step for being a Professional'},
                            status=status.HTTP_202_ACCEPTED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, uid=None):
        if uid:
            profuser = ProfessionalUser.objects.get(pk=uid)
            serializer = ProfessionalUserSerializer(profuser)
            return Response(serializer.data)
        else:
            return Response({'message': 'Please Provide Professional Id'}, status=status.HTTP_404_NOT_FOUND)


class ProfessionalUserServiceView(APIView):
    """
    Professional users services listing
    """
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request):
        """A public API for services_listings"""
        pu_services_list = ProfessionalUserService.objects.all()
        serializer = ProfessionalUserServiceSerializer(pu_services_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProfessionalUserServiceSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Congratulation your service is listed'}, status=status.HTTP_202_ACCEPTED)


# class HireProfessionalRequestView(APIView):
#     """
#     Hiring Professional by User
#     """
#     permission_classes = [IsAuthenticated]

    # serializer_class = HireProfessionalRequestSerializer

    # def get(self, request):
    #     """All Professional Requests send or received"""
    #     user = request.user
    #     if user.role == 'prof':
    #         received = HireProfessionalRequest.objects.get()

    # def post(self, request):
    #     data = {**request.data, "user_id": request.user.id}
    #     print("Post data:", data)
        # serializer = HireProfessionalRequestSerializer(data=data)
        # if serializer.is_valid():
        #     print("Serializer After valid:", serializer)
        #     serializer.save()
        #     print("Data After Saving:", serializer.data)
        #     return Response({'message': f'Hiring request is Sent to the Professional {request.user.full_name}'},
        #                     status=status.HTTP_202_ACCEPTED)
        # return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserRequirementViewSet(ModelViewSet):
    serializer_class = UserRequirementSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserRequirement.objects.all()


class FlaggedProfessionalUserReportViewSet(ModelViewSet):
    serializer_class = FlaggedProfessionalUserReportSerializer
    permission_classes = [IsAuthenticated]
    queryset = FlaggedProfessionalUserReport.objects.all()


class FavouriteUserViewSet(ModelViewSet):
    serializer_class = FavouriteUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = FavouriteUser.objects.all()
