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
import pymongo

# use pymongo to connect to db
client = pymongo.MongoClient('mongodb+srv://<user>:<password>!@djangolab-cluster.y0zsa4f.mongodb.net/')
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
    """This view handles HTTP requests for managing meteorite landings data.

    It provides CRUD (Create, Read, Update, Delete) operations for meteorite landing entries 
    in the database. Additionally, it supports filtering and sorting of results by accepting 
    query parameters in the URL. All operations return JSON responses.

    Methods:
        - get: (GET) Retrieve a list of meteorite landings, with optional filtering and sorting.
        - post: (POST) Create a new meteorite landing record.
        - put: (PUT) Update an existing meteorite landing record by its ID.
        - delete: (DELETE) Delete a meteorite landing record by its ID.

    Parameters:
        The expected input for post and put actions is in JSON format:
        {
            "name": "Aachen",                  # Expects a string with the meteorite's name.
            "id": 1,                           # Expects an integer ID for the meteorite.
            "nametype": "Valid",               # Expects a string representing the name type.
            "recclass": "L5",                  # Expects a string indicating the classification.
            "mass (g)": 21,                    # Expects a string representing the mass in grams.
            "fall": "Fell",                    # Expects a string indicating whether the meteorite fell or was found.
            "year": 1880,                      # Expects an integer representing the year of the meteorite landing.
            "reclat": 50.775,                  # Expects a double representing the latitude.
            "reclong": 6.0833,                 # Expects a double representing the longitude.
            "GeoLocation": "(50.775, 6.0833)"  # Expects a string representing the geographic location.
        }

    Returns:
        - get: A JSON response with a list of serialized meteorite landing instances (limited to 10 results). 
        - post: A JSON response with the ID of the newly created meteorite landing instance. 
        - put: A JSON response indicating success or failure. Status 200 if the record was updated, 
        - delete: A JSON response indicating success or failure. Status 200 if the record was deleted, 

    Filtering and Sorting:
        - `name`: Used to filter meteorite landings by an exact name match. Example: `/api/meteorite_landings/?name=Aachen`
        - `year`: Used to filter meteorite landings by the year of occurrence. Example: `/api/meteorite_landings/?year=1880`
        - `sort`: Specifies the field to sort the results by. Default is 'name'. Example: `/api/meteorite_landings/?sort=year`
        - `order`: Specifies the sort order, either 'asc' for ascending or 'desc' for descending. Default is 'asc'. 
          Example: `/api/meteorite_landings/?sort=year&order=desc`

        You can combine multiple query parameters in a single URL. For instance: 
        `/api/meteorite_landings/?name=Aachen&year=1880&sort=year&order=desc`
    """
    def get(self, request):
        """Retrieve a list of meteorite landings with optional filtering and sorting.
        """
        # Get query parameters for filtering and sorting
        filter_params = {}
        if 'name' in request.GET:
            filter_params['name'] = request.GET['name']
        if 'year' in request.GET:
            filter_params['year'] = int(request.GET['year'])  # Assuming year is an integer

        # Get sort parameter (default to sorting by 'name' if not provided)
        sort_param = request.GET.get('sort', 'name')
        sort_order = request.GET.get('order', 'asc')
        sort_order = 1 if sort_order == 'asc' else -1

        # Find and sort the documents
        cursor = collection.find(filter_params).sort(sort_param, sort_order).limit(10)
        list_cur = list(cursor)

        # Serialize the data
        serialized_meteorite = [MeteoriteSerializer(meteorite) for meteorite in list_cur]
        return JsonResponse(serialized_meteorite, safe=False)

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