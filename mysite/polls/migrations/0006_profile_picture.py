# Generated by Django 4.0.2 on 2022-02-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_profile_f1_remove_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='999', upload_to='uploads/'),
        ),
    ]