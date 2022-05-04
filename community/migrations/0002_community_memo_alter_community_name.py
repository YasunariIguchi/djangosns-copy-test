# Generated by Django 4.0.3 on 2022-04-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='memo',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
