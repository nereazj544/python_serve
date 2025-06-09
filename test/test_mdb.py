from pymongo import MongoClient


DB_MONGO = "MaxServer"
COLLECTION_MONGO_1 = "Personajes"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Empresa"

client = MongoClient("mongodb://localhost:27017/")


db = client[DB_MONGO]
collection_personajes = db[COLLECTION_MONGO_2]


r = collection_personajes.find()
for document in r:
    print(f"ID: {document['id']} - Nombre: {document['nombre']}")