from django.urls import path, include
from .views import MyTokenObtainPairView, TestView, ListServiceView, ListSubserviceView, AllServicesListView
from rest_framework.routers import DefaultRouter
from users.views import SignupAPIView, ContactusView, ChangeUserPasswordView, ForgetPasswordView, ResetPasswordView, \
    DeactivateAccountView, UserDetailsView, ContactDetailsView, ProfessionalUserView, ProfessionalUserServiceView, \
    UserRequirementViewSet, FlaggedProfessionalUserReportViewSet, FavouriteUserViewSet  # HireProfessionalRequestView
from rest_framework_simplejwt.views import (TokenRefreshView)

router = DefaultRouter()
router.register('user/requirement', UserRequirementViewSet)
router.register('flag/professional', FlaggedProfessionalUserReportViewSet)
router.register('fav/professional', FavouriteUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contact_us/', ContactusView.as_view(), name='contact_us'),
    path('contact_us/<pk>/', ContactusView.as_view(), name='contact_us_id'),

    path('auth/signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', SignupAPIView.as_view(), name='create_user'),
    path('auth/change_password/', ChangeUserPasswordView.as_view(), name='change_password'),
    path('auth/deactivate_account', DeactivateAccountView.as_view(), name='deactivate_account'),
    path('request/forget_password', ForgetPasswordView.as_view(), name='forget_password'),
    path('request/reset_password/<uid>/<token>/', ResetPasswordView.as_view(), name='rest_password'),

    path('user/details/', UserDetailsView.as_view(), name="current_user_details"),
    path('user/details/<uid>/', UserDetailsView.as_view(), name="id_user_details"),
    path('user/contact_details/', ContactDetailsView.as_view(), name="contact_details"),

    path('user/professional/', ProfessionalUserView.as_view(), name="professional_user"),
    path('user/professional/<uid>/', ProfessionalUserView.as_view(), name="professional_user_via_id"),
    path('professional/services_list/', ProfessionalUserServiceView.as_view(), name="professional_user_listings"),

    # path('flag/professional/', FlaggedProfessionalUserReportView.as_view({'get': 'list'}),
    #      name="flag_professional_user"),

    # path('hire/professional/', HireProfessionalRequestView.as_view(), name="user_professional_hiring"),

    path('test/', TestView.as_view(), name='just_for_auth_testing'),

    path('services/all', ListServiceView.as_view(), name='all_services'),
    path('services/sub_services/all', ListSubserviceView.as_view(), name='all_sub_services'),
    path('services/list_all/', AllServicesListView.as_view(), name='services_with_nested'),
]

# urlpatterns += router.urls
