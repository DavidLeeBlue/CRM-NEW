# Generated by Django 5.1.3 on 2024-11-29 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='rooms',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('rented', 'Rented'), ('under_maintenance', 'Under Maintenance')], default='available', max_length=20),
        ),
        migrations.AddField(
            model_name='property',
            name='type',
            field=models.CharField(choices=[('apartment', 'Apartment'), ('house', 'House'), ('office', 'Office')], default='apartment', max_length=20),
        ),
    ]
