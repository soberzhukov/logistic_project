# Generated by Django 4.0.4 on 2022-11-30 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='condition',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='condition'),
        ),
    ]
