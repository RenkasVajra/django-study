# Generated by Django 5.0.1 on 2024-01-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulearn', '0003_demand_table_geography_table_alter_demand_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='image',
            field=models.ImageField(null=True, upload_to='img', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='geography',
            name='image',
            field=models.ImageField(null=True, upload_to='img', verbose_name='Изображение'),
        ),
    ]