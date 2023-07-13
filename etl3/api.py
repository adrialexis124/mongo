from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from bson import json_util
import requests
import json
from bson.objectid import ObjectId
from flask_cors import CORS
from time import sleep
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
    "mongodb://localhost:27047/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27048/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27049/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
]

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
    connection_strings = [
    "mongodb://localhost:27047/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27048/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27049/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    ]

    client = None

    for conn_str in connection_strings:
        try:
            temp_client = MongoClient(conn_str)
            if temp_client.is_primary:
                client = temp_client
                break
        except errors.ServerSelectionTimeoutError:
            pass

    db = client.test  # Nombre de la base de datos
    collection = db.test  # Nombre de la colección
    # Obtener los primeros 5 documentos
    data = list(collection.find().limit(10).sort("_id", -1))
    serialized_data = json_util.dumps(data)

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
    connection_strings = [
        "mongodb://localhost:27047/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
        "mongodb://localhost:27048/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
        "mongodb://localhost:27049/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    ]

    client = None

    for conn_str in connection_strings:
        try:
            temp_client = MongoClient(conn_str)
            if temp_client.is_primary:
                client = temp_client
                break
        except errors.ServerSelectionTimeoutError:
            pass
    todos=get_all_data()
    deserialized_data = json.loads(todos)
    db = client.test
    collection = db.test
    collection.delete_many({})
    #new_data = request.json
    result = collection.insert_many(deserialized_data)
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
    connection_strings = [
    "mongodb://localhost:27047/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27048/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    "mongodb://localhost:27049/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
    ]

    client2 = None

    for conn_str in connection_strings:
        try:
            temp_client = MongoClient(conn_str)
            if temp_client.is_primary:
                client2 = temp_client
                break
        except errors.ServerSelectionTimeoutError:
            pass

    db2 = client2.test
    destination_collection = db2.test

    # data_to_load = request.get_json(force=True)
    # Realiza las operaciones de carga en la base de datos de destino
    destination_collection.delete_many({})
    data_to_load = request.get_json(force=True)


    print(data_to_load)
    destination_collection.insert_many(data_to_load)

    return 201


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