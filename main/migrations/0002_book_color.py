# Generated by Django 5.0.6 on 2024-06-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="color",
            field=models.IntegerField(
                choices=[(1, "Red"), (2, "Blue"), (3, "Green")], default=1
            ),
        ),
    ]
