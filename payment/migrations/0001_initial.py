# Generated by Django 4.0.4 on 2022-11-15 06:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('currency', models.CharField(blank=True, choices=[('RUB', 'Рубль'), ('EUR', 'Евро'), ('USD', 'Доллар'), ('USDT', 'Tether'), ('BTC', 'Биткойн'), ('ETH', 'Эфир'), ('TON', 'Тон'), ('BNB', 'Binance Coin'), ('GBP', 'Фунт стерлингов'), ('JPY', 'Японская иена'), ('CNY', 'Жэньминьби'), ('TRX', 'TRON')], default='RUB', max_length=500, verbose_name='Валюта')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Бюджет',
                'verbose_name_plural': 'Бюджеты',
            },
        ),
    ]
