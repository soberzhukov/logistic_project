# Generated by Django 4.0.2 on 2022-02-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, verbose_name='Администратор для обслуживания устройства'),
        ),
    ]
