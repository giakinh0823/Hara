# Generated by Django 3.0 on 2021-05-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_order_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
