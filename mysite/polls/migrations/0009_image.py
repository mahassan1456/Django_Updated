# Generated by Django 4.0.2 on 2022-02-21 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='test/')),
            ],
        ),
    ]
