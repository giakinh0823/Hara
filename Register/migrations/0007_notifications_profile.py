# Generated by Django 3.0 on 2021-05-08 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0006_auto_20210508_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Register.Profile'),
        ),
    ]
