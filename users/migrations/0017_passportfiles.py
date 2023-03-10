# Generated by Django 4.0.4 on 2022-12-26 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassportFiles',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('main_page', models.FileField(upload_to='uploads/passports/', verbose_name='Главная страница паспорта')),
                ('registration_page', models.FileField(upload_to='uploads/passports/', verbose_name='Страница прописки')),
                ('date_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passports_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Файлы паспорта',
                'verbose_name_plural': 'Файлы паспорта',
            },
        ),
    ]
