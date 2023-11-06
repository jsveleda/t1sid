import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
  host='redis-10262.c308.sa-east-1-1.ec2.cloud.redislabs.com',
  port=10262,
  password='FUlfPwDTMifoCObmsNgd24zCNWAzwWEo')

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

if __name__ == '__main__':
    app.run(debug=True)