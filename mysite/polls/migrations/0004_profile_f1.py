# Generated by Django 4.0.2 on 2022-02-21 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_profile_picture_alter_profile_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='f1',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
