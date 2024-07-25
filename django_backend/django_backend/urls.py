"""django_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
from image_upload.views import (
    upload_image_view,
    image_detail_view,
    image_update_view,
    image_delete_view,
)
from .views import (
    home_view,
)

from recipe_recommendation_app.views import (
    recipe_recommendation_view,
    recipe_detail_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_view),

    #image upload and recognition
    path("image_upload/upload_image/", upload_image_view, name="upload_image"),
    path("image_upload/<int:id>/", image_detail_view, name="image_detail"),
    path("image_upload/<int:id>/update/", image_update_view, name="image_update"),
    path("image_upload/<int:id>/delete/", image_delete_view, name="image_delete"),
    
    #authentication
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),

    #recipe recommendation
    path("recommend/", recipe_recommendation_view, name="recipe_recommendation"),
    path("recommend/<str:recipe>/", recipe_detail_view, name="recipe_detail"),
    # path('external_link/<str:recipe>/', external_link_view, name='external_link'),
    # path("recommend/<str:recipe>/<str:link>", external_link_view, name="redirect_link")
    # path('redirect/<path:url>/', external_link_view, name='external_link_view'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
