# Generated by Django 4.0.4 on 2023-01-11 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_passportfiles_selfie_with_passport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passportfiles',
            name='main_page',
        ),
        migrations.RemoveField(
            model_name='passportfiles',
            name='registration_page',
        ),
        migrations.RemoveField(
            model_name='passportfiles',
            name='selfie_with_passport',
        ),
    ]
