# Generated by Django 4.2 on 2023-06-01 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price']},
        ),
    ]
