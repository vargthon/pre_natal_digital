# Generated by Django 4.2.6 on 2023-10-11 00:26

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.image_upload_path),
        ),
    ]
