# Generated by Django 4.1 on 2022-08-11 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letterapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]