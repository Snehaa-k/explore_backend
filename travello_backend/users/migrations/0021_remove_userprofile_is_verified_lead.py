# Generated by Django 5.0.7 on 2024-08-24 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_remove_usermodels_otp_expiration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_verified_lead',
        ),
    ]
