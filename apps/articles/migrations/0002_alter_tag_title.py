# Generated by Django 4.0.2 on 2022-05-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=35, unique=True),
        ),
    ]
