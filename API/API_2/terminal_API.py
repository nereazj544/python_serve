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
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)
    






















if __name__ == '__main__':
    app.run(debug=True)
