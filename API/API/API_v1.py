from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client['zoo3']
collection = db['animales']





app = Flask(__name__)

# TODO : ======= RUTAS DE LA APLICACION =======
@app.route('/')
def home(): # ? Ruta principa
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)


#TODO: AGREGAR UN ANIMAL
@app.route('/add', methods=['POST'])
def add_animal():
    nombre = request.form.get('nombre').capitalize()
    entorno = request.form.get('entorno').capitalize()
    tipo_reproduccion = request.form.get('tipo_reproduccion').capitalize()
    if nombre and entorno and tipo_reproduccion:
        collection.insert_one({
            'id': collection.count_documents({}) +1, # Genera un ID aumentando uno al anterior
            'nombre': nombre,
            'entorno': entorno,
            'tipo_reproduccion': tipo_reproduccion
        })        
        return jsonify({'status': 'succes', 'message': '¡Animal agregado exitosamente!'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400
    
#TODO: ELIMINAR UN ANIMAL
@app.route('/delete', methods=['POST'])
def delete_animal():
    try:
        item_id = int(request.form.get('id'))
        if not item_id:
            return jsonify({'status': 'error', 'message': '¡ERROR: ID NO VALIDO!'}), 400
        
        item_id = int(item_id)
        result = collection.delete_one({'id': item_id})
        if result.deleted_count > 0:
            return jsonify({'status': 'success', 'message': '¡ID ELIMINADO EXITOSAMENTE!'})
        else:
            return jsonify({'status': 'error', 'message': '¡ERROR: ID NO ENCONTRADO!'})
    except:
        return jsonify({'status': 'error', 'message': '¡ERROR AL ELIMINAR EL ELEMNTO!'})













if __name__ == '__main__':
    app.run(debug=True)