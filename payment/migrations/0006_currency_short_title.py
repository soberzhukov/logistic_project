# Generated by Django 4.0.4 on 2022-12-08 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_budget_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='short_title',
            field=models.CharField(default='1', max_length=300, verbose_name='Короткое назавание оплаты'),
            preserve_default=False,
        ),
    ]
