from flask import Flask, render_template, request, jsonify
import mysql.connector


HOST = 'localhost'
DATABASE = 'ZOO'
PASS = '321_ytrewq'
USER = 'api_python'



def get_MySQL_conn():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASS,
        database=DATABASE
    )


app = Flask(__name__)

@app.route('/')
def home():
    items = "select * from ANIMALES"
    conn = get_MySQL_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(items)
    results = cursor.fetchall()
    return render_template('index.html', items=results)

@app.route('/add', methods=['POST'])
def add_item():
    nombre = request.form.get('nombre').capitalize()
    especie = request.form.get('especie').capitalize()
    

    if nombre and especie:
        conn = get_MySQL_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ANIMALES (nombre, especie) VALUES (%s, %s)", (nombre, especie))
        conn.commit()
        return jsonify({'status': 'success', 'message': '¡Elemento agregado exitosamente!'})
    else:
        return jsonify({'status': 'error', 'message': '¡Todos los campos son obligatorios!'}), 400


@app.route('/delete', methods=['POST'])
def delete_item(): 
    try:
        item_id = int(request.form.get('id'))
        if not item_id:
            return jsonify({'status': 'error', 'message': '¡ID no válido!'}), 400
        conn = get_MySQL_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ANIMALES WHERE id = %s", (item_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'status': 'success', 'message': '¡Elemento eliminado exitosamente!'})
        else:
            return jsonify({'status': 'error', 'message': '¡Elemento no encontrado!'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'¡Error al eliminar el elemento! {str(e)}'}), 500

@app.route('/filter', methods=['POST'])
def filter_items():
    especie = request.form.get('especie').capitalize()
    if especie:
        conn = get_MySQL_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ANIMALES WHERE especie = %s", (especie,))
        results = cursor.fetchall()
        return render_template('index.html', items=results)
    else:
        return jsonify({'status': 'error', 'message': '¡Especie no válida!'}), 400



if __name__ == '__main__':
    app.run(debug=True)
