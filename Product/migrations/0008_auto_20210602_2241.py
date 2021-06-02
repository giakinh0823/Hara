# Generated by Django 3.0 on 2021-06-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_remove_product_islike'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='goal',
            field=models.DecimalField(decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
