# Generated by Django 3.1.7 on 2021-05-15 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_userseennotifycation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userseennotifycation',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti', to='user.notification'),
        ),
    ]