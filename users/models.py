import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from cities_light.models import City, Country



class User(AbstractUser):
    """Модель юзера"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField('Username', max_length=20, unique=True, null=True)
    first_name = models.CharField('Имя', max_length=500, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=500, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=500, blank=True, null=True)
    # email = models.CharField('Электронная почта', max_length=500, blank=True, null=True)
    push_token = models.CharField('Токен Firebase', max_length=200, blank=True)
    is_blocked = models.BooleanField('Заблокирован', blank=True, default=False)
    cause_blocked = models.TextField('Причина блокировки', blank=True, null=True)
    is_admin = models.BooleanField('Администратор для обслуживания устройства', blank=True, default=False)
    push_off = models.BooleanField('Отключение необязательных push уведомлений', blank=True, default=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Страна')
    is_verified = models.BooleanField('Верифицирован?', default=False)
    avatar = models.ForeignKey('common.Image', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Аватар')
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class BaseConfirm(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    code = models.CharField('Код подтверждения', max_length=6, blank=False)
    is_confirmed = models.BooleanField('Подтвержденный аккаунт', blank=True, default=False)
    expired_time = models.DateTimeField('Дата окончания действия', null=True)
    date_created = models.DateTimeField('Дата создания', default=timezone.now, blank=True)

    class Meta:
        abstract = True


class ConfirmPhone(BaseConfirm):
    phone = models.CharField('Номер телефона', max_length=20, blank=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Подтвержение аккаунта'
        verbose_name_plural = 'Подтвержение аккаунта'
        ordering = ['date_created']


class ConfirmPassword(BaseConfirm):
    phone = models.CharField('Номер телефона', max_length=20, blank=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Подтвержение пароля'
        verbose_name_plural = 'Подтвержение пароля'
        ordering = ['expired_time']


class PassportFiles(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.OneToOneField(User, related_name='passports_files', on_delete=models.CASCADE, blank=True)
    main_page = models.ForeignKey('common.Image', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Главная страница паспорта', related_name='passport_main_page')
    registration_page  = models.ForeignKey('common.Image', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Страница прописки', related_name='passport_registration_page')
    selfie_with_passport = models.ForeignKey('common.Image', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Селви с папортом', related_name='passport_selfie_with_passport')
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Файлы паспорта'
        verbose_name_plural = 'Файлы паспорта'
