# Generated by Django 4.0.2 on 2022-08-24 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_confirmpassword_confirmphone_delete_confirmcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_confirmed',
        ),
    ]
