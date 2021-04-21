# Generated by Django 2.2.5 on 2021-04-21 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_service', '0003_auto_20210417_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='collaborative_recommendations',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='movie',
            name='content_based_recommendations',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='movie',
            name='key_words',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
