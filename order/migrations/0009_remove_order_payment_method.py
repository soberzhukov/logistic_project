# Generated by Django 4.0.4 on 2022-12-08 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_electedorder_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
    ]