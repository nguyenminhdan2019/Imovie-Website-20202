# Generated by Django 3.1.7 on 2021-05-20 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_auto_20210515_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(max_length=140, null=True),
        ),
    ]
