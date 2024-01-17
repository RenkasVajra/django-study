# Generated by Django 5.0.1 on 2024-01-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ulearn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='staticfiles/img')),
            ],
            options={
                'verbose_name': 'Востребованность',
                'verbose_name_plural': 'Востребованности',
                'db_table': 'demand',
            },
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='staticfiles/img')),
            ],
            options={
                'verbose_name': 'География',
                'verbose_name_plural': 'География',
                'db_table': 'geography',
            },
        ),
    ]
