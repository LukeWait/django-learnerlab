"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

# Imports the 'render' function to serve HTML files (templates) as HttpResponse.
from django.shortcuts import render
# Imports the 'HttpResponse' function to serve simple HTTP responses.
from django.http import HttpResponse
# Imports 'APIView' class to create structured API views, and 'Response' class for returning responses in various formats.
from rest_framework.views import APIView
from rest_framework.response import Response
# Imports HTTP status codes and permissions classes for controlling access to API views.
from rest_framework import status, permissions
# Import the models defined in the 'models.py' file to be accessed by API views.
from .models import RecordLabel, Musician, Album
# Imports serializers in 'serializers.py' to convert model instances to JSON and validate incoming data.
from .serializers import RecordLabelSerializer, MusicianSerializer, AlbumSerializer

# Regular views - Regular views in Django respond to HTTP requests by returning HTML content. 
# They can utilize the 'render' function, which points to a given template (like 'index.html') with context data to 
# produce a complete HTML response. Alternatively, views can directly return an 'HttpResponse' object for simpler responses.
def index(request):
    """This function handles rendering the main index page of the application.
    """
    # By default 'render' looks in the 'templates' directory, so this points to main_app/templates/main_app/index.html
    return render(request, 'main_app/index.html')
    # return HttpResponse("<h1>Hello and welcome to the <u>sql_ex</u> front end!</h1>")

# API Views - API views in Django, particularly when using the Django REST Framework, are designed
# to handle programmatic access to resources. They typically return data in formats like 
# JSON, which is suitable for client-side applications or other services. The APIView 
# class provides a structure for defining HTTP methods (GET, POST, etc.) to manage requests and responses. 
# It allows you to handle authentication, permissions, and data serialization.
class RecordLabelListApiView(APIView):
    """This class-based API view handles HTTP requests for listing and creating record labels.
    
    It has no authorization check and allows all authenticated users full access.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """List all the record labels.
        
        This method retrieves all record label entries from the database and 
        returns them in a serialized format.
        """
        record_labels = RecordLabel.objects.all()
        serializer = RecordLabelSerializer(record_labels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create a new RecordLabel with the provided data.
        
        This method validates and saves a new record label entry in the database.
        If the data is valid, a new record label is created. 
        Example valid input:
        {
            "name": "Example Label",
            "address": "123 Music Lane, Melody City, 12345",
            "email": "contact@examplelabel.com"
        }
        """
        data = {
            'name': request.data.get('name'),        # Expects a string with a maximum length of 100 characters.
            'address': request.data.get('address'),  # Expects a string with a maximum length of 300 characters.
            'email': request.data.get('email')       # Expects a valid email address.
        }
        serializer = RecordLabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MusicianListApiView(APIView):
    """This class-based API view handles HTTP requests for listing and creating musicians.
    
    It uses Groups to authorize authenticated users to view and create 'Musician' entries.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """List musicians based on user group.
        
        This method retrieves musician entries from the database based on the user's Group.
        'Admin' users are able to view all, whereas 'Talent Agents' can only view musicians they manage.
        """
        if request.user.groups.filter(name='Admin').exists():
            musicians = Musician.objects.all()
        elif request.user.groups.filter(name='Talent Agents').exists():
            musicians = Musician.objects.filter(agent=request.user)
        else:
            # If the user was not in either group they would be denied access.
            return Response(
                {'res': 'You do not have permission to view musicians.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MusicianSerializer(musicians, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create a new Musician with the provided data.
        
        This method validates and saves a new musician entry in the database, associating it with the current user. 
        Only users belonging to the 'Talent Agents' Group can use this method.
        Example valid input:
        {
            "first_name": "Luke",
            "last_name": "Wait",
            "instrument": "Guitar"
        }
        """
        if request.user.groups.filter(name='Talent Agents').exists():
            data = {
                'first_name': request.data.get('first_name'),  # Expects a string with a maximum length of 30 characters.
                'last_name': request.data.get('last_name'),    # Expects a string with a maximum length of 30 characters.
                'instrument': request.data.get('instrument'),  # Expects a string with a maximum length of 50 characters.
                'agent': request.user.id                       # Automatically associates with agent 'id' if applicable.
            }
            serializer = MusicianSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'res': 'You do not have permission to create a musician.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
class MusicianDetailApiView(APIView):
    """This class-based API view handles HTTP requests for individual musician details.
    
    It authorizes authenticated users by comparing the current user to the 'agent' field of the musician with the 
    'musician_id' passed in with the endpoint for this class - defined in 'urls.py' as 'api/musician/<int:musician_id>/'.
    This implies only the agent that manages a musician can perform these methods (GET, PUT, DELETE).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, musician_id, user):
        """Helper method to retrieve a Musician object by ID and associated user.
        
        This method checks if the musician exists and if the requesting user has
        the necessary permissions to access it.
        """
        try:
            return Musician.objects.get(id=musician_id, agent=user)
        except Musician.DoesNotExist:
            return None

    def get(self, request, musician_id, *args, **kwargs):
        """Retrieve the Musician with the given ID.
        
        This method returns the serialized data of a specific musician if the user
        has permission to view it.
        """
        musician_instance = self.get_object(musician_id, request.user)
        if musician_instance:
            serializer = MusicianSerializer(musician_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'res': 'Musician with the given ID does not exist or you do not have permission to view it'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    def put(self, request, musician_id, *args, **kwargs):
        """Update the Musician with the given ID.
        
        This method validates the input data and updates the corresponding musician
        entry in the database if the user has permission to modify it.
        Example valid input:
        {
            "first_name": "Luke",
            "last_name": "Wait",
            "instrument": "Guitar"
        }
        """
        musician_instance = self.get_object(musician_id, request.user)
        if musician_instance:
            data = {
                'first_name': request.data.get('first_name'),  # Expects a string with a maximum length of 30 characters.
                'last_name': request.data.get('last_name'),    # Expects a string with a maximum length of 30 characters.
                'instrument': request.data.get('instrument')   # Expects a string with a maximum length of 50 characters.
            }
            serializer = MusicianSerializer(instance=musician_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'res': 'Musician with the given ID does not exist or you do not have permission to update it'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    def delete(self, request, musician_id, *args, **kwargs):
        """Delete the Musician with the given ID.
        
        This method removes the specified musician entry from the database if
        the user has permission to delete it.
        """
        musician_instance = self.get_object(musician_id, request.user)
        if musician_instance:
            musician_instance.delete()
            return Response({'res': 'Musician deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)   
        else:
            return Response(
                {'res': 'Musician with the given ID does not exist or you do not have permission to delete it'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
class AlbumListApiView(APIView):
    """This class-based API view handles HTTP requests for listing and creating albums.
    
    It authorizes authenticated users by checking they have explicit permission in Users/Groups.
    Only 'Admin' should be able to access these APIs as 'Talent Agents' are only granted CRUD permissions on the 'Musician' model. 
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """List all the albums for the authenticated user.
        
        This method retrieves all album entries from the database that the user
        has permission to view and returns them in a serialized format.
        """
        if request.user.has_perm('main_app.view_album'):
            albums = Album.objects.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        else:
            return Response(
                {'detail': 'You do not have permission to view albums.'},
                status=status.HTTP_403_FORBIDDEN
            )  

    def post(self, request, *args, **kwargs):
        """Create a new album with the provided data.
        
        This method validates and saves a new album entry in the database
        if the user has permission to add albums.
        Example valid input:
        {
            "title": "My New Album",
            "artist": "Famous Artist",
            "release_date": "2024-08-04",
            "genre": "Rock",
            "label": 1,
            "album_members": [2, 3]
        }
        """
        if request.user.has_perm('main_app.add_album'):
            data = {
                'title': request.data.get('title'),                 # Expects a string with a maximum length of 200 characters.
                'artist': request.data.get('artist'),               # Expects a string with a maximum length of 200 characters.
                'release_date': request.data.get('release_date'),   # Expects a A string in the format YYYY-MM-DD.
                'genre': request.data.get('genre'),                 # Expects a string with a maximum length of 100 characters.
                'label': request.data.get('label'),                 # Expects a int representing exiting record label 'id'
                'album_members': request.data.get('album_members')  # Expects a list of ints representing existing musician 'id's.
            }
            serializer = AlbumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'detail': 'You do not have permission to add albums.'},
                status=status.HTTP_403_FORBIDDEN
            )
