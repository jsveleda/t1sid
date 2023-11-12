import redis
from flask import Flask, request, jsonify
from data_generator import DataGenerator

app = Flask(__name__)

# Connect to Redis
POOL = redis.ConnectionPool(
  host='redis-19973.c308.sa-east-1-1.ec2.cloud.redislabs.com',
  port=19973,
  password='a5RhKG6KysXOokImNYGnuhsCRSxAZXUI')
r = redis.StrictRedis(connection_pool=POOL)

from flask import Flask
import time

app = Flask(__name__)

# Função de wrapper para medir o tempo de execução
def measure_execution_time(route_function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = route_function(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Tempo de execução de {route_function.__name__}: {execution_time} segundos")
        return result
    wrapper.__name__ = f"{route_function.__name__}_wrapper"
    return wrapper


@app.route('/')
@measure_execution_time
def hello_world():
    return 'Hello, World!'

# Create
@app.route('/create/<key>/<value>', methods=['POST'])
@measure_execution_time
def create(key, value):
    r.set(key, value)
    return jsonify({'message': 'Key-Value pair created successfully'})

# Read
@app.route('/read/<key>', methods=['GET'])
@measure_execution_time
def read(key):
    value = r.get(key)
    if value is None:
        return jsonify({'error': 'Key not found'})
    return jsonify({key: value.decode('utf-8')})

# Update
@app.route('/update/<key>/<value>', methods=['PUT'])
@measure_execution_time
def update(key, value):
    if r.exists(key):
        r.set(key, value)
        return jsonify({'message': 'Key-Value pair updated successfully'})
    else:
        return jsonify({'error': 'Key not found'})

# Delete
@app.route('/delete/<key>', methods=['DELETE'])
@measure_execution_time
def delete(key):
    if r.exists(key):
        r.delete(key)
        return jsonify({'message': 'Key deleted successfully'})
    else:
        return jsonify({'error': 'Key not found'})
    
# List all keys
@app.route('/list_keys', methods=['GET'])
@measure_execution_time
def list_keys():
    keys = [key.decode('utf-8') for key in r.keys('*')]
    key_value_pairs = {key: r.get(key).decode('utf-8') for key in keys}
    return jsonify(key_value_pairs)

# Calls generator to insert new data
@app.route('/insert_data')
@measure_execution_time
def insert_data():
    data_gen = DataGenerator()
    data_gen.generate_data(5000)
    
    for key, value in data_gen.data:
        r.set(key, value)
    
    return jsonify({'message': 'Data inserted successfully'})

if __name__ == '__main__':
    app.run(debug = True)