# Generated by Django 3.1.7 on 2021-05-14 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_user_search'),
        ('user', '0023_auto_20210514_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.user_rate'),
        ),
    ]
