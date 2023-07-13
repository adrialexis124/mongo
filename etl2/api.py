from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from bson import json_util
import requests
import json
from bson.objectid import ObjectId
from flask_cors import CORS
try:
    import carga
except:
    pass

app = Flask(__name__)
# Conexión a la base de datos MongoDB
#client = MongoClient("mongodb://localhost:27017,mongodb://localhost:27018,mongodb://localhost:27019/?replicaSet=iadbrs")
#
#client = MongoClient("mongodb://localhost:27018/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1")


connection_strings = [
    "mongodb://localhost:27037/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27038/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27039/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
] 

"""
connection_strings = [
    "mongodb://172.21.0.7:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://172.21.0.4:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://172.21.0.2:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
]
"""
client = None

for conn_str in connection_strings:
    try:
        temp_client = MongoClient(conn_str)
        if temp_client.is_primary:
            client = temp_client
            break
    except errors.ServerSelectionTimeoutError:
        pass


CORS(app)
# Ruta para obtener todos los documentos


@app.route('/api/data', methods=['GET'])
def get_all_data():
    db = client.test  # Nombre de la base de datos
    collection = db.test  # Nombre de la colección
    # Obtener los primeros 5 documentos
    data = list(collection.find().limit(10).sort("_id", -1))
    serialized_data = json_util.dumps(data)

    url = "http://127.0.0.1:5050//run-script"

    # Realiza la solicitud GET a la API
    response = requests.get(url)

    return serialized_data, 200
    # data = list(collection.find().limit(5))  # Obtener todos los documentos
    # return jsonify(data), 200

# Ruta para obtener un documento por su ID


@app.route('/api/data/<id>', methods=['GET'])
def get_data(id):
    db = client.test
    collection = db.test
    data = collection.find_one({'_id': ObjectId(id)})
    return jsonify({
      '_id': str(ObjectId(data['_id'])),
      'name': data['name'],
      'height': data['height'],
      'weight': data['weight'],
        'egg': data['egg']
  })

# Ruta para crear un nuevo documento


@app.route('/api/data', methods=['POST'])
def create_data():
    db = client.test
    collection = db.test
    new_data = request.json
    result = collection.insert_one(new_data)
    return str(result.inserted_id), 201

# Ruta para actualizar un documento existente


@app.route('/api/data/<id>', methods=['PUT'])
def update_data(id):
    db = client.test
    collection = db.test
    updated_data = request.json

    result = collection.update_one(
        {"_id": ObjectId(id)}, {'$set': updated_data})
    print(result)
    return jsonify({'message': 'User Updated'})

# Ruta para eliminar un documento por su ID


@app.route('/api/data/<id>', methods=['DELETE'])
def delete_data(id):
    db = client.test
    collection = db.test
    result = collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User Deleted'})


@app.route('/api/load', methods=['POST'])
def load_data():
    client2 = MongoClient("mongodb://172.21.0.3:27018")
    db2 = client2.destino
    destination_collection = db2.test

    # data_to_load = request.get_json(force=True)
    # Realiza las operaciones de carga en la base de datos de destino
    data_to_load = request.get_json(force=True)

    cleaned_data = []
    for item in data_to_load:
        try:
            item['_id'] = str(ObjectId())  # Convertir ObjectId a cadena
            cleaned_data.append(item)
        except json.JSONDecodeError as e:
            print(f"Error de formato JSON en el documento: {item}")
            continue

    print(data_to_load)

    # Realiza las operaciones de carga en la base de datos de destino
    for item in cleaned_data:
        destination_collection.insert_one(item)

    """ for item in data_to_load:
        transformed_item = carga.transform_data(item)
        transformed_data.append(transformed_item) """

    # Carga los datos en PostgreSQL
    carga.insert_data_mysql(cleaned_data)

    # Guarda los datos en un archivo CSV
    carga.save_data_csv(cleaned_data)

    # return 'Datos cargados en la base de datos de destino', 201
    return item, 201


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/')
def hello():
    return 'El servidor está en funcionamiento'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)