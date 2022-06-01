from django.urls import path
from .views import MyTokenObtainPairView, TestView
from users.views import SignupAPIView
from .views import ListServiceView, ListSubserviceView
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('auth/signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', SignupAPIView.as_view(), name='create_user'),
    path('test/', TestView.as_view(), name='just_for_auth_testing'),

    path('services/all', ListServiceView.as_view(), name='all_services'),
    path('services/sub_services/all', ListSubserviceView.as_view(), name='all_sub_services'),
]
