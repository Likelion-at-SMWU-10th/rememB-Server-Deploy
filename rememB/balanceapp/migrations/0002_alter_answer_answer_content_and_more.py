# Generated by Django 4.0.6 on 2022-08-11 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_content',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_content',
            field=models.CharField(max_length=300),
        ),
    ]
