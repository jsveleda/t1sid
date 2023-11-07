import redis
import random
import threading
from flask import Flask, request, jsonify
from data_generator import DataGenerator

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
  host='redis-11288.c308.sa-east-1-1.ec2.cloud.redislabs.com',
  port=11288,
  password='vVocxS1PGAx4Zlr8dVix8IyybHDqaCwt')

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Create
@app.route('/create/<key>/<value>', methods=['POST'])
def create(key, value):
    r.set(key, value)
    return jsonify({'message': 'Key-Value pair created successfully'})

# Read
@app.route('/read/<key>', methods=['GET'])
def read(key):
    value = r.get(key)
    if value is None:
        return jsonify({'error': 'Key not found'})
    return jsonify({key: value.decode('utf-8')})

# Update
@app.route('/update/<key>/<value>', methods=['PUT'])
def update(key, value):
    if r.exists(key):
        r.set(key, value)
        return jsonify({'message': 'Key-Value pair updated successfully'})
    else:
        return jsonify({'error': 'Key not found'})

# Delete
@app.route('/delete/<key>', methods=['DELETE'])
def delete(key):
    if r.exists(key):
        r.delete(key)
        return jsonify({'message': 'Key deleted successfully'})
    else:
        return jsonify({'error': 'Key not found'})
    
# List all keys
@app.route('/list_keys', methods=['GET'])
def list_keys():
    keys = [key.decode('utf-8') for key in r.keys('*')]
    key_value_pairs = {key: r.get(key).decode('utf-8') for key in keys}
    return jsonify(key_value_pairs)

# Calls generator to insert new data
@app.route('/insert_data')
def insert_data():
    data_gen = DataGenerator()
    data_gen.generate_data(100)
    
    for key, value in data_gen.data:
        r.set(key, value)
    
    return jsonify({'message': 'Data inserted successfully'})

# Function to create a thread for reading
def read_thread():
    key = f'key_{random.randint(0, 4999)}'
    value = r.get(key)
    if value is not None:
        return {key: value.decode('utf-8')}
    return {'error': 'Key not found'}

# Function to create a thread for writing
def write_thread():
    data_gen = DataGenerator()
    data_gen.generate_data(1)
    key, value = data_gen.data[0]
    r.set(key, value)
    return {'message': 'Key-Value pair created successfully'}

# Route to start the threads
@app.route('/start_threads', methods=['POST'])
def start_threads():
    num_threads = 100  # You can adjust this number as needed
    num_read_threads = 70  # Adjust the percentage of read threads as needed

    threads = []
    for _ in range(num_threads):
        if _ < num_read_threads:
            thread = threading.Thread(target=read_thread)
        else:
            thread = threading.Thread(target=write_thread)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify({'message': 'Threads executed'})


if __name__ == '__main__':
    app.run(debug = True)