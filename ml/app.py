import os 
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

DB_URL = os.getenv('DATABASE_URL')
engine = create_engine(DB_URL)
MODEL_PATH = 'bed.pkl'

def preprocess_data(df):
    df['has_oxygen'] = df['has_oxygen'].astype(int)
    df['has_ventilator'] = df['has_ventilator'].astype(int)
    df['has_monitor'] = df['has_monitor'].astype(int)
    df['target'] = df['status'].apply(lambda x : 1 if x== 'occupied' else 0)
    return df

@app.route('/train', methods=['POST'])
def train_model():
    try:
        query = "SELECT status, has_oxygen, has_ventilator, has_monitor, daily_rate_bdt FROM public.beds"
        df = pd.read_sql(query, engine)
        df = preprocess_data(df)
        
        X = df[['has_oxygen', 'has_ventilator', 'has_monitor', 'daily_rate_bdt']]
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        joblib.dump(model, MODEL_PATH)
        
        return jsonify({"status":"success", "message":"Model trained and saved."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/predict-occupancy', methods=['POST'])
def predict():
    try:
        if not os.path.exists(MODEL_PATH):
            return jsonify({"error": "Model not trained yet"}), 400
        
        model = joblib.load(MODEL_PATH)
        input_data = request.json 
        
        features = pd.DataFrame([input_data])[['has_oxygen', 'has_ventilator', 'has_monitor', 'daily_rate_bdt']]
        prediction = model.predict(features)
        probability = model.predict_proba(features)
        
        return jsonify({
            "is_occupied_prediction": int(prediction[0]),
            "occupancy_probability": float(probability[0][1])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/fetch-beds', methods=['GET'])
def fetch_beds():
    try:
        query = "SELECT id, tenant_id, ward_id, bed_number, status, has_oxygen, has_ventilator, has_monitor, daily_rate_bdt, current_patient_id, admission_date, expected_discharge_date, created_at, updated_at FROM public.beds"
        df = pd.read_sql(query, engine)
        
        df['current_patient_id'] = df['current_patient_id'].where(df['current_patient_id'].notnull(), None)
        df['admission_date'] = pd.to_datetime(df['admission_date'])
        df['admission_date'] = df['admission_date'].dt.strftime('%Y-%m-%d').where(df['admission_date'].notnull(), None)   
        df['expected_discharge_date'] = pd.to_datetime(df['expected_discharge_date'])
        df['expected_discharge_date'] = df['expected_discharge_date'].dt.strftime('%Y-%m-%d').where(df['expected_discharge_date'].notnull(), None)
        if 'meta' in df.columns: 
            df['meta'] = df['meta'].where(df['meta'].notnull(), None)
        
        data = df.to_dict(orient='records')

        return jsonify({
            "status":"success",
            "count": len(df),
            "data":data
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"message": "Hello from Flask inside Docker!"})

@app.route('/')
def hello():
    return "The Flask server is definitely working!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)