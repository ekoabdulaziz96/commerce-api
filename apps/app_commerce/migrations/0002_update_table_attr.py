# Generated by Django 4.2.5 on 2024-09-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_commerce", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="message",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="channel",
            name="name",
            field=models.CharField(
                choices=[
                    ("shopee", "Shopee"),
                    ("tokopedia", "Tokopedia"),
                    ("blibli", "Blibli"),
                ],
                max_length=50,
            ),
        ),
    ]
