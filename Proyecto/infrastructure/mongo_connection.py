import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGO_URI)
db = client.get_default_database() if client.get_default_database().name else client['restaurante_db']

def get_db():
    return db
