# Generated by Django 3.0 on 2021-05-08 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0004_notifications_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='image',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
