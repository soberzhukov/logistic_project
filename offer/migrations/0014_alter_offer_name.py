# Generated by Django 4.0.4 on 2023-02-06 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0013_offer_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название'),
        ),
    ]
