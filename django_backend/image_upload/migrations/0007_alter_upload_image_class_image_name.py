# Generated by Django 4.1 on 2024-06-22 20:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("image_upload", "0006_alter_upload_image_class_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="upload_image_class",
            name="image_name",
            field=models.TextField(default=""),
        ),
    ]
