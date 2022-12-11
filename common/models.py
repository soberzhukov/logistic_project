import uuid

from django.db import models
from django.utils import timezone

from payment.models import Budget, PaymentMethod


class CommonStatus:
    DRAFT = 'draft'
    AWAITING_PAYMENT = 'await'
    BLOCKED = 'blocked'
    DELETED = 'deleted'
    MODERATION = 'moderation'
    PUBLISHED = 'published'


class CommonManager(models.Manager):
    def all(self):
        return self.get_queryset().exclude(status='deleted')



class CommonObject(models.Model):
    """Абстрактная модель для Order и Offer"""
    STATUS_CHOICES = [
        (CommonStatus.DRAFT, 'Черновик'),
        (CommonStatus.AWAITING_PAYMENT, 'Ожидает оплаты'),
        (CommonStatus.BLOCKED, 'Заблокирован'),
        (CommonStatus.MODERATION, 'На модерации'),
        (CommonStatus.DELETED, 'Удален'),
        (CommonStatus.PUBLISHED, 'Опубликован'),
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название Предложениеа', max_length=500)
    description = models.TextField('Описание', blank=True, null=True)
    status = models.CharField('Статус', max_length=300, choices=STATUS_CHOICES, blank=True, default=CommonStatus.DRAFT)
    payment_method = models.ForeignKey(PaymentMethod, models.SET_NULL, null=True)
    execution_time = models.DateTimeField('Время исполнения', blank=True, null=True)
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    max_contracts = models.PositiveIntegerField('Максимальное количество заказчиков', default=0)

    budget = models.ForeignKey(Budget, models.SET_NULL, null=True)
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)

    objects = CommonManager()

    class Meta:
        abstract = True
