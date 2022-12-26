import uuid

from django.db import models
from django.utils import timezone

from offer.models import Offer
from order.models import Order


class SelectionObject(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название подборки', max_length=500)

    sorting_number = models.PositiveSmallIntegerField('Сортировочный номер', blank=True, unique=True)
    date_created = models.DateTimeField('Время создания', blank=True, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['sorting_number']


class SelectionOrder(SelectionObject):
    orders = models.ManyToManyField(Order, related_name='selections_order', blank=True)

    class Meta:
        verbose_name = 'Подборка заказа'
        verbose_name_plural = 'Подборки заказов'


class SelectionOffer(SelectionObject):
    offers = models.ManyToManyField(Offer, related_name='selections_offer', blank=True)

    class Meta:
        verbose_name = 'Подборка предложения'
        verbose_name_plural = 'Подборки предложений'
