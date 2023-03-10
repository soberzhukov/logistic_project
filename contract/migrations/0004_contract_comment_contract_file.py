# Generated by Django 4.0.4 on 2022-12-26 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0003_alter_contract_offer_alter_contract_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='contract',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/contract_file/', verbose_name='Прикрепленный файл'),
        ),
    ]
