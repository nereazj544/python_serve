from flask import Flask, render_template, request, jsonify
from flasgger import Swagger # Swagger para documentacion de la API
from pymongo import MongoClient


# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client['ns']
collection = db['terminales']

app = Flask(__name__)
swagger = Swagger(app)  # Inicializar Swagger para la documentacion de la API

@app.route('/')
def home():
        """
        
        RUTA PARA MOSTRAR LOS ELEMENTOS QUE HAY EN LA BASE DE DATOS
        
        ---

        tags:
            - Terminales View

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
    valor = request.form.get('estado').capitalize()

    if valor:
        items = list(collection.find({'estado':valor}))
        for item in items:
            item['_id'] = str(item['_id'])
        return render_template ('index.html', items=items)
    else:
        return jsonify({'status': 'error', 'message': '¡ENTORNO NO VALIDO!'}), 400






@app.route('/api/terminal_view')
def terminal_view():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)






if __name__ == '__main__':
    app.run(debug=True)
