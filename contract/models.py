import uuid

from django.db import models
from rest_framework.exceptions import ValidationError

from offer.models import Offer
from order.models import Order
from payment.models import Budget
from users.models import User


class StatusContract:
    CREATED = 'created'
    REJECTED = 'rejected'
    INPROCESS = 'in_process'
    MODERATION = 'moderation'
    COMPLETED = 'completed'
    FORREVISION = 'for_revision'
    DISPUTE = 'dispute'


class Contract(models.Model):
    STATUS_CHOICES = [
        (StatusContract.CREATED, 'Создан (не подписан)'),
        (StatusContract.REJECTED, 'Отклонен'),
        (StatusContract.INPROCESS, 'На выполнении'),
        (StatusContract.MODERATION, 'На проверке'),
        (StatusContract.COMPLETED, 'Выполнен'),
        (StatusContract.FORREVISION, 'На доработку'),
        (StatusContract.DISPUTE, 'Открыт спор'),

    ]
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='contracts_order')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, blank=True, null=True, related_name='contracts_offer')
    amount = models.ForeignKey(Budget, models.SET_NULL, null=True, related_name='contracts')
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='contracts_executor', verbose_name='Исполнитель')
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='contracts_customer', verbose_name='Покупатель')
    status = models.CharField('Статус', max_length=300, choices=STATUS_CHOICES, blank=True,
                              default=StatusContract.CREATED)
    signature = models.BooleanField('Подтвержден?', default=False)
    condition = models.CharField('condition', max_length=500, null=True, blank=True)

    file = models.FileField('Прикрепленный файл', upload_to='uploads/contract_file/', null=True, blank=True)
    comment = models.CharField('Комментарий', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

    def save(self, *args, **kwargs):
        if not self.executor and not self.customer:
            raise ValidationError
        if not self.order and not self.offer:
            raise ValidationError
        super().save(*args, **kwargs)
