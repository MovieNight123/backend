# Generated by Django 2.2.5 on 2021-04-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_service', '0005_auto_20210421_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='collaborative_recommendations',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='content_based_recommendations',
            field=models.CharField(default='', max_length=256, null=True),
        ),
    ]
