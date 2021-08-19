# Generated by Django 3.2.5 on 2021-08-19 10:53

import accounts.models
import core.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default/avatar.jpeg', storage=core.storage_backends.PublicMediaStorage, upload_to=accounts.models.user_directory_path, validators=[accounts.models.validate_image]),
        ),
    ]
