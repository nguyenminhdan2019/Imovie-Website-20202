# Generated by Django 3.1.7 on 2021-04-04 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20210404_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='slug',
        ),
    ]
