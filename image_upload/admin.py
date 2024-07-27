from django.contrib import admin

# Register your models here.
from .models import upload_image_class

class upload_image_class_admin(admin.ModelAdmin):
    list_display = ['id', 'image_name', 'predicted_class','uploaded_at', 'description']
    search_fields = ['image_name', 'predicted_class', 'uploaded_at']


admin.site.register(upload_image_class, upload_image_class_admin)