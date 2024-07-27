import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import upload_image_class
from .forms import image_upload_form, image_name_update_form
from .utils.recognition import predict_image_class



@login_required
def user_images_view(request):
    user_images = upload_image_class.objects.filter(user=request.user)
    return render(request, 'image_upload/user_images.html', {'images': user_images})


@login_required
def upload_image_view(request):
    if request.method == "POST":
        form = image_upload_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # Save form but don't commit to database yet
            instance.user = request.user  # Associate the uploaded image with the current user
            instance.save()
            try:
                
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', os.path.basename(instance.image.name))
                image_path = image_path.replace('\\', '/')

                # Check if file exists
                if not os.path.isfile(image_path):
                    error_message = f"File not found: {image_path}"
                    print(error_message)
                    return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})

                
                predicted_class = None

                # Set image_name based on user input or predicted value
                if not instance.image_name:
                    predicted_class = predict_image_class(image_path)
                    instance.image_name = predicted_class
                    # Save predicted class to the instance and then to the database
                    instance.predicted_class = predicted_class
                    if predicted_class is None:
                        error_message = "Prediction failed. No class returned."
                        print(error_message)
                        return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})

                instance.save()  # Save again with the predicted class

                success_message = "Image uploaded successfully!"


                context = {
                    'predicted_class': predicted_class,
                    'uploaded_image_url': instance.image.url,  # Pass image URL to display in results
                    'image_name': instance.image_name,
                    'form': form,
                    'success_message': success_message,
                }

               
                return render(request, 'image_upload/upload_image.html', context)
            except Exception as e:
                
                error_message = f"Error predicting image from upload_image_view: {e}"
                return render(request, 'image_upload/upload_image.html', {'form': form, 'error': error_message})
    else:
        form = image_upload_form()

    return render(request, 'image_upload/upload_image.html', {'form': form})


@login_required
def image_detail_view(request, id=None):
    image_obj = None
    if id is not None:
        image_obj = get_object_or_404(upload_image_class, id=id, user=request.user)
        rot_status = rot_calculator(image_obj)


    context = {
        "object": image_obj,
        "rot_status": rot_status,
    }
    return render(request, "image_upload/details.html", context=context)





@login_required
def image_update_view(request, id=None):
    image_obj = get_object_or_404(upload_image_class, id=id, user=request.user)
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
    image_obj = get_object_or_404(upload_image_class, id=id, user=request.user)
    if request.method == "POST":
        image_obj.delete()
        return redirect('/') 
    context = {
        "object": image_obj,
    }
    return render(request, "image_upload/delete.html", context=context)




SHELF_LIFE_DICT = {
    'Apple': 42,
    'Banana': 7,
    'Broccoli': 5,
    'Carrots': 24,
    'Cauliflower': 14,
    'Chili': 21,
    'Coconut': 21,
    'Cucumber': 7,
    'Custard apple': 3,
    'Dates': 365,
    'Dragon': 14,
    'Egg': 35,
    'Garlic': 21,
    'Grape': 14,
    'Green Lemon': 28,
    'Jackfruit': 7,
    'Kiwi': 10,
    'Mango': 6,
    'Okra': 3,
    'Onion': 30,
    'Orange': 21,
    'Papaya': 7,
    'Peanut': 180,
    'Pineapple': 5,
    'Pomegranate': 28,
    'Star Fruit': 7,
    'Strawberry': 7,
    'Sweet Potato': 35,
    'Watermelon': 21,
    'White Mushroom': 10,
}


@login_required
def rot_calculator(image_obj):
    current_date = datetime.now()
    uploaded_date = image_obj.uploaded_at.replace(tzinfo=None)

    stored_days = (current_date - uploaded_date).days
    shelf_life = SHELF_LIFE_DICT.get(image_obj.image_name, 0)

    good = (30/100)*shelf_life
    moderate = good + (40/100)*shelf_life
    getting_bad = moderate + (30/100)*shelf_life

    if 0 <= stored_days < good:
        return "good"
    elif good <= stored_days < moderate:
        return "moderate"
    elif moderate <= stored_days < getting_bad:
        return "getting_bad"
    else:
        return "expired"

    