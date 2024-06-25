from django.http import HttpResponse
from django.template.loader import render_to_string
from image_upload.models import upload_image_class
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


@login_required
def home_view(request, id=None, *args, **kwargs):

    try:
        image_obj = upload_image_class.objects.latest('id')
        image_list = upload_image_class.objects.all()
        context = {
            "object_list" : image_list,
            "id" : image_obj.id,
            "object" : image_obj,
            "image" : image_obj.image,
            "image_name" : image_obj.image_name,
            "uploaded_at" : image_obj.uploaded_at,
            "predicted_class" : image_obj.predicted_class,
            "user": request.user
        }
    except ObjectDoesNotExist:
        context = {
            "error_message": "No image found",
            "user": request.user
        }



    html = render_to_string('show_images.html', context=context)

    return HttpResponse(html)
