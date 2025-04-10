# Generated by Django 5.1.6 on 2025-04-10 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('reference_point', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('relationship', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PregnantWoman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pregnancy.address')),
                ('emergency_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pregnancy.emergencycontact')),
            ],
        ),
    ]
