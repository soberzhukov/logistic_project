import uuid

from django.db import models
from django.utils import timezone

from payment.models import Budget, PaymentMethod
from users.models import User


class StatusOffer:
    DRAFT = 'draft'
    AWAITING_PAYMENT = 'await'
    BLOCKED = 'blocked'
    DELETED = 'deleted'
    MODERATION = 'moderation'
    PUBLISHED = 'published'


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

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='offers', on_delete=models.CASCADE, blank=True)
    name = models.CharField('Название Предложениеа', max_length=500)
    description = models.TextField('Описание', blank=True, null=True)
    status = models.CharField('Статус', max_length=300, choices=STATUS_CHOICES, blank=True, default=StatusOffer.DRAFT)
    payment_method = models.ForeignKey(PaymentMethod, models.SET_NULL, null=True, related_name='offers')
    execution_time = models.DateTimeField('Время исполнения', blank=True, null=True)
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    max_contracts = models.PositiveIntegerField('Максимальное количество заказчиков', default=0)

    budget = models.ForeignKey(Budget, models.SET_NULL, null=True, related_name='offers')
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)

    objects = OfferManager()

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
