# Generated by Django 2.2.5 on 2021-04-16 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_id',
            field=models.PositiveIntegerField(db_index=True, unique=True),
        ),
    ]
