import uuid

from django.db import models

from common.models import CommonObject, CommonElected
from payment.models import Budget, PaymentMethod
from users.models import User


class Offer(CommonObject):
    """Предложение"""

    author = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'


class ElectedOffer(CommonElected):
    """Избранное предложение"""
    offer = models.ForeignKey(Offer, related_name='rel_offer_elected', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.offer} - {self.user}'

    class Meta:
        verbose_name = 'Избранное предложение'
        verbose_name_plural = 'Избранные предложения'
