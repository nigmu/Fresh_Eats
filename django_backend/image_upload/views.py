import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import upload_image_class
from .forms import image_upload_form, image_name_update_form
from .utils.recognition import predict_image_class



# Create your views here.



# def image_upload_view(request):
#     if request.method == "POST":
#         image = request.POST.get('image')
#         print("image:", image)
#         upload_image_class.objects.create(image=image)
#     context = {}
#     return render(request, "image_upload/upload_image.html", context=context)

  # Adjust the import as per your actual model name




# # newer function works better
# def image_upload_view(request):
#     if request.method == "POST":
#         form = image_upload_form(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = image_upload_form()  # Initialize form for GET request
    
#     context = {'form': form}
#     return render(request, "image_upload/upload_image.html", context)


# @login_required
# def image_detail_view(request, id=None):
#     image_obj = None
#     if id is not None:
#         image_obj = upload_image_class.objects.get(id=id)
#     context = {
#         "object": image_obj,
#     }
#     return render(request, "image_upload/details.html", context=context)


@login_required
def image_detail_view(request, id=None):
    image_obj = None
    if id is not None:
        image_obj = upload_image_class.objects.get(id=id)
    context = {
        "object": image_obj,
    }
    return render(request, "image_upload/details.html", context=context)



@login_required
def upload_image_view(request):
    if request.method == "POST":
        form = image_upload_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()  # Save form but don't commit to database yet
            try:
                # Construct the full path to the image
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', os.path.basename(instance.image.name))
                image_path = image_path.replace('\\', '/')  # Normalize path for Windows

                # Check if file exists
                if not os.path.isfile(image_path):
                    error_message = f"File not found: {image_path}"
                    print(error_message)
                    return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})


                # Predict the class of the uploaded image
                
                predicted_class = None

                #Set image_name based on user input or predicted value
                if not instance.image_name:
                    predicted_class = predict_image_class(image_path)
                    instance.image_name = predicted_class
                    # Save predicted class to the instance and then to the database
                    instance.predicted_class = predicted_class
                    if predicted_class is None:
                        error_message = "Prediction failed. No class returned."
                        print(error_message)
                        return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})
                else:
                    instance.predicted_class = None
                    

                
                
                instance.save()  # Save again with the predicted class

                # Prepare context for rendering results or redirect
                context = {
                    'predicted_class': predicted_class,
                    'uploaded_image_url': instance.image.url,  # Pass image URL to display in results
                    'image_name':instance.image_name,
                }

                # Render a result page with prediction
                return render(request, 'show_images.html', context)
            except Exception as e:
                # Handle the exception (e.g., log the error)
                error_message = f"Error predicting image: {e}"
                print(error_message)
                return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})
    else:
        form = image_upload_form()

    return render(request, 'image_upload/upload_image.html', {'form': form})



@login_required
def image_update_view(request, id=None):
    image_obj = get_object_or_404(upload_image_class, id=id)
    form = image_name_update_form(request.POST or None, instance=image_obj)
    
    if form.is_valid():
        form.save()
        return redirect('image_detail', id=image_obj.id)
    context = {
        "form": form,
        "object": image_obj,
    }
    return render(request, "image_upload/update.html", context=context)



@login_required
def image_delete_view(request, id=None):
    image_obj = get_object_or_404(upload_image_class, id=id)
    if request.method == "POST":
        image_obj.delete()
        return redirect('/') 
    context = {
        "object": image_obj,
    }
    return render(request, "image_upload/delete.html", context=context)
