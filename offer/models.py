import uuid

from django.db import models
from django.utils import timezone

from payment.models import Budget
from users.models import User


class StatusOffer:
    DRAFT = 'draft'
    AWAITING_PAYMENT = 'await'
    BLOCKED = 'blocked'
    DELETED = 'deleted'
    MODERATION = 'moderation'
    PUBLISHED = 'published'


class PaymentMethod:
    CARD = 'credit_card'


class OfferManager(models.Manager):
    def all(self):
        return self.get_queryset().exclude(status='deleted')


class Offer(models.Model):
    """Предложение"""
    STATUS_CHOICES = [
        (StatusOffer.DRAFT, 'Черновик'),
        (StatusOffer.AWAITING_PAYMENT, 'Ожидает оплаты'),
        (StatusOffer.BLOCKED, 'Заблокирован'),
        (StatusOffer.MODERATION, 'На модерации'),
        (StatusOffer.DELETED, 'Удален'),
        (StatusOffer.PUBLISHED, 'Опубликован'),
    ]
    PAYMENT_METHOD_CHOICES = [
        (PaymentMethod.CARD, 'Кредитной картой'),
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE, blank=True)
    name = models.CharField('Название Предложениеа', max_length=500)
    description = models.TextField('Описание', blank=True, null=True)
    status = models.CharField('Статус', max_length=300, choices=STATUS_CHOICES, blank=True, default=StatusOffer.DRAFT)
    payment_method = models.CharField('Метод оплаты', max_length=300, choices=PAYMENT_METHOD_CHOICES, blank=True,
                                      default=PaymentMethod.CARD)
    execution_time = models.DateTimeField('Время исполнения', blank=True, null=True)
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    max_contracts = models.PositiveIntegerField('Максимальное количество заказчиков', default=0)

    budget = models.ForeignKey(Budget, models.SET_NULL, null=True, related_name='offers')
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
