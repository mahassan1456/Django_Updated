# Generated by Django 4.0.2 on 2022-02-26 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
