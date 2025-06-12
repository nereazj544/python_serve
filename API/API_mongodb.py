from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)


# configuracion con la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ZOO']
collection = db['ANIMALES']


@app.route('/')
def home():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('nombre')
    species = request.form.get('especie')

    if name and species:
        collection.insert_one({
            'id': collection.count_documents({}) + 1,
            'nombre': name, 'especie': species})
        return jsonify({'status': 'success', 'message': '¡Elemento agregado exitosamente!'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400
    
@app.route('/delete', methods=['POST'])
def delete_item():
    try:
            item_id = int(request.form.get('id'))
            if not item_id:
                return jsonify({'status': 'error', 'message': '¡ID no válido!'}), 400
            
            item_id = int(item_id)
            result = collection.delete_one({'id': item_id})
            if result.deleted_count > 0:
                return jsonify({'status': 'success', 'message': '¡Elemento eliminado exitosamente!'})
            else:
                return jsonify({'status': 'error', 'message': '¡Elemento no encontrado!'}), 404
    except:
            return jsonify({'status': 'error', 'message': '¡Error al eliminar el elemento!'}), 500
        # Siempre refresca la página, puedes añadir mensajes con flash si lo deseas

if __name__ == '__main__':
    app.run(debug=True)
