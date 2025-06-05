from pymongo import MongoClient


DB_MONGO = "MaxServer"
COLLECTION_MONGO_1 = "Personajes"
COLLECTION_MONGO_2 = "Juegos"
COLLECTION_MONGO_3 = "Empresa"

client = MongoClient("mongodb://localhost:27017/")


