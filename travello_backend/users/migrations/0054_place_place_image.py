# Generated by Django 5.0.7 on 2024-10-05 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0053_usermodels_reset_token_usermodels_token_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='place_image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
