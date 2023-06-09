# Generated by Django 4.2 on 2023-05-19 14:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("amenities", "0002_initial"),
        ("experiences", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="amenities",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="experiences",
                to="amenities.amenity",
            ),
        ),
    ]
