# Generated by Django 5.0.1 on 2024-01-23 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_proxy', '0002_customuser_delete_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
