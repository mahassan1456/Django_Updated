# Generated by Django 4.0.2 on 2022-02-21 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_remove_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]