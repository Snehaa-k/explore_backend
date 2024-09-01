# Generated by Django 5.0.7 on 2024-08-31 04:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_usermodels_is_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('location', models.CharField(max_length=250, null=True)),
                ('type_of_Trip', models.CharField(max_length=250, null=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=345, null=True)),
                ('accommodation', models.CharField(blank=True, max_length=234, null=True)),
                ('transportation', models.CharField(max_length=345)),
                ('amount', models.IntegerField()),
                ('participant_Limit', models.IntegerField()),
                ('travelead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('accomodation', models.TextField(blank=True, max_length=234, null=True)),
                ('Transportation', models.TextField(blank=True, max_length=234, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to='users.trips')),
            ],
        ),
    ]
