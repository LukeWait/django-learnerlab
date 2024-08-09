"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

from django.http import JsonResponse, HttpResponse
from django.views import View
from .serializers import UserSerializer
import pymongo

# use pymongo to connect to db
client = pymongo.MongoClient('mongodb+srv://lukewait:Passw0rd1!@djangolab-cluster.y0zsa4f.mongodb.net/')
dbname = client['nasa_data_db']
collection = dbname['users']

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
class UserLoginApiView(View):
    def get(self, request):
        """Retrieve a list of users.
        """
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        serialized_users = [UserSerializer(user) for user in list_cur]
        return JsonResponse(serialized_users, safe=False)
