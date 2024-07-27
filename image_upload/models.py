from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class upload_image_class(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", default="")
    image_name = models.CharField(max_length=100, default="", blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    predicted_class = models.CharField(max_length=100, null=True, blank=True)

    @classmethod
    def get_serialized_objects(cls):
        objects = cls.objects.all().order_by('id')
        for index, obj in enumerate(objects, start=1):
            setattr(obj, 'serial_number', index)
        return objects
    

    def __str__(self):
        return self.image_name if self.image_name else "Untitled Image"