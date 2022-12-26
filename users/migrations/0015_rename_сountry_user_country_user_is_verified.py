# Generated by Django 4.0.4 on 2022-12-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_rename_country_user_сountry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='сountry',
            new_name='country',
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Верифицирован?'),
        ),
    ]
