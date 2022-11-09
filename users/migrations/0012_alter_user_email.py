# Generated by Django 4.0.4 on 2022-10-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default='ses', max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
