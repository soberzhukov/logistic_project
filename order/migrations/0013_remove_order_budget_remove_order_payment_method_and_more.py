# Generated by Django 4.0.4 on 2022-12-15 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_currency_short_title'),
        ('order', '0012_alter_electedorder_user_delete_savedsearch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='budgets',
            field=models.ManyToManyField(to='payment.budget'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_methods',
            field=models.ManyToManyField(to='payment.paymentmethod'),
        ),
    ]
