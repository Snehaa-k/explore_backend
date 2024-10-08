# Generated by Django 5.0.7 on 2024-10-06 14:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_trips_is_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.trips')),
            ],
        ),
    ]
