# Generated by Django 4.0.5 on 2022-08-18 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letterapp', '0005_letter_user_alter_letter_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='letter_from',
            field=models.CharField(max_length=100, null=True),
        ),
    ]