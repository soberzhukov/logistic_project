import uuid

from django.db import models
from django.utils import timezone

from payment.models import Budget, PaymentMethod
from users.models import User


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

    execution_time = models.DateTimeField('Время исполнения', blank=True, null=True)
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    max_contracts = models.PositiveIntegerField('Максимальное количество заказчиков', default=5)
    payment_methods = models.ManyToManyField(PaymentMethod)
    budgets = models.ManyToManyField(Budget)
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)

    objects = CommonManager()

    class Meta:
        abstract = True


class CommonElected(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    notes = models.TextField('Отзыв', blank=True, null=True)

    class Meta:
        abstract = True


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


class File(models.Model):
    """Файлы"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    file = models.FileField('Файл', upload_to='uploads/files/')
    date_created = models.DateTimeField('Дата создания', blank=True, default=timezone.now)
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
