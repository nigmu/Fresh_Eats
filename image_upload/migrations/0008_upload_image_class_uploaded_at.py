# Generated by Django 4.1 on 2024-06-23 08:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("image_upload", "0007_alter_upload_image_class_image_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="upload_image_class",
            name="uploaded_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
