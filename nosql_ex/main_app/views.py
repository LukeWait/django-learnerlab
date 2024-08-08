"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
import json
from bson.json_util import dumps
import pymongo

# use pymongo to connect to db
client = pymongo.MongoClient('mongodb+srv://lukewait:Passw0rd1!@djangolab-cluster.y0zsa4f.mongodb.net/')
dbname = client['nasa_data_db']
collection = dbname['meteorite_landings']

# Regular views - Regular views in Django respond to HTTP requests by returning HTML content. 
# They can utilize the 'render' function, which points to a given template (like 'index.html') with context data to 
# produce a complete HTML response. Alternatively, views can directly return a 'HttpResponse' object for simpler responses.
def index(request):
    """This function returns a simple HttpResponse.
    """
    return HttpResponse("<h1>Hello and welcome to the <u>nosql_ex</u> front end!</h1>")
 
# API Views - API views in Django, particularly when using the Django REST Framework, are designed
# to handle programmatic access to resources. They typically return data in formats like 
# JSON, which is suitable for client-side applications or other services. 
# The APIView class provides a structure for defining HTTP methods (GET, POST, etc.) to manage requests and responses. 
# It allows you to handle authentication, permissions, and data serialization, assisting in adhereing to REST principles.  
class MeteoriteLandingsApiView(APIView):
    """API View to handle meteorite landings data.
    
    example record
    meteorite_1 = {
        "name": "Apophis",
        "year": "2029"
    }

    to DELETE a record
    collection.delete_one(meteorite_1)

    stores all documents in collection
    meteorite_details = collection.find({})

    outputs all documents in collection to terminal
    for i in meteorite_details:
        print(str(i['name']))
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve a list of meteorite landings.
        """
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        return JsonResponse(json_data, safe=False)

    def post(self, request):
        """Create a new meteorite landing record.
        """
        body = json.loads(request.body.decode("utf-8"))
        newrecord = {
            "name": body['name'],
            "year": body['year']
        }
        result = collection.insert_one(newrecord)
        data = {"_id": str(result.inserted_id)}
        return JsonResponse(dumps(data), safe=False)