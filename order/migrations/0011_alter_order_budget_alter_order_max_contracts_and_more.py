# Generated by Django 4.0.4 on 2022-12-11 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_currency_short_title'),
        ('order', '0010_order_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.budget'),
        ),
        migrations.AlterField(
            model_name='order',
            name='max_contracts',
            field=models.PositiveIntegerField(default=0, verbose_name='Максимальное количество заказчиков'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название Предложениеа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.paymentmethod'),
        ),
    ]