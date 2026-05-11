from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/ml/test')
def api():
    return jsonify({"message": "Hello from Flask inside Docker!"})

@app.route('/')
def hello():
    return "The Flask server is definitely working!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)