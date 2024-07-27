from django import forms
from .models import upload_image_class


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class image_upload_form(forms.ModelForm):
    class Meta:
        model = upload_image_class 
        fields = ['image', 'image_name', 'description'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})  # Specify accepted file types (optional)
        self.fields['image_name'].required = False


class image_name_update_form(forms.ModelForm):
    class Meta:
        model = upload_image_class
        fields = ['image_name']

