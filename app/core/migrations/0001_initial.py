# Generated by Django 5.1.6 on 2025-03-25 00:56

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to=core.models.image_upload_path)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('full_name', models.CharField(max_length=255)),
                ('sus_card_number', models.CharField(max_length=20, unique=True)),
                ('birth_date', models.DateField()),
                ('nis_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('prefered_name', models.CharField(blank=True, max_length=255, null=True)),
                ('race', models.CharField(max_length=50)),
                ('ethnicity', models.CharField(max_length=50)),
                ('work_outside_home', models.BooleanField(default=False)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('due_date', models.DateField()),
                ('image', models.ImageField(null=True, upload_to=core.models.profile_image_upload_path)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
