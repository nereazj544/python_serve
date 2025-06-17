from flask import Flask, render_template, request, jsonify
from flasgger import Swagger

from pymongo import MongoClient

# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client['zoo3']
collection = db['animales']


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def home(): # ? Ruta principa
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_animal():
    """
    Agregar un nuevo animal a la base de datos.
    ---
    parameters:
      - name: nombre
        in: formData
        type: string
        required: true
        description: Nombre del animal.
      - name: entorno
        in: formData
        type: string
        required: true
        description: Entorno del animal.
      - name: tipo_reproduccion
        in: formData
        type: string
        required: true
        description: Tipo de reproduccion del animal.
      - name: habitat
        in: formData
        type: string
        required: true
        description: Habitat del animal.
      - name: velocidad
        in: formData
        type: string
        required: false
        description: Velocidad del animal.
      - name: alimentacion
        in: formData
        type: string
        required: false
        description: Alimentacion del animal.
      - name: informacion_basica
        in: formData
        type: string
        required: false
        description: Informacion basica del animal.
      - name: img_url
        in: formData
        type: string
        required: false
        description: URL de la imagen del animal.
    """
    nombre = request.form.get('nombre').capitalize()
    entorno = request.form.get('entorno').capitalize()
    tipo_reproduccion = request.form.get('tipo_reproduccion').capitalize()
    habitat = request.form.get('habitat').capitalize()
    velocidad = request.form.get('velocidad')
    alimentacio = request.form.get('alimentacion').capitalize()
    habitat = request.form.get('habitat').capitalize()
    informacion_basica = request.form.get('informacion_basica')

    img_url = request.form.get('img_url')
    if nombre and entorno and tipo_reproduccion:
        collection.insert_one({
            'id': collection.count_documents({}) +1, # Genera un ID aumentando uno al anterior
            'nombre': nombre,
            'entorno': entorno,
            'tipo_reproduccion': tipo_reproduccion,
            'habitat': habitat,
            'velocidad': velocidad,
            'alimentacion': alimentacio,
            'informacion_basica': informacion_basica,
            'img_url': img_url
        })        
        return jsonify({'status': 'succes', 'message': '¡Animal agregado exitosamente!'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400
  

if __name__ == '__main__':
    app.run(debug=True)