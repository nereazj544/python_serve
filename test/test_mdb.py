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


data ={
    "id": 1,
    "nombre": "Link",
    "Elemento": "Varios",
    "Genero": "Masculino",
    "Arma": 'Espada Maestra',
    "Faccion": "Hyrule",
    "juego_id": 4
}

collection_personajes.insert_one(data)