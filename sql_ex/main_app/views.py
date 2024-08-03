from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import RecordLabel
from .models import Musician
from .models import Album
from .serializers import RecordLabelSerializer
from .serializers import MusicianSerializer
from .serializers import AlbumSerializer

def index(request):
    return render(request, 'main_app/index.html')

class RecordLabelListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ''' List all the record labels
        '''
        record_labels = RecordLabel.objects.all()
        serializer = RecordLabelSerializer(record_labels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        ''' Create a new RecordLabel with the provided data
        '''
        data = {
            'name': request.data.get('name'), 
            'address': request.data.get('address'), 
            'email': request.data.get('email'),
        }
        serializer = RecordLabelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MusicianListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ''' List musicians based on user group
        '''
        if request.user.groups.filter(name='Admin').exists():
            # Admins can see all musicians without filtering by agent
            musicians = Musician.objects.all()
        elif request.user.groups.filter(name='Talent Agents').exists():
            # Talent Agents see only musicians associated with them
            musicians = Musician.objects.filter(agent=request.user)
        else:
            return Response(
                {"res": "You do not have permission to view musicians."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MusicianSerializer(musicians, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        ''' Create a new Musician with the provided data
        '''
        # Check if the user is in the 'Talent Agents' group
        is_talent_agent = request.user.groups.filter(name='Talent Agents').exists()
        data = {
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'instrument': request.data.get('instrument'),
            'agent': request.user.id if is_talent_agent else None  # Set agent to None if not in 'Talent Agents'
        }
        serializer = MusicianSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MusicianDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, musician_id, user):
        ''' Helper method to get the Musician object with the given id
        '''
        try:
            return Musician.objects.get(id=musician_id, agent=user)
        except Musician.DoesNotExist:
            return None

    def get(self, request, musician_id, *args, **kwargs):
        ''' Retrieve the Musician with the given id
        '''
        musician_instance = self.get_object(musician_id, request.user)
        if not musician_instance:
            return Response(
                {"res": "Musician with the given id does not exist or you do not have permission to view it"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MusicianSerializer(musician_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, musician_id, *args, **kwargs):
        ''' Update the Musician with the given id
        '''
        musician_instance = self.get_object(musician_id, request.user)
        if not musician_instance:
            return Response(
                {"res": "Musician with the given id does not exist or you do not have permission to update it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = {
            'first_name': request.data.get('first_name'), 
            'last_name': request.data.get('last_name'), 
            'instrument': request.data.get('instrument'),
        }
        serializer = MusicianSerializer(instance=musician_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, musician_id, *args, **kwargs):
        ''' Delete the Musician with the given id
        '''
        musician_instance = self.get_object(musician_id, request.user)
        if not musician_instance:
            return Response(
                {"res": "Musician with the given id does not exist or you do not have permission to delete it"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        musician_instance.delete()
        return Response({"res": "Musician deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class AlbumListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ''' List all the albums for the authenticated user
        '''
        if request.user.has_perm('main_app.view_album'):
            albums = Album.objects.all()
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        else:
            return Response(
                {"detail": "You do not have permission to view albums."},
                status=status.HTTP_403_FORBIDDEN
            )  

    def post(self, request, *args, **kwargs):
        ''' Create a new album with the provided data
        '''
        if request.user.has_perm('main_app.add_album'):
            data = {
                'title': request.data.get('title'),
                'artist': request.data.get('artist'),
                'release_date': request.data.get('release_date'),
                'genre': request.data.get('genre'),
                'label': request.data.get('label'),  # Expecting the record label ID
                'album_members': request.data.get('album_members'),  # Expecting a list of musician IDs
            }
            serializer = AlbumSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "You do not have permission to add albums."},
                status=status.HTTP_403_FORBIDDEN
            )
