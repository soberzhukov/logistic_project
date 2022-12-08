# Generated by Django 4.0.4 on 2022-11-30 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0005_electedoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electedoffer',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_user_offer_elected', to=settings.AUTH_USER_MODEL),
        ),
    ]