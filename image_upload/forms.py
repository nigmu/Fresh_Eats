from django import forms
from .models import upload_image_class


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class image_upload_form(forms.ModelForm):
    class Meta:
        model = upload_image_class  # Replace with your actual model name
        fields = ['image']  # Specify the fields from your model you want to include in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})  # Specify accepted file types (optional)


# image_upload/forms.py
