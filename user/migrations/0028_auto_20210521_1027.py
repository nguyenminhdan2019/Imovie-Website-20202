# Generated by Django 3.1.7 on 2021-05-21 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_profile_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='google_link',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedln_link',
            field=models.CharField(max_length=140, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_link',
            field=models.CharField(max_length=140, null=True),
        ),
    ]
