from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileAPIView, SetPhoneNumberAPIView, PhoneNumberActivateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('info/', UserProfileAPIView.as_view(), name='user-info'),
    path('set_phone/', SetPhoneNumberAPIView.as_view(), name="set_user_phone_number"),
    path('activate_phone/', PhoneNumberActivateAPIView.as_view(), name="activate_user_phone_number"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]