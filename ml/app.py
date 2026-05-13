import os 
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

DB_URL = os.getenv('DATABASE_URL')
engine = create_engine(DB_URL)

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