# Generated by Django 4.0.4 on 2023-01-11 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_image'),
        ('users', '0021_remove_passportfiles_main_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passportfiles',
            name='main_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_main_page', to='common.File', verbose_name='Главная страница паспорта'),
        ),
        migrations.AddField(
            model_name='passportfiles',
            name='registration_page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_registration_page', to='common.File', verbose_name='Страница прописки'),
        ),
        migrations.AddField(
            model_name='passportfiles',
            name='selfie_with_passport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='passport_selfie_with_passport', to='common.File', verbose_name='Селви с папортом'),
        ),
    ]