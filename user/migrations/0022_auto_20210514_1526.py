# Generated by Django 3.1.7 on 2021-05-14 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20210514_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='follow',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='post',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='reply_to_post',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='reply_to_review',
        ),
    ]
