# Generated by Django 4.0.6 on 2022-11-22 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_massage_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='id_massage',
        ),
    ]
