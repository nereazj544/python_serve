from flask import Flask, render_template, request, jsonify
from flasgger import Swagger # Swagger para documentacion de la API
from pymongo import MongoClient


# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client['ns']
collection = db['terminales']
collection_historial = db['history']
collection_tecnico = db['tecnicos']
collection_tec_inventario = db['inventario_tecnicos']

# TODO : ======= RUTAS DE LA APLICACION =======
app = Flask(__name__)
swagger = Swagger(app)  # Inicializar Swagger para la documentacion de la API

@app.route('/')
def home():
        """
        
        RUTA PARA MOSTRAR LOS ELEMENTOS QUE HAY EN LA BASE DE DATOS
        
        ---

        tags:
            - Terminales 

        parameters:
             - name: id
               type: number
               description: "Muestra el ID del terminal"
             - name: estado
               type: string
               description: "Muestra el estado del terminal (operativa, mantenimiento, inactiva)"
             - name: zona
               type: string
               description: "Muestra la zona del terminal"
             - name: modelo
               type: string
               description: "Muestra el modelo del terminal"
             - name: ubicacion
               type: string
               description: "Muestra la ubicación del terminal"
             - name: ubicacion_url
               type: string
               description: "Muestra la foto de la ubicacion del terminal"

        """
        items = list(collection.find())
        for item in items:
            item['_id'] = str(item['_id'])
        return render_template('index.html', items=items)
    






@app.route('/add', methods=['POST'])
def add():
    """
    RUTA PARA AÑADIR UN NUEVO TERMINAL
    ---
    tags:
        - Terminales 

    parameters:
        - name: nombre
          in: formData
          type: string
          required: true
          description: "Nombre del terminal"
        - name: zona
          in: formData
          type: string
          required: true
          description: "Zona del terminal"
        - name: estado
          in: formData
          type: string
          required: true
          description: "Estado del terminal (operativa, mantenimiento, inactiva)"
        - name: ubicacion
          in: formData
          type: string
          required: true
          description: "Ubicación del terminal"
        - name: ubicacion_url
          in: formData
          type: string
          required: true
          description: "URL de la ubicación del terminal"
        - name: modelo
          in: formData
          type: string
          required: true
          description: "Modelo del terminal"
    """

    nombre = request.form.get('nombre').capitalize()
    zona = request.form.get('zona').capitalize()
    estado = request.form.get('estado').capitalize()
    ubicacion = request.form.get('ubicacion').capitalize()
    ubicacion_url = request.form.get('ubicacion_url')
    modelo = request.form.get('modelo').capitalize()
    fecha_ins = request.form.get('fecha_instalacion')
    fecha_man = request.form.get('fecha_mantenimiento')
    ultima_rev = request.form.get('ultima_revision')
    fecha_rep = request.form.get('fecha_reporte')
    proxima_mantenimiento = request.form.get('proximo_mantenimiento')
    tecnico = request.form.get('tecnico').capitalize()

    if nombre and zona and estado and ubicacion and ubicacion_url and modelo and fecha_ins and fecha_man and ultima_rev and proxima_mantenimiento and tecnico:
        collection.insert_one({
            'id': collection.count_documents({}) + 1,
            "estado": estado,
            "zona": zona,
            "nombre": nombre,
            "ubicacion":ubicacion, 
            "ubicacion_url": ubicacion_url,
            "modelo": modelo,
            "fecha_instalacion": fecha_ins,
            "fecha_mantenimiento": fecha_man,
            "fecha_reporte": fecha_rep,
            "ultima_revision": ultima_rev,
            "proximo_mantenimiento": proxima_mantenimiento,
            "tecnico": tecnico
        })
        return jsonify({'status': 'succes', 'message': 'Terminal agregado exitosamente'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400


@app.route('/delete', methods=['POST'])
def delete():
    """
RUTA PARA ELIMINAR UN TERMINAL
---
tags:
    - Terminales 
parameters:
    - name: id
      in: formData
      type: integer
      required: true
      description: "ID del terminal a eliminar"
    """


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
    """
    RUTA PARA FILTRAR TERMINALES
    ---
    tags:
        - Terminales 
    parameters:
        - name: estado
          in: formData
          type: string
          required: true
          description: "Estado del terminal (operativa, mantenimiento, inactiva)"
    """
    valor = request.form.get('estado').capitalize()

    if valor:
        items = list(collection.find({'estado':valor}))
        for item in items:
            item['_id'] = str(item['_id'])
        return render_template ('index.html', items=items)
    else:
        return jsonify({'status': 'error', 'message': '¡ENTORNO NO VALIDO!'}), 400

@app.route('/update', methods=['POST'])
def update():
    """
    RUTA PARA ACTUALIZAR UN TERMINAL
    ---
    tags:
        - Terminales 
    parameters:
        - name: id
          in: formData
          type: integer
          required: true
          description: "ID del terminal a actualizar"
        - name: estado
          in: formData
          type: string
          description: "Nuevo estado del terminal (operativa, mantenimiento, inactiva)"
        - name: fecha_reporte
          in: formData
          type: string
          description: "Fecha del reporte de la terminal"
        - name: descripcion
          in: formData
          type: string
          description: "Descripción de la actualización"
    """


    try:
        item_id = request.form.get('id')
        if not item_id:
            return jsonify({'status': 'error', 'message': 'ID requerido'}), 400
        item_id = int(item_id)

        update_fields = {}
        if request.form.get('estado'):
            update_fields['estado'] = request.form.get('estado').capitalize()
        if request.form.get('fecha_reporte'):
            update_fields['fecha_reporte'] = request.form.get('fecha_reporte')

        if not update_fields:
            return jsonify({'status': 'error', 'message': 'No hay campos para actualizar'}), 400

        result = collection.update_one({'id': item_id}, {'$set': update_fields})

        # Historial
        descripcion = request.form.get('descripcion') or ''
        if descripcion or request.form.get('fecha_reporte'):
            entry = {
                'fecha': request.form.get('fecha_reporte') or '',
                'descripcion': descripcion or '-'
            }
            collection_historial.update_one(
                {'terminal_id': item_id},
                {'$push': {'reparaciones': entry}, '$setOnInsert': {'estado_actual': update_fields.get('estado',''), 'terminal_id': item_id}},
                upsert=True
            )

        if result.modified_count > 0:
            return jsonify({'status': 'success', 'message': 'Terminal actualizada correctamente'})
        else:
            return jsonify({'status': 'error', 'message': 'No se ha actualizado ningún campo (¿ID válido?)'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/historial/<int:item_id>')
def historial(item_id):
    """
    RUTA PARA MOSTRAR EL HISTORIAL DE UN TERMINAL ESPECIFICO

    ---

    tags:
        - Terminales 

    parameters:
         - name: item_id
           in: path
           type: integer
           required: true
           description: "ID del terminal para mostrar su historial"

    responses:
        200:
            description: "Historial del terminal"
        404:
            description: "Terminal no encontrado"
    """
   # Buscar datos de la terminal
    item = collection.find_one({'id': item_id})
    # Buscar el historial correspondiente
    historial = collection_historial.find_one({'terminal_id': item_id})
    # Convertir ObjectId a str si es necesario
    if item and '_id' in item:
        item['_id'] = str(item['_id'])
    if historial and '_id' in historial:
        historial['_id'] = str(historial['_id'])
    if not item:
        return jsonify({'status': 'error', 'message': '¡Terminal no encontrada!'}), 404
    # Renderizar la plantilla pasando ambos objetos
    return render_template('historial.html', item=item, historial=historial)




@app.route('/api/terminal_view')
def terminal_view():
    """
    RUTA PARA OBTENER TODOS LOS TERMINALES EN FORMATO JSON
    ---
    summary: "Obtener todos los terminales"
    tags:
        - Terminales 
    
                
    """
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)


@app.route('/tecnico')
def tecnico():
    """
    RUTA PARA MOSTRAR LOS TECNICOS
    ---
    summary: "Mostrar tecnicos"
    tags:
        - Tecnicos 
    """
    tecnicos = list(collection_tecnico.find())
    for tecnico in tecnicos:
        tecnico['_id'] = str(tecnico['_id'])
    return render_template('tecnico.html', tecnicos=tecnicos)

@app.route('/add_tecnico', methods=['POST'])
def add_tecnico():
    """
    RUTA PARA AÑADIR UN NUEVO TECNICO
    ---
    summary: "Añadir tecnico"
    tags:
        - Tecnicos
    parameters:
        - name: nombre
          in: formData
          type: string
          required: true
          description: "Nombre del tecnico"
        - name: zona
          in: formData
          type: string
          required: true
          description: "Zona del tecnico"
    """
    nombre = request.form.get('nombre').capitalize()
    zona = request.form.get('zona').capitalize()
    

    if nombre and zona:
        collection_tecnico.insert_one({
            'id': collection_tecnico.count_documents({}) + 1,
            'nombre': nombre,
            'zona': zona
        })
        return jsonify({'status': 'success', 'message': 'Tecnico agregado exitosamente'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400

@app.route('/delete_tecnico', methods=['POST'])
def delete_tecnico():
    """
    RUTA PARA ELIMINAR UN TECNICO
    ---
    summary: "Eliminar tecnico"
    tags:
        - Tecnicos
    parameters:
        - name: id
          in: formData
          type: integer
          required: true
          description: "ID del tecnico a eliminar"
    """
    try:
        item_id = int(request.form.get('id'))
        if not item_id:
            return jsonify({'status': 'error', 'message': '¡ERROR: ID NO VALIDO!'}), 400
        
        result = collection_tecnico.delete_one({'id': item_id})
        if result.deleted_count > 0:
            return jsonify({'status': 'success', 'message': '¡ID ELIMINADO EXITOSAMENTE!'})
        else:
            return jsonify({'status': 'error', 'message': '¡ERROR: ID NO ENCONTRADO!'})
    except:
        return jsonify({'status': 'error', 'message': '¡ERROR AL ELIMINAR EL ELEMENTO!'})

@app.route('/filter_tecnico', methods=['POST'])
def filter_tecnico():
    """
    RUTA PARA FILTRAR TECNICOS
    ---
    summary: "Filtrar tecnicos"
    tags:
        - Tecnicos
    parameters:
        - name: zona
          in: formData
          type: string
          required: true
          description: "Zona del tecnico"
    """
    valor = request.form.get('zona').capitalize()

    if valor:
        tecnicos = list(collection_tecnico.find({'zona': valor}))
        for tecnico in tecnicos:
            tecnico['_id'] = str(tecnico['_id'])
        return render_template('tecnico.html', tecnicos=tecnicos)
    else:
        return jsonify({'status': 'error', 'message': '¡ENTORNO NO VALIDO!'}), 400


@app.route('/api/tecnico_view')
def tecnico_view():
    """
    RUTA PARA OBTENER TODOS LOS TECNICOS EN FORMATO JSON
    ---
    summary: "Obtener todos los tecnicos"
    tags:
        - Tecnicos

    """
    items = list(collection_tecnico.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)


@app.route('/tecnico_view/<int:item_id>')
def inventario(item_id):
    """
    RUTA PARA MOSTRAR EL INVENTARIO DE UN TECNICO ESPECIFICO

    ---

    tags:
        - Tecnicos 

    parameters:
         - name: item_id
           in: path
           type: integer
           required: true
           description: "ID del terminal para mostrar su historial"

    responses:
        200:
            description: "Historial del terminal"
        404:
            description: "Terminal no encontrado"
    """
   # Buscar datos del tecnico
    item = collection_tecnico.find_one({'id': item_id})
    # Buscar el inventario correspondiente
    inventario = collection_tec_inventario.find_one({'tecnico_id': item_id})
    # Convertir ObjectId a str si es necesario
    if item and '_id' in item:
        item['_id'] = str(item['_id'])
    if inventario and '_id' in inventario:
        inventario['_id'] = str(inventario['_id'])
    if not item:
        return jsonify({'status': 'error', 'message': '¡Técnico no encontrado!'}), 404
    # Renderizar la plantilla pasando ambos objetos
    return render_template('tec_inventario.html', item=item, inventario=inventario)


@app.route('/update_tecnico', methods=['POST'])
def tecnico_update():
    """
    RUTA PARA ACTUALIZAR UN TECNICO
    ---
    tags:
        - Tecnicos
    """
    pass


if __name__ == '__main__':
    app.run(debug=True)
