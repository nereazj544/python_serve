from pymongo import MongoClient

db_name = "test_python_db"
collection_1 = "empresas"
collection_2 = "personajes"


def insetar():

    data = input("1. Empresa\n2. Personaje\nSeleccione una opción (numero): ")
    if data == "1":
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[collection_1]
        print("Insertar un nuevo registro en la colección 'empresa'")
        nombre = input("Ingrese el nombre de la empresa: ")

        data = {
                "id" : collection.count_documents({}) + 1,
                "nombre" : nombre
            }
        data = collection.insert_one(data)
    elif data == "2":
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[collection_2]
        print("Insertar un nuevo registro en la colección 'personaje'")
        nombre = input("Ingrese el nombre del personaje: ")
        juego = input("Ingrese el juego del personaje: ")
        num_empresa = input("Ingrese el id de la empresa: ")
        data = {
                "id" : collection.count_documents({}) + 1,
                "nombre" : nombre,
                "juego" : juego,
                "empresa_id" : int(num_empresa)
            }
    else:
        print("Opción no válida.")
        return

    
    

def buscar():
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_1]

    

def main():
    print("1. Insertar")
    print("2. Buscar")

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        insetar()
    elif opcion == "2":
        buscar()
    else:
        print("Opción no válida.")


main()