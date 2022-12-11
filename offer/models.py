import uuid

from django.db import models

from common.models import CommonObject
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


class ElectedOffer(models.Model):
    """Избранное предложение"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='rel_user_offer_elected', on_delete=models.CASCADE, blank=True)
    offer = models.ForeignKey(Offer, related_name='rel_offer_elected', on_delete=models.CASCADE)
    notes = models.TextField('Отзыв', blank=True, null=True)

    def __str__(self):
        return f'{self.offer} - {self.user}'

    class Meta:
        verbose_name = 'Избранное предложение'
        verbose_name_plural = 'Избранные предложения'
