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
# from django.contrib import admin

# Import 'path' from Django's URL dispatcher to define URL patterns and map them to specific views.
# Import the 'include' function to reference other URL configurations.
from django.urls import path, include, re_path

# Import functions from drf_yasg to create schema views for API documentation.
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a schema view for generating API documentation, specifying metadata like title, version, and contact information.
main_app_schema_view = get_schema_view(
    openapi.Info(
        title="nosql_ex Project: Main App API",
        default_version='v1',
        description="API documentation for all API views present in main_app - view.py",
        terms_of_service=None,
        contact=openapi.Contact(email='lukewait@outlook.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    
    # This setting determines access control for the API documentation, currently allowing anyone to view the schema. 
    # This can be adjusted to restrict access to authenticated users.
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin site URL - provides an interface for managing application models and data.
    # path('admin/', admin.site.urls),
    
    # Define endpoints for accessing the OpenAPI schema documentation in different formats (JSON or YAML).
    # This allows developers to programmatically retrieve the API specifications in standard formats.
    re_path(r'^swagger/main_app(?P<format>\.json|\.yaml)$', main_app_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # Define endpoints for accessing OpenAPI schema documentation rendered with Swagger UI or Redoc UI, 
    # providing a user-friendly interface to explore API endpoints and test requests directly in the browser.
    path('swagger/main_app/', main_app_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/main_app/', main_app_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Main application URLs - this sets the base URL path and for the app and includes the URL patterns 
    # defined in the main_app's 'urls.py', allowing access to the functionalities specific to that application.
    path('main_app/', include('main_app.urls')),
    # Auth application URLs - same as Main application but for authentication fucntionalities defined in auth_app.
    # This app handles user/role syncronisation with MongoDB and uses the data for authentication purposes.
    path('auth_app/', include('auth_app.urls')),
]