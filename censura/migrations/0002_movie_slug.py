# Generated by Django 2.2.28 on 2025-03-10 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('censura', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
