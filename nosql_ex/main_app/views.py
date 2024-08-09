"""views.py

This module contains the view logic for the Django application. It handles incoming HTTP requests,
interacts with the data models, and returns HTTP responses. The views can be categorized into regular views 
and API views, where API views are designed for programmatic access to resources, typically in JSON format.
"""

from django.http import JsonResponse, HttpResponse
from django.views import View
from .serializers import MeteoriteSerializer
import json
from bson import ObjectId
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
    return HttpResponse("<h1>Hello and welcome to the <u>nosql_ex main_app!</u></h1>")
 
# API Views - API views are designed to handle programmatic access to resources. 
# They typically return data in formats like JSON, which is suitable for client-side applications or other services. 
# The View class provides a structure for defining HTTP methods (GET, POST, etc.) to manage requests and responses. 
# Compared to the sql_ex project that used Django REST Framework for ViewSets/APIView that handles permissions and serialization, 
# this project will require custom authentication methods which will utilize MongoDB users/roles via the 'auth_app' app. 
class MeteoriteLandingsApiView(View):
    """API View to handle meteorite landings data.
    
    GET: /api/meteorite_landings/ - Retrieves the first 10 meteorite landings.
    POST: /api/meteorite_landings/ - Creates a new meteorite landing.
    PUT: /api/meteorite_landings/<meteorite_id>/ - Updates a specific meteorite landing.
    DELETE: /api/meteorite_landings/<meteorite_id>/ - Deletes a specific meteorite landing.
    """

    def get(self, request):
        """Retrieve a list of meteorite landings.
        """
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        serialized_meteorite = [MeteoriteSerializer(meteorite) for meteorite in list_cur]
        return JsonResponse(serialized_meteorite, safe=False, json_dumps_params={'indent': 4})

    def post(self, request):
        """Create a new meteorite landing record.
        """
        body = json.loads(request.body.decode("utf-8"))
        newrecord = {
            "name": body.get('name'),
            "id": body.get('id'),
            "nametype": body.get('nametype'),
            "recclass": body.get('recclass'),
            "mass (g)": body.get('mass (g)'),
            "fall": body.get('fall'),
            "year": body.get('year'),
            "reclat": body.get('reclat'),
            "reclong": body.get('reclong'),
            "GeoLocation": body.get('GeoLocation')
        }
        result = collection.insert_one(newrecord)
        data = {"_id": str(result.inserted_id)}
        return JsonResponse(data, status=201)

    def put(self, request, meteorite_id):
        """Update an existing meteorite landing record.
        """
        body = json.loads(request.body.decode("utf-8"))
        update_data = {
            "name": body.get('name'),
            "id": body.get('id'),
            "nametype": body.get('nametype'),
            "recclass": body.get('recclass'),
            "mass (g)": body.get('mass (g)'),
            "fall": body.get('fall'),
            "year": body.get('year'),
            "reclat": body.get('reclat'),
            "reclong": body.get('reclong'),
            "GeoLocation": body.get('GeoLocation')
        }
        result = collection.update_one({"_id": ObjectId(meteorite_id)}, {"$set": update_data})
        if result.matched_count == 0:
            return JsonResponse({"error": "Record not found"}, status=404)
        return JsonResponse({"message": "Record updated successfully"}, status=200)

    def delete(self, request, meteorite_id):
        """Delete a meteorite landing record.
        """
        result = collection.delete_one({"_id": ObjectId(meteorite_id)})
        if result.deleted_count == 0:
            return JsonResponse({"error": "Record not found"}, status=404)
        return JsonResponse({"message": "Record deleted successfully"}, status=200)