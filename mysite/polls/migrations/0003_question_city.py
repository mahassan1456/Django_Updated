# Generated by Django 4.0.2 on 2022-02-12 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_question_test_question_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='city',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
