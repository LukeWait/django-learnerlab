"""urls.py

URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# Import the 'admin' module to register path to the Django admin interface.
from django.contrib import admin
# Import 'path' from Django's URL dispatcher to define URL patterns and map them to specific views.
# Import the 'include' function to reference other URL configurations.
from django.urls import path, include

urlpatterns = [
    # Admin site URL - provides an interface for managing application models and data.
    path('admin/', admin.site.urls),
    # Include REST framework authentication URLs - this allows for built-in authentication endpoints 
    # such as login and logout when using the Django REST Framework.    
    path('auth/', include('rest_framework.urls')),
    # Main application URLs - this sets the base URL path and for the app and includes the URL patterns 
    # defined in the main_app's 'urls.py', allowing access to the functionalities specific to that application.
    path('main_app/', include('main_app.urls'))
]
