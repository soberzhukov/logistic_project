# Generated by Django 4.0.4 on 2022-11-30 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0005_savedsearch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedsearch',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_savedsearch', to=settings.AUTH_USER_MODEL),
        ),
    ]
