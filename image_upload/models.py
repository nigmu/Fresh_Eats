from django.db import models
from django.utils import timezone

# Create your models here.
class upload_image_class(models.Model):
    image = models.ImageField(upload_to="images/", default="")
    image_name = models.TextField(default="")
    uploaded_at = models.DateTimeField(default=timezone.now)
    predicted_class = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.image_name