from django.urls import path
from .views import MyTokenObtainPairView, TestView, ListServiceView, ListSubserviceView

from users.views import SignupAPIView, ChangeUserPasswordView, ForgetPasswordView, ResetPasswordView, \
    DeactivateAccountView, UpdateContactDetailsView
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('auth/signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', SignupAPIView.as_view(), name='create_user'),
    path('auth/change_password/', ChangeUserPasswordView.as_view(), name='change_password'),
    path('auth/deactivate_account', DeactivateAccountView.as_view(), name='deactivate_account'),
    path('request/forget_password', ForgetPasswordView.as_view(), name='forget_password'),
    path('request/reset_password/<uid>/<token>/', ResetPasswordView.as_view(), name='rest_password'),
    path('request/update/contact_details/', UpdateContactDetailsView.as_view(), name="update_contact_details"),

    path('test/', TestView.as_view(), name='just_for_auth_testing'),

    path('services/all', ListServiceView.as_view(), name='all_services'),
    path('services/sub_services/all', ListSubserviceView.as_view(), name='all_sub_services'),
]
