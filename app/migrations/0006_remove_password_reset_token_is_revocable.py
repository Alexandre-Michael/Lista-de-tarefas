# Generated by Django 5.1.1 on 2025-01-09 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_password_reset_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password_reset_token',
            name='is_revocable',
        ),
    ]
