from django.db import models

from common.models import CommonObject, CommonElected
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


class ElectedOrder(CommonElected):
    """Избранный заказ"""
    order = models.ForeignKey(Order, related_name='rel_order_elected', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} - {self.user}'

    class Meta:
        verbose_name = 'Избранный заказ'
        verbose_name_plural = 'Избранные заказы'
