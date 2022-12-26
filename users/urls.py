from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import PasswordConfirmAPIView, ResetPasswordView
from . import views

urlpatterns = [
    path('sign-up/', views.RegistrationAPIView.as_view(), name='sing_up'),
    path('sign-in/', views.LoginAPIVIew.as_view(), name='sing_in'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('confirm/create/', views.CreatePhoneConfirmAPIView.as_view(), name='create_confirm_phone'),
    path('confirm/confirmed/', views.PhoneConfirmAPIView.as_view(), name='confirm_phone'),
    path('confirm_pass/create/', views.CreatePasswordConfirmAPIView.as_view(), name='create_confirm_password'),
    path('confirm_pass/confirmed/', PasswordConfirmAPIView.as_view(), name='confirm_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    # path('cities/', views.GetCitiesAPIView.as_view(), name='get_cities'),
    path('countries/', views.GetCountriesAPIView.as_view(), name='get_countries'),
    path('user_info/', views.UserInfoAPIView.as_view(), name='user_info'),
    path('user_info/update/', views.UserInfoUpdateAPIView.as_view(), name='user_info_update'),
    path('user_info/passport/', views.PassportAPIView.as_view(), name='passport')
]
