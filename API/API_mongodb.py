import flask 
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)


# configuracion con la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ZOO']
collection = db['animales']


@app.route('/')
def home():
    items = list(collection.find())
    for item in items:
        item['_id'] = str(item['_id'])
    return render_template('index.html', items=items)



if __name__ == '__main__':
    app.run(debug=True)
