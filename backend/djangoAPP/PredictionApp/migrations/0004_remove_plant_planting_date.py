# Generated by Django 5.0.3 on 2024-03-22 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PredictionApp', '0003_remove_plant_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='planting_date',
        ),
    ]
