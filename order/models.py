import uuid

from django.db import models
from django.db.models import Count, F
from django.utils import timezone

from payment.models import Budget
from users.models import User


class StatusOrder:
    DRAFT = 'draft'
    AWAITING_PAYMENT = 'await'
    BLOCKED = 'blocked'
    DELETED = 'deleted'
    MODERATION = 'moderation'
    PUBLISHED = 'published'


class PaymentMethod:
    CARD = 'credit_card'


class OrderManager(models.Manager):
    def all(self):
        return self.get_queryset().exclude(status='deleted')

    def get_lt_max_contracts(self):
        return self.all().annotate(count_cs=Count('contracts_order')).filter(max_contracts__gt=F('count_cs'))


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        (StatusOrder.DRAFT, 'Черновик'),
        (StatusOrder.AWAITING_PAYMENT, 'Ожидает оплаты'),
        (StatusOrder.BLOCKED, 'Заблокирован'),
        (StatusOrder.MODERATION, 'На модерации'),
        (StatusOrder.DELETED, 'Удален'),
        (StatusOrder.PUBLISHED, 'Опубликован'),
    ]
    PAYMENT_METHOD_CHOICES = [
        (PaymentMethod.CARD, 'Кредитной картой'),
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, blank=True)
    name = models.CharField('Название заказа', max_length=500)
    description = models.TextField('Описание', blank=True, null=True)
    status = models.CharField('Статус', max_length=300, choices=STATUS_CHOICES, blank=True, default=StatusOrder.DRAFT)
    payment_method = models.CharField('Метод оплаты', max_length=300, choices=PAYMENT_METHOD_CHOICES, blank=True,
                                      default=PaymentMethod.CARD)
    execution_time = models.DateTimeField('Время исполнения', blank=True, null=True)
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    max_contracts = models.PositiveIntegerField('Максимальное количество исполнителей', default=0)

    budget = models.ForeignKey(Budget, models.SET_NULL, null=True, related_name='orders')
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)
    objects = OrderManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


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
