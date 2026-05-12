from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"message": "Hello from Flask inside Docker!"})

@app.route('/')
def hello():
    return "The Flask server is definitely working!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)