"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

# Imports the 'render' function to serve HTML files (templates) as HttpResponse.
from django.shortcuts import render
# Imports 'Response' class for returning responses in various formats.
from rest_framework.response import Response
# Imports HTTP viewsets, status codes and permissions classes for controlling access to API views.
from rest_framework import viewsets, status, permissions
# Import the models defined in the 'models.py' file to be accessed by API views.
from .models import RecordLabel, Musician, Album
# Imports serializers in 'serializers.py' to convert model instances to JSON and validate incoming data.
from .serializers import RecordLabelSerializer, MusicianSerializer, AlbumSerializer

# Regular views - Regular views in Django respond to HTTP requests by returning HTML content. 
# They can utilize the 'render' function, which points to a given template (like 'index.html') with context data to 
# produce a complete HTML response. Alternatively, views can directly return a 'HttpResponse' object for simpler responses.
def index(request):
    """This function handles rendering the main index page of the application.
    """
    # By default 'render' looks in the 'templates' directory, so this points to main_app/templates/main_app/index.html
    return render(request, 'main_app/index.html')

# API Views - API views in Django, particularly when using the Django REST Framework, are designed to handle programmatic access 
# to resources. They typically return data in formats like JSON, which is suitable for client-side applications or other services.
# ViewSets - ViewSets provided by the Django REST Framework library simplify the implementation of CRUD operations by grouping
# related API views for a model into a single class. They automatically handle requests based on HTTP methods (GET, POST, PUT, 
# PATCH, DELETE) and support features like authentication, permissions, and data serialization. These features drastically reduce 
# the amount of code required.
class RecordLabelViewSet(viewsets.ModelViewSet):
    """This viewset handles HTTP requests for managing record labels.

    It provides the full range of CRUD (Create, Read, Update, Delete) operations for 
    record label entries in the database. This viewset uses the `RecordLabelSerializer`
    for data serialization and validation. All operations require authentication.

    Methods:
        - list: (GET) Retrieve a list of all RecordLabel instances.
        - create: (POST) Create a new RecordLabel instance.
        - retrieve: (GET) Retrieve a specific RecordLabel instance by ID.
        - update: (PUT) Update a specific RecordLabel instance by ID, only if the user manages it.
                  (PATCH) Update specific fields of a RecordLabel instance by ID.
        - destroy: (DELETE) Delete a specific RecordLabel instance by ID.

    Parameters:
        The expected input for create and update actions is in JSON format:
        {
            "name": "Example Label",                          # Expects a string with a maximum length of 100 characters.
            "address": "123 Music Lane, Melody City, 12345",  # Expects a string with a maximum length of 300 characters.
            "email": "contact@examplelabel.com"               # Expects a valid email address.
        }

    Returns:
        - list: A JSON array of serialized RecordLabel instances.
        - create: A JSON object of the newly created RecordLabel instance.
        - retrieve: A JSON object of the specific RecordLabel instance.
        - update: A JSON object of the updated RecordLabel instance.
        - destroy: Status code indicating success (204 No Content) with no body, or an error message if deletion fails.
    """
    queryset = RecordLabel.objects.all()
    serializer_class = RecordLabelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MusicianViewSet(viewsets.ModelViewSet):
    """This viewset handles HTTP requests for managing musicians.

    It provides the full range of CRUD (Create, Read, Update, Delete) operations for 
    musician entries in the database, with specific access controls based on user groups.
    Only 'Talent Agents' can create a new musician. In addition, editing specific musicians 
    (retrive, update, and destroy) can only be performed by the 'agent' who manages the musician.
    This viewset uses the `MusicianSerializer` for data serialization and validation.
    All operations require authentication.

    Methods:
        - list: (GET) Retrieve a list of all Musician instances based on user Group.
        - create: (POST) Create a new Musician instance associated with the current user.
        - retrieve: (GET) Retrieve a specific Musician instance by ID, only if the user manages it.
        - update: (PUT) Update a specific Musician instance by ID, only if the user manages it.
                  (PATCH) Update specific fields of a Musician instance by ID.
        - destroy: (DELETE) Delete a specific Musician instance by ID, only if the user manages it.

    Parameters:
        The expected input for create and update actions is in JSON format:
        {
            "first_name": "Luke",   # Expects a string with a maximum length of 30 characters.
            "last_name": "Wait",    # Expects a string with a maximum length of 30 characters.
            "instrument": "Guitar"  # Expects a string with a maximum length of 50 characters.
        }

    Returns:
        - list: A JSON array of serialized Musician instances based on user Group.
        - create: A JSON object of the newly created Musician instance.
        - retrieve: A JSON object of the specific Musician instance.
        - update: A JSON object of the updated Musician instance.
        - destroy: Status code indicating success (204 No Content) with no body, or an error message if deletion fails.
    """
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve a queryset of Musician instances based on the user's group.

        Admin users can view all musicians, while Talent Agents can only view musicians they manage.
        
        This method is used by the parent class methods (e.g., list, retrieve, update, destroy) through the
        super() function to ensure that the queryset reflects the permissions of the authenticated user.
        """
        if self.request.user.groups.filter(name='Admin').exists():
            return Musician.objects.all()
        elif self.request.user.groups.filter(name='Talent Agents').exists():
            return Musician.objects.filter(agent=self.request.user)
        else:
            return Musician.objects.none()

    # Override the create method to enforce group-based authorization
    def create(self, request, *args, **kwargs):
        """Create a new Musician with the provided data.

        Only users belonging to the 'Talent Agents' Group can use this method.
        """
        if not request.user.groups.filter(name='Talent Agents').exists():
            return Response({'res': 'You do not have permission to create a musician.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    # Override the retrieve method to enforce group-based authorization
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific Musician instance by ID.

        Only the agent that manages a musician can perform this action.
        """
        musician_instance = self.get_object()
        if musician_instance.agent != request.user:
            return Response({'res': 'You do not have permission to view this musician.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)

    # Override the update method to enforce group-based authorization
    def update(self, request, *args, **kwargs):
        """Update a specific Musician instance by ID.

        Only the agent that manages the musician can perform this action.
        """
        musician_instance = self.get_object()
        if musician_instance.agent != request.user:
            return Response({'res': 'You do not have permission to update this musician.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    # Override the destroy method to enforce group-based authorization
    def destroy(self, request, *args, **kwargs):
        """Delete a specific Musician instance by ID.

        Only the agent that manages the musician can perform this action.
        """
        musician_instance = self.get_object()
        if musician_instance.agent != request.user:
            return Response({'res': 'You do not have permission to delete this musician.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
 
class AlbumViewSet(viewsets.ModelViewSet):
    """This viewset handles HTTP requests for managing albums.

    It provides the full range of CRUD (Create, Read, Update, Delete) operations for 
    album entries in the database, with specific access controls based on user permissions.
    It authorizes authenticated users by checking they have explicit permission in Users/Groups. Only 'Admin' should be 
    able to access these API views as 'Talent Agents' are only granted CRUD permissions on the 'Musician' model.
    This viewset uses the `AlbumSerializer` for data serialization and validation.
    All operations require authentication.

    Methods:
        - list: (GET) Retrieve a list of all Album instances that the user has permission to view.
        - create: (POST) Create a new Album instance associated with the current user, if the user has permission.
        - retrieve: (GET) Retrieve a specific Album instance by ID, only if the user has permission to view it.
        - update: (PUT) Update a specific Album instance by ID, only if the user has permission to change it.
                  (PATCH) Update specific fields of an Album instance by ID, subject to permissions.
        - destroy: (DELETE) Delete a specific Album instance by ID, only if the user has permission to delete it.

    Parameters:
        The expected input for create and update actions is in JSON format:
        {
            "title": "My New Album",            # Expects a string with a maximum length of 200 characters.
            "artist": "Famous Artist",          # Expects a string with a maximum length of 200 characters.
            "release_date": "2024-08-04",       # Expects a string in the format YYYY-MM-DD.
            "genre": "Rock",                     # Expects a string with a maximum length of 100 characters.
            "label": 1,                         # Expects an int representing an existing record label 'id'.
            "album_members": [2, 3]             # Expects a list of ints representing existing musician 'id's.
        }

    Returns:
        - list: A JSON array of serialized Album instances that the user has permission to view.
        - create: A JSON object of the newly created Album instance.
        - retrieve: A JSON object of the specific Album instance.
        - update: A JSON object of the updated Album instance.
        - destroy: Status code indicating success (204 No Content) with no body, or an error message if deletion fails.
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override the list method to enforce permission based authorization
    def list(self, request, *args, **kwargs):
        """List all Album entries for the authenticated user.
        
        Only users with the permission 'main_app.view_album' can use this method.
        """
        if not request.user.has_perm('main_app.view_album'):
            return Response({'res': 'You do not have permission to view albums.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().list(request, *args, **kwargs)

    # Override the create method to enforce permission based authorization
    def create(self, request, *args, **kwargs):
        """Create a new Album with the provided data.
        
        Only users with the permission 'main_app.add_album' can use this method.
        """
        if not request.user.has_perm('main_app.add_album'):
            return Response({'res': 'You do not have permission to create an album.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    # Override the retrieve method to enforce permission based authorization
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific Album instance by ID.
        
        Only users with the permission 'main_app.view_album' can use this method.
        """
        if not request.user.has_perm('main_app.view_album'):
            return Response({'res': 'You do not have permission to view this album.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().retrieve(request, *args, **kwargs)

    # Override the udpate method to enforce permission based authorization
    def update(self, request, *args, **kwargs):
        """Update a specific Album instance by ID.
        
        Only users with the permission 'main_app.change_album' can use this method.
        """
        if not request.user.has_perm('main_app.change_album'):
            return Response({'res': 'You do not have permission to update this album.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    # Override the destroy method to enforce permission based authorization
    def destroy(self, request, *args, **kwargs):
        """Delete a specific Album instance by ID.
        
        Only users with the permission 'main_app.delete_album' can use this method.
        """
        if not request.user.has_perm('main_app.delete_album'):
            return Response({'res': 'You do not have permission to delete this album.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
    