# Generated by Django 4.0.3 on 2022-05-24 03:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_dreamstream', '0007_profiledetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProfileDetails',
            new_name='Profile',
        ),
    ]
