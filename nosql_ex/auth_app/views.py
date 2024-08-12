"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

from django.http import JsonResponse, HttpResponse
from django.views import View
from .serializers import UserSerializer
import json
from bson import ObjectId
import hashlib
from datetime import datetime, timezone
import requests
from django.views.decorators.csrf import csrf_exempt
import pymongo

# use pymongo to connect to db
client = pymongo.MongoClient('mongodb+srv://<user>:<password@djangolab-cluster.y0zsa4f.mongodb.net/')
dbname = client['nasa_data_db']
collection = dbname['users']

# MongoDB Atlas API credentials
MONGODB_ATLAS_API_PUBLIC_KEY = ''
MONGODB_ATLAS_API_PRIVATE_KEY = ''
MONGODB_ATLAS_PROJECT_ID = ''
MONGODB_ATLAS_GROUP_ID = ''

def hash_password(password):
    """Hash the password using SHA-256 or another suitable hashing algorithm.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

"""
def create_mongodb_atlas_user(username, password):
    url = f"https://cloud.mongodb.com/api/atlas/v1.0/groups/{MONGODB_ATLAS_GROUP_ID}/databaseUsers"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "databaseName": "nasa_data_db",
        "roles": [
            {
                "roleName": "readWrite",
                "databaseName": "users"
            }
        ],
        "username": username,
        "password": password
    }
    
    response = requests.post(url, auth=(MONGODB_ATLAS_API_PUBLIC_KEY, MONGODB_ATLAS_API_PRIVATE_KEY), json=payload, headers=headers)

    if response.status_code == 201:
        print(f"MongoDB Atlas user {username} created successfully.")
    else:
        print(f"Failed to create MongoDB Atlas user: {response.json()}")
"""

# Regular views - Regular views in Django respond to HTTP requests by returning HTML content. 
# They can utilize the 'render' function, which points to a given template (like 'index.html') with context data to 
# produce a complete HTML response. Alternatively, views can directly return a 'HttpResponse' object for simpler responses.
def index(request):
    """This function returns a simple HttpResponse.
    """
    return HttpResponse("<h1>Hello and welcome to the <u>nosql_ex auth_app!</u></h1>")
 
# API Views - API views are designed to handle programmatic access to resources. 
# They typically return data in formats like JSON, which is suitable for client-side applications or other services. 
# The View class provides a structure for defining HTTP methods (GET, POST, etc.) to manage requests and responses.
class UserManageApiView(View):
    """This view handles HTTP requests for managing user data in the system.

    It provides CRUD (Create, Read, Update, Delete) operations for user records in the database.
    All operations return JSON responses.

    Methods:
        - get: (GET) Retrieve a list of all users.
        - post: (POST) Create a new user record.
        - put: (PUT) Update an existing user record by its ID.
        - delete: (DELETE) Delete a user record by its ID.

    Parameters:
        The expected input for post and put actions is in JSON format:
        {
            "username": "luke",                    # Expects a string with the username.
            "password": "hashed_password",         # Expects a string with the hashed password.
            "roles": ["administrator", "user"],    # Expects a list of strings indicating user roles.
            "last_login": "2024-08-09T04:05:23Z",  # Expects a string in ISO 8601 format representing the last login time.
            "profile_data": {                      # Expects a dictionary containing profile information.
                "first_name": "Luke",              # Expects a string with the user's first name.
                "last_name": "Wait",               # Expects a string with the user's last name.
                "email": "lukewait@email.com"      # Expects a string with the user's email.
            }
        }

    Returns:
        - get: A JSON response with a list of serialized user instances.
        - post: A JSON response with the ID of the newly created user instance.
        - put: A JSON response indicating success or failure. Status 200 if the record was updated.
        - delete: A JSON response indicating success or failure. Status 200 if the record was deleted.
    """
    def get(self, request):
        """Retrieve a list of users.
        """
        cursor = collection.find()
        list_cur = list(cursor)
        serialized_users = [UserSerializer(user) for user in list_cur]
        return JsonResponse(serialized_users, safe=False)

    def post(self, request):
        """Create a new user record.
        """
        body = json.loads(request.body.decode("utf-8"))
        hashed_password = hash_password(body.get('password')) # Hash the password before storing
        new_user = {
            "username": body.get('username'),
            "password": hashed_password,  
            "roles": body.get('roles', ["user"]),             # Default role to 'user' if not provided
            "last_login": datetime.now(timezone.utc),         # Use timezone-aware datetime for last_login
            "profile_data": {
                "first_name": body.get('profile_data', {}).get('first_name'),
                "last_name": body.get('profile_data', {}).get('last_name'),
                "email": body.get('profile_data', {}).get('email')
            }
        }

        result = collection.insert_one(new_user)
        data = {"_id": str(result.inserted_id)}
        # Create a MongoDB Atlas admin user
        # create_mongodb_atlas_user(new_user['username'], hashed_password)
        return JsonResponse(data, status=201)

    def put(self, request, user_id):
        """Update an existing user record.
        """
        body = json.loads(request.body.decode("utf-8"))
        update_data = {
            "username": body.get('username'),
            "password": hash_password(body.get('password')) if body.get('password') else None,
            "roles": body.get('roles'),
            "profile_data": {
                "first_name": body.get('first_name'),
                "last_name": body.get('last_name'),
                "email": body.get('email')
            }
        }

        # Remove fields with None values (to prevent overwriting with None)
        update_data = {k: v for k, v in update_data.items() if v is not None}

        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        if result.matched_count == 0:
            return JsonResponse({"error": "User not found"}, status=404)
        return JsonResponse({"message": "User updated successfully"}, status=200)

    def delete(self, request, user_id):
        """Delete a user record.
        """
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return JsonResponse({"error": "User not found"}, status=404)
        return JsonResponse({"message": "User deleted successfully"}, status=200)
