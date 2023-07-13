from pymongo import MongoClient

# Conexión a la base de datos fuente
source_replica_set = 'my-replica-set'
source_nodes = 'host.docker.internal:27037,host.docker.internal:27038,host.docker.internal:27039'
source_client = MongoClient(f'mongodb://{source_nodes}/?replicaSet={source_replica_set}&appName=mongosh+1.10.1')
source_db = source_client['test']
source_collection = source_db['test']

# Conexión a la base de datos destino
target_replica_set = 'my-replica-set2'
target_nodes = 'host.docker.internal:27047,host.docker.internal:27048,host.docker.internal:27049' 
target_client = MongoClient(f'mongodb://{target_nodes}/?replicaSet={target_replica_set}&appName=mongosh+1.10.1')
target_db = target_client['test']
target_collection = target_db['test']

# Ejecuta el proceso ETL
documents = source_collection.find()
for doc in documents:
    # En este punto, podrías transformar los datos si es necesario
    # Por ejemplo: doc['campo'] = transformar(doc['campo'])
    target_collection.insert_one(doc)

# Verifica que los datos se copiaron correctamente
print(target_collection.count_documents({}))
