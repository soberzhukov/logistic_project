# Generated by Django 4.0.4 on 2022-12-16 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_user_city_user_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='country',
            new_name='сountry',
        ),
    ]
