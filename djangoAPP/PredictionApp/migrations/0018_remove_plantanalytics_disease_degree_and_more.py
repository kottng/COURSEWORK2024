# Generated by Django 5.0.3 on 2024-05-26 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PredictionApp', '0017_delete_image_alter_plantanalytics_plant_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantanalytics',
            name='disease_degree',
        ),
        migrations.RemoveField(
            model_name='plantanalytics',
            name='disease_degree_description',
        ),
    ]
