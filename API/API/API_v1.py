from flask import Flask, render_template, request, jsonify

from flasgger import Swagger # Swagger para documentacion de la API


from pymongo import MongoClient

# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client['zoo3']
collection = db['animales']

app = Flask(__name__)
swagger = Swagger(app)  # Inicializar Swagger para la documentacion de la API


# TODO : ======= RUTAS DE LA APLICACION =======
@app.route('/')
def home(): # ? Ruta principa
    """
    Ruta principal donde se muestran todos los datos de la base de datos: MongoDB
    ---
    parameters:
        - name: id
          type: number
          description: "Muestra el ID del animal"
        - name: entorno
          type: string
          description: "Muestra el tipo de entorno (terrestre, acuático, aéreo)"
        - name: tipo_reproduccion
          type: string
          description: "Muestra el tipo de reproducción (ovíparo, mamífero)"

    responses:
        200:
            description: "Lista de animales"
        500:
            description: "Error al obtener los datos de la base de datos"
    tags:
        - Animales
    summary: "Obtener todos los animales"
    description: "Esta ruta obtiene todos los animales de la base de datos."
    produces:
        - application/json
    
    
    


    """

    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)


#TODO: AGREGAR UN ANIMAL
@app.route('/add', methods=['POST'])
def add_animal():

    """
    Ruta para agregar un nuevo animal a la base de datos
    ---
    tags:
        - Animales
    
    parameters:
        - name: nombre
          in: formData
          type: string
          required: true
          description: "Nombre del animal"
        - name: entorno
          in: formData
          type: string
          required: true
          description: "Entorno del animal (terrestre, acuático, aéreo)"
        - name: tipo_reproduccion
          in: formData
          type: string
          required: true
          description: "Tipo de reproducción del animal (ovíparo, mamífero)"
        - name: habitat
          in: formData
          type: string
          required: false
          description: "Hábitat del animal"
        - name: velocidad
          in: formData
          type: string
          required: false
          description: "Velocidad del animal"
        - name: alimentacion
          in: formData
          type: string
          required: false
          description: "Tipo de alimentación del animal"
        - name: informacion_basica
          in: formData
          type: string
          required: false
          description: "Información básica sobre el animal"
        - name: img_url
          in: formData
          type: string
          required: false
          description: "URL de la imagen del animal"

    
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

@app.route('/filter', methods=['POST'])
def filter_items():
    valor = request.form.get('entorno').capitalize()
    if valor:
        items = list(collection.find({"$or":[{'entorno': valor},{'tipo_reproduccion': valor}]}))
        for item in items:
            item['_id'] = str(item['_id'])
        return render_template('index.html', items=items)
    else:
        return jsonify({'status': 'error', 'message': '¡ENTORNO NO VALIDO!'}), 400


@app.route('/ficha/<int:item_id>')
def ficha(item_id):
    item = collection.find_one({'id': item_id})
    if not item:
        return jsonify({'status': 'error', 'message': '¡ID NO ENCONTRADO!'}), 404
    item['_id'] = str(item['_id'])
    result = collection.find_one({'id': item_id})
    if not result:
        return jsonify({'status': 'error', 'message': '¡ID NO ENCONTRADO!'}), 404
    return render_template('ficha.html', item=result)





# TODO: == VIEW API ==
@app.route('/api/animal_view')
def animal_view():
    """
    Ejemplo de respuesta:
    ---
    tags:
    - View API
    summary: "Obtener todos los animales en formato JSON"
    responses:
      200:
        description: Lista de animales en formato JSON
        examples:
          application/json: |
            [
              {
                "id": 1, 
                "nombre": "Leon", 
                "informacion_basica": "El leon es conocido como el rey de la selva, vive en manadas y es uno de los grandes depredadores de Africa", 
                "entorno": "Terreste", 
                "tipo_reproduccion": "Mamifero",
                "habitat": "Sabana africana", 
                "velocidad": "80 km/h", 
                "alimentacion": "Carnivoro", 
                "img_url": "https://images.pexels.com/photos/1912176/pexels-photo-1912176.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", 
                "galeria": ["https://images.pexels.com/photos/32551859/pexels-photo-32551859.jpeg",
                "https://images.pexels.com/photos/68421/pexels-photo-68421.jpeg","https://images.pexels.com/photos/40803/lion-animal-predator-big-cat-40803.jpeg","https://images.pexels.com/photos/107506/pexels-photo-107506.jpeg","https://images.pexels.com/photos/162206/lioness-animal-predator-cat-162206.jpeg"]},
            ]
    """
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)



if __name__ == '__main__':
    app.run(debug=True)