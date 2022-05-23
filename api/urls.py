from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('user/signup/', )
]
