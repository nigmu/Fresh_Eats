import os, sys

from django.shortcuts import render
from django.shortcuts import render, redirect

from image_upload.models import upload_image_class
from .recipe_recommendation.Recipe_recom import RecSys

# Create your views here.


def recipe_recommendations():
    ingredients = upload_image_class.objects.values_list('image_name', flat=True).order_by('uploaded_at')
    
    combined_ingredients = ", ". join(ingredients)
    
    recommendations = RecSys(combined_ingredients, N=10)
    return recommendations


# This function is again defined in home_view to display in the main.html, th below is for recommendations.html
def recipe_recommendation_view(request):
    
    recommendations = recipe_recommendations()
    
    context = {
        'recommendations': recommendations,
    }

    print(recommendations)
    
    return render(request, 'recipe_recommendation_app/recommendations.html',context=context)
    # return render(request, 'base.html',context=context)
    


def recipe_detail_view(request, recipe):
    recommendations = recipe_recommendations().to_dict('records')

    # Filter out the recipe details by name
    recipe_details = next((rec for rec in recommendations if rec['recipe'] == recipe), None)

    ing_strip = (str(recipe_details['ingredients']).strip()).split(",")

    dir_strip = (str(recipe_details['directions']).strip('[]"')).split('", "')

    url = "https://"+recipe_details.get('url', '') #https:// added so that python recognise it as an extaernal link

    context = {
        "recipe_name": recipe,
        "recipe_details": recipe_details,
        "directions": dir_strip,
        "ingredients": ing_strip,
        "external_url": url,
    }
    return render(request, "recipe_recommendation_app/recipe_details.html", context=context)
