# Generated by Django 5.0.7 on 2024-08-31 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_alter_trips_accommodation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trips',
            old_name='image',
            new_name='Trip_image',
        ),
        migrations.RenameField(
            model_name='trips',
            old_name='accommodation',
            new_name='accomodation',
        ),
    ]
