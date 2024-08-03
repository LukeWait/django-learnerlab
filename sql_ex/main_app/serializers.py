from rest_framework import serializers
from .models import RecordLabel
from .models import Musician
from .models import Album

class RecordLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordLabel
        fields = ["id", "name", "address", "email"]

class MusicianSerializer(serializers.ModelSerializer):
    # Enables output of agent.username instead of the default - agent.id
    agent_username = serializers.CharField(source='agent.username', read_only=True)
    
    class Meta:
        model = Musician
        fields = ["id", "first_name", "last_name", "instrument", "agent_username"]
        
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "title", "artist", "release_date", "genre", "label", "album_members"]
