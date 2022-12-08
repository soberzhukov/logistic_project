# Generated by Django 4.0.4 on 2022-12-08 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_currency_alter_paymentmethod_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='budgets', to='payment.currency'),
        ),
    ]