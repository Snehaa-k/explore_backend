# Generated by Django 5.0.7 on 2024-08-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_travelleaderform_visited_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodels',
            name='is_approve_leader',
            field=models.BooleanField(default=False),
        ),
    ]
