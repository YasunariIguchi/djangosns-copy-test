# Generated by Django 4.0.3 on 2022-06-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_alter_community_lat_alter_community_lon'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='addr21',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='community',
            name='zip21',
            field=models.TextField(default='0', max_length=3),
        ),
        migrations.AddField(
            model_name='community',
            name='zip22',
            field=models.TextField(default='0', max_length=4),
        ),
    ]
