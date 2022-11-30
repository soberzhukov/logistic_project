import uuid

from django.db import models


class CurrencyMethod:
    RUB = 'RUB'
    EUR = 'EUR'
    USD = 'USD'
    USDT = 'USDT'
    BTC = 'BTC'
    ETH = 'ETH'
    TON = 'TON'
    BNB = 'BNB'
    GBP = 'GBP'
    JPY = 'JPY'
    CNY = 'CNY'
    TRX = 'TRX'


class Budget(models.Model):
    """Бюджет"""
    CURRENCY_CHOICES = [
        (CurrencyMethod.RUB, 'Рубль'),
        (CurrencyMethod.EUR, 'Евро'),
        (CurrencyMethod.USD, 'Доллар'),
        (CurrencyMethod.USDT, 'Tether'),
        (CurrencyMethod.BTC, 'Биткойн'),
        (CurrencyMethod.ETH, 'Эфир'),
        (CurrencyMethod.TON, 'Тон'),
        (CurrencyMethod.BNB, 'Binance Coin'),
        (CurrencyMethod.GBP, 'Фунт стерлингов'),
        (CurrencyMethod.JPY, 'Японская иена'),
        (CurrencyMethod.CNY, 'Жэньминьби'),
        (CurrencyMethod.TRX, 'TRON'),
    ]
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    currency = models.CharField('Валюта', max_length=500, choices=CURRENCY_CHOICES, blank=True,
                                default=CurrencyMethod.RUB)
    count = models.DecimalField('Количество/цена??', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
