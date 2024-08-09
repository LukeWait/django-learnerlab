"""serializers.py

This file defines the serializers for converting complex data types, such as MongoDB Objects, into native Python data types.
These serializers are used to transform model instances into JSON, XML, or other content types for use with APIs.
Serializers also handle validation and deserialization of input data.
"""

def MeteoriteSerializer(meteorite):
    """Custom serialization for meteorite_landings documents.
    """
    meteorite['_id'] = str(meteorite['_id'])  # Convert ObjectId to string
    
    return meteorite