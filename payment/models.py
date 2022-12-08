import uuid

from django.db import models


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Валюта', max_length=300)
    short_title = models.CharField('Короткое назавание оплаты', max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Метод оплаты', max_length=300)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'


class Budget(models.Model):
    """Бюджет"""
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    currency = models.ForeignKey(Currency, models.SET_NULL, null=True, related_name='budgets')
    count = models.DecimalField('Количество/цена??', max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
