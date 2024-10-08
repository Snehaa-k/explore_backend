# Generated by Django 5.0.7 on 2024-09-04 18:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_rename_image_post_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='article',
        ),
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('article', models.TextField(blank=True, null=True)),
                ('travel_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
