from rest_framework import serializers
from .models import RecordLabel
from .models import Musician
from .models import Album

class RecordLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordLabel
        fields = ["id", "name", "address", "email"]

class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musician
        fields = ["id", "first_name", "last_name", "instrument"]
        
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "title", "artist", "release_date", "genre", "label", "album_members"]
