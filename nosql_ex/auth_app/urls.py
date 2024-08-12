"""urls.py

This file defines the URL patterns for the Django application, mapping URL paths to their corresponding views.
It extends the base URL patterns defined in the main project's URL configuration (config/urls.py).
Each URL pattern is considered an endpoint (or API endpoint for API views), providing specific routes to access the app's functionalities.
"""

# Import 'path' from Django's URL dispatcher to define URL patterns and map them to specific views.
from django.urls import path
# Import all views from 'views.py' to utilize specific functions and classes for handling requests and responses.
from . import views

# URL patterns define the routes for the application, mapping specific URL paths to their corresponding view functions.
# The base URL is defined in 'config/urls.py' (auth_app/), so these serve as an extension to that.
# For example when using 'python manage.py runserver' -> http://127.0.0.1:8000/main_app/api/user_manage/
urlpatterns = [
    path('',views.index,name='index'),
    path('api/user_manage/', views.UserManageApiView.as_view())
    ]