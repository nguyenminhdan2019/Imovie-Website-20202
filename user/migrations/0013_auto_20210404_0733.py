# Generated by Django 3.1.7 on 2021-04-04 07:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0012_commenttopost_posttouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttouser',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posttouser',
            name='reports',
            field=models.ManyToManyField(blank=True, related_name='reports', to=settings.AUTH_USER_MODEL),
        ),
    ]
