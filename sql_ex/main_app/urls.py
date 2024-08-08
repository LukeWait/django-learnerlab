"""urls.py

This file defines the URL patterns for the Django application, mapping URL paths to their corresponding views.
It extends the base URL patterns defined in the main project's URL configuration (config/urls.py).
Each URL pattern is considered an endpoint (or API endpoint for API views), providing specific routes to access the app's functionalities.
"""

# Import 'path' from Django's URL dispatcher to define URL patterns and map them to specific views.
from django.urls import path, include
# Import all views from 'views.py' to utilize specific functions and classes for handling requests and responses.
from . import views

# Import 'DefaultRouter' from Django REST Framework to create a router that automatically generates URL conf for ViewSets.
from rest_framework.routers import DefaultRouter
# Initialize the router instance that will manage the URL routing for API endpoints, mapping them to the corresponding ViewSets.
router = DefaultRouter()
# Register ViewSets with the router. This allows for automatic generation of the standard CRUD URLs for each ViewSet.
# The registered name becomes part of the endpoint path.
router.register(r'record_label', views.RecordLabelViewSet)
router.register(r'musician', views.MusicianViewSet)
router.register(r'album', views.AlbumViewSet)

# URL patterns define the routes for the application, mapping specific URL paths to their corresponding view functions.
# The base URL is defined in 'config/urls.py' (main_app/), so these serve as an extension to that.
# For example when using 'python manage.py runserver' -> http://127.0.0.1:8000/main_app/api/record_label/
urlpatterns = [
    # Endpoints - represent routes in the application that provide access to various client-facing views, such as web pages or forms.
    path('', views.index, name='index'),
    # API endpoints - the registered routes need to be included in the urlpatterns. It's common practice to include 'api/' in the
    # path to ensure all your API endpoints have a clear distinction.
    path('api/', include(router.urls)),
]
