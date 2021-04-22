# Generated by Django 3.2 on 2021-04-22 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0007_item_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('P', 'Phone'), ('C', 'Car'), ('L', 'Lamp')], max_length=2),
        ),
    ]