# Generated by Django 4.0.3 on 2022-06-09 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_coordenadas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordenadas',
            name='lat',
            field=models.FloatField(default=0, max_length=20),
        ),
        migrations.AlterField(
            model_name='coordenadas',
            name='lon',
            field=models.FloatField(default=0, max_length=20),
        ),
    ]