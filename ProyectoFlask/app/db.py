from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Colecciones
platos = db["platos"]
menus = db["menus"]
pedidos = db["pedidos"]