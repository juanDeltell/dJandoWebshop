# Generated by Django 3.2 on 2021-04-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0008_alter_item_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='item_slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
