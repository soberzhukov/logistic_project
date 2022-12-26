import datetime

import pytz
from cities_light.models import Country
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from logisticproject.exceptions import BadeRequestException, ForbiddenException, AccessException
from logisticproject.responses import AccessResponse
from users import schema
from users.models import ConfirmPhone, User, ConfirmPassword, PassportFiles
from users.permissions import IsOwner, IsPassportOwner
from users.serializers import CreateConfirmPhoneSerializer, ConfirmPhoneSerializer, RegistrationSerializer, \
    CustomTokenObtainPairSerializer, CreateConfirmPasswordSerializer, ConfirmPasswordSerializer, \
    ResetPasswordSerializer, UserInfoSerializer, CountryLightSerializer, PassportFilesSerializer
from users.tasks import send_code_for_confirm_phone, send_code_for_confirm_password


class CreatePhoneConfirmAPIView(CreateAPIView):
    """
    Создание модели подтверждение телефона
    """
    serializer_class = CreateConfirmPhoneSerializer
    queryset = ConfirmPhone.objects.all()
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        phone = serializer.validated_data.get('phone')
        send_code_for_confirm_phone.delay(phone)


class PhoneConfirmAPIView(GenericAPIView):
    """
    Подтверждение пользователя

    По коду из смс
    """
    serializer_class = ConfirmPhoneSerializer
    queryset = ConfirmPhone.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_object(self, serializer):
        phone = self._validate_phone(serializer.validated_data.get('phone'))
        instance = self.queryset.filter(phone=phone).last()
        if not instance:
            raise BadeRequestException(message='Not found phone number', code='not_phone')
        if instance.code != serializer.data['code']:
            raise BadeRequestException(message='Wrong code', code='wrong_code')
        return instance

    def _validate_phone(self, phone):
        return PhoneNumber.from_string(phone_number=phone, region='RU').as_e164

    def _confirmed(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object(serializer)
        if instance.is_confirmed:
            raise AccessException(message='Код уже подтвержден', code='confirmed')
        instance.is_confirmed = True
        instance.save()

    def post(self, request):
        self._confirmed(request)
        return AccessResponse()


class RegistrationAPIView(CreateAPIView):
    """
    Регистрация пользователя

    Регистрация по номеру телефона и паролю
    """
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    @swagger_auto_schema(responses=schema.RegistrationSchema.response)
    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def perform_create(self, serializer):
        self._is_confirmed_phone(serializer)
        return super().perform_create(serializer)

    def _is_confirmed_phone(self, serializer):
        phone = serializer.validated_data.get('username')
        confirm_phone = ConfirmPhone.objects.filter(phone=phone).last()
        if not confirm_phone:
            raise ForbiddenException(message='Phone not verified', code='not_verified')

        if not confirm_phone.is_confirmed:
            raise ForbiddenException(message='Phone not verified', code='not_verified')


class LoginAPIVIew(TokenObtainPairView):
    """
    Авторизация пользователя

    После авторизации выдается access и refresh токен
    """
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(responses=schema.LoginSchema.response)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreatePasswordConfirmAPIView(CreateAPIView):
    """
    Создание модели подтверждение пароля
    """
    serializer_class = CreateConfirmPasswordSerializer
    queryset = ConfirmPassword.objects.all()
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        phone = serializer.validated_data.get('phone')
        send_code_for_confirm_password.delay(phone)


class PasswordConfirmAPIView(GenericAPIView):
    """
    Подтверждение пользователя

    По коду из смс
    """
    serializer_class = ConfirmPasswordSerializer
    queryset = ConfirmPassword.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_object(self, serializer):
        phone = self._validate_phone(serializer.validated_data.get('phone'))

        instance = self.queryset.filter(phone=phone).last()
        if not instance:
            raise BadeRequestException(message='Not found phone number', code='not_phone')
        if instance.expired_time < timezone.now():
            raise BadeRequestException(message='Expired time', code='expired_time')
        if instance.code != serializer.data['code']:
            raise BadeRequestException(message='Wrong code', code='wrong_code')
        return instance

    def _validate_phone(self, phone):
        return PhoneNumber.from_string(phone_number=phone, region='RU').as_e164

    def _confirmed(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object(serializer)
        if instance.is_confirmed:
            raise AccessException(message='Код уже подтвержден', code='confirmed')
        instance.is_confirmed = True
        instance.save()

    def post(self, request):
        self._confirmed(request)
        return AccessResponse()


class ResetPasswordView(APIView):
    """
    Смена пароля
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password1 = serializer.data['password1']
        valid_phone = PhoneNumber.from_string(phone_number=username, region='RU').as_e164
        try:
            user = User.objects.get(username=valid_phone)
        except User.DoesNotExist:
            return Response(data={'username': 'Not found'}, status=HTTP_400_BAD_REQUEST)

        confirm_reset_password = ConfirmPassword.objects.filter(phone=valid_phone).last()
        # проверяем подтверждена ли смена пароля
        if confirm_reset_password and confirm_reset_password.is_confirmed:
            # Если код подтвержден больше 5 часов назад
            if confirm_reset_password.expired_time < datetime.datetime.now(pytz.utc) - datetime.timedelta(hours=5):
                return Response(data={'password': 'expired time'}, status=HTTP_400_BAD_REQUEST)
            user.set_password(password1)
            user.save()
            return Response(data={'message': 'ok'}, status=HTTP_200_OK)
        else:
            return Response(data={'password': 'not confirmed'}, status=HTTP_400_BAD_REQUEST)


# class GetCitiesAPIView(ListAPIView):
#     """Получение списка городов"""
#     serializer_class = CitiesLightSerializer
#     queryset = City.objects.all()
#     permission_classes = [permissions.AllowAny]

class GetCountriesAPIView(ListAPIView):
    """Получение списка городов"""
    serializer_class = CountryLightSerializer
    queryset = Country.objects.all().order_by('id')
    permission_classes = [permissions.AllowAny]


class UserInfoAPIView(RetrieveAPIView):
    serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_object(self):
        return self.request.user


class UserInfoUpdateAPIView(UpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_object(self):
        return self.request.user


class PassportAPIView(CreateAPIView,
                      RetrieveAPIView,
                      UpdateAPIView):
    queryset = PassportFiles.objects.all()
    serializer_class = PassportFilesSerializer
    permission_classes = (IsPassportOwner,)

    def get_object(self):
        return get_object_or_404(self.queryset, **{'author': self.request.user})
