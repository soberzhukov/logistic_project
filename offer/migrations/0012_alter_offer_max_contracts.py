# Generated by Django 4.0.4 on 2022-12-16 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0011_remove_offer_budget_remove_offer_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='max_contracts',
            field=models.PositiveIntegerField(default=5, verbose_name='Максимальное количество заказчиков'),
        ),
    ]
