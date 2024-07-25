import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import upload_image_class

@receiver(post_delete, sender=upload_image_class)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)