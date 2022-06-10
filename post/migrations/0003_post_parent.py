# Generated by Django 4.0.2 on 2022-04-04 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post', verbose_name='親コメント'),
        ),
    ]