from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
from bson.json_util import dumps

# use pymongo to connect to db
import pymongo
client = pymongo.MongoClient('mongodb+srv://lukewait:tafenosql@cluster1.syijvpg.mongodb.net/test')
# define db name
dbname = client['meteorite_landings_db']
# define collection
collection = dbname['meteorite_landings']

# create views here.
def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

'''
# example record
meteorite_1 = {
	"name": "Apophis",
	"year": "2029"
}

# to POST a record
# collection.insert_one(meteorite_1)

# to DELETE a record
# collection.delete_one(meteorite_1)


# stores all documents in collection
meteorite_details = collection.find({})
# outputs all documents in collection to terminal
for i in meteorite_details:
	print(str(i['name']))
'''

def TheModelView(request):
    if(request.method == "GET"):
        cursor = collection.find().limit(10)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJsON data", json_data)
        return JsonResponse(json_data, safe=False)
    
    if(request.method == "POST"):
        body = json.loads(request.body.decode("utf-8"))
        newrecord = {
			"name": body['name'],
			"year": body['year']
		}
        result = collection.insert_one(newrecord)
        data = {"_id": str(result.inserted_id)}
        return JsonResponse(dumps(data), safe=False)
