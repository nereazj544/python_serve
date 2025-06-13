from flask import Flask, jsonify

app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return jsonify({'mensaje': '¡Hola, esta es una API simple en Python!'})

# Ruta para obtener un dato de ejemplo
@app.route('/dato')
def get_dato():
    return jsonify({'dato': 42})

if __name__ == '__main__':
    app.run(debug=True)
