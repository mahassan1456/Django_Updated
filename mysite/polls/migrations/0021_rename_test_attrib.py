# Generated by Django 4.0.2 on 2022-02-21 21:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0020_rename_test_test_work'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test',
            new_name='Attrib',
        ),
    ]