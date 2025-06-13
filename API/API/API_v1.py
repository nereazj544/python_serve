from flask import Flask, jsonify, request, render_template

from pymongo import MongoClient

# TODO: ======= CONFIGURACION DE LA BASE DE DATOS =======
client = MongoClient('mongodb://localhost:27017/')
db = client




app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')






if __name__ == '__main__':
    app.run(debug=True)