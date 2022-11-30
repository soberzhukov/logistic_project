# Generated by Django 4.0.4 on 2022-11-30 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0004_alter_offer_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectedOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Отзыв')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_offer_elected', to='offer.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_user_offer_elected', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Избранное предложение',
                'verbose_name_plural': 'Избранные предложения',
            },
        ),
    ]
