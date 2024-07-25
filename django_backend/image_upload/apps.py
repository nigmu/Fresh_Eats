from django.apps import AppConfig


from django.apps import AppConfig

class image_upload_config(AppConfig):
    name = 'image_upload'

    def ready(self):
        import image_upload.signals
