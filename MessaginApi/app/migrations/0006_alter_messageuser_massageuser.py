# Generated by Django 4.0.6 on 2022-11-22 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageuser',
            name='massageUser',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
