# Generated by Django 4.0.2 on 2022-02-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to='test/'),
        ),
    ]