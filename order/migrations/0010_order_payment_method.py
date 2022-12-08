# Generated by Django 4.0.4 on 2022-12-08 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_paymentmethod'),
        ('order', '0009_remove_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='payment.paymentmethod'),
        ),
    ]
