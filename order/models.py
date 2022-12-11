import uuid

from django.db import models
from django.utils import timezone

from common.models import CommonObject
from payment.models import Budget, PaymentMethod
from users.models import User


class Order(CommonObject):
    """Заказ"""

    author = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ElectedOrder(models.Model):
    """Избранный заказ"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='rel_user_order_elected', on_delete=models.CASCADE, blank=True)
    order = models.ForeignKey(Order, related_name='rel_order_elected', on_delete=models.CASCADE)
    notes = models.TextField('Отзыв', blank=True, null=True)

    def __str__(self):
        return f'{self.order} - {self.user}'

    class Meta:
        verbose_name = 'Избранный заказ'
        verbose_name_plural = 'Избранные заказы'


class TypeSearch:
    ORDER = 'order'
    OFFER = 'offer'


class SavedSearch(models.Model):
    """Сохранненный поиск"""
    TYPE_CHOICES = [
        (TypeSearch.ORDER, 'Поиск по заказам'),
        (TypeSearch.OFFER, 'Поиск по предложениям'),
    ]
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='rel_savedsearch', on_delete=models.CASCADE, blank=True)
    body_params = models.JSONField('Параметры поиска из body', default=dict)
    date_create = models.DateTimeField('Время создания', blank=True, default=timezone.now)
    type_search = models.CharField('Тип поиска', max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.author} - {self.type_search}'

    class Meta:
        verbose_name = 'Сохраненный поиск'
        verbose_name_plural = 'Сохраненные поиски'
