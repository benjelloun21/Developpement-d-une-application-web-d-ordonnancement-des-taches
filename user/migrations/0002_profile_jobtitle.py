# Generated by Django 5.0.4 on 2024-06-06 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='jobtitle',
            field=models.CharField(default='-', max_length=200),
        ),
    ]
