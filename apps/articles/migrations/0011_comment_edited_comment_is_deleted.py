# Generated by Django 4.0.2 on 2022-06-28 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_comment_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
