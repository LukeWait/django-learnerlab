"""serializers.py

This file defines the serializers for converting complex data types, such as Django models, into native Python data types.
These serializers are used to transform model instances into JSON, XML, or other content types for use with APIs.
Serializers also handle validation and deserialization of input data.
"""

# Import 'serializers' from Django REST Framework to convert complex data types, 
# such as querysets and model instances, into JSON and vice versa.
from rest_framework import serializers
# Import the models defined in the 'models.py' file to be serialized.
from .models import RecordLabel, Musician, Album

class RecordLabelSerializer(serializers.ModelSerializer):
    """Serializer for the RecordLabel model.
    """
    class Meta:
        """Configures the serializer. It defines the model to serialize and specifies 
        which fields should be included or excluded from the serialized output.
        """
        model = RecordLabel
        # You can opt to include all fields from the associated model.
        fields = '__all__'

class MusicianSerializer(serializers.ModelSerializer):
    """Serializer for the Musician model.
    """
    # Custom field to display the agent's 'username' instead of the default agent 'id'.
    agent_username = serializers.CharField(source='agent.username', read_only=True)
    
    class Meta:
        """Configures the serializer. It defines the model to serialize and specifies 
        which fields should be included or excluded from the serialized output.
        """
        model = Musician
        # Specify the fields to be included to abstract the agent 'id' since we're using 'agent_username'.
        fields = ['id', 'first_name', 'last_name', 'instrument', 'agent_username']

class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for the Album model.
    """
    # Nested serializers to include serialized data representing other models.
    # This ensures that label/album_members outputs the serialized data and not just the 'id' numbers.
    label = RecordLabelSerializer(read_only=True)
    album_members = MusicianSerializer(many=True, read_only=True)
    
    class Meta:
        """Configures the serializer. It defines the model to serialize and specifies 
        which fields should be included or excluded from the serialized output.
        """
        model = Album
        fields = '__all__'
