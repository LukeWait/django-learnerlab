"""serializers.py

This file defines the serializers for converting complex data types, such as MongoDB Objects, into native Python data types.
These serializers are used to transform model instances into JSON, XML, or other content types for use with APIs.
Serializers also handle validation and deserialization of input data.
"""

def UserSerializer(user):
    """Custom serialization for user documents.
    """
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    
    return user