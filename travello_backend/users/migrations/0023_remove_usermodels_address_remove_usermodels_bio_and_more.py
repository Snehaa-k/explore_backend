# Generated by Django 5.0.7 on 2024-08-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_remove_userprofile_address_remove_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodels',
            name='address',
        ),
        migrations.RemoveField(
            model_name='usermodels',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='usermodels',
            name='country_state',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(default=9, max_length=345),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(max_length=234, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country_state',
            field=models.CharField(max_length=234, null=True),
        ),
    ]
