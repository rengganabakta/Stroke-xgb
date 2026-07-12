from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import pandas as pd
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# Load model bundle
MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgb_stroke_model.pkl")

bundle = None
model = None
best_threshold = None
feature_names = None

def load_model():
    global bundle, model, best_threshold, feature_names
    with open(MODEL_PATH, "rb") as f:
        bundle = pickle.load(f)
    model = bundle["model"]
    best_threshold = bundle["best_threshold"]
    feature_names = bundle["feature_names"]
    print(f"[INFO] Model loaded. Threshold: {best_threshold}")
    print(f"[INFO] Feature names: {feature_names}")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Map nilai dari frontend ke encoding model
        gender_map = {"Laki-Laki": 1.0, "Perempuan": 0.0}
        married_map = {"Menikah": 1.0, "Belum menikah": 0.0}
        work_map = {
            "Anak-Anak": 0.0,
            "Belum pernah bekerja": 1.0,
            "PNS": 2.0,
            "Swasta": 3.0,
            "Wiraswasta/Pekerja mandiri": 4.0
        }
        residence_map = {"Perkotaan": 1.0, "Perdesaan": 0.0}
        smoking_map = {
            "Tidak merokok": 0.0,
            "Mantan Merokok": 1.0,
            "Perokok aktif": 2.0
        }

        new_data = pd.DataFrame({
            'gender': [gender_map[data['gender']]],
            'age': [float(data['age'])],
            'hypertension': [1 if data['hypertension'] == 'Iya' else 0],
            'heart_disease': [1 if data['heart_disease'] == 'Iya' else 0],
            'ever_married': [married_map[data['ever_married']]],
            'work_type': [work_map[data['work_type']]],
            'Residence_type': [residence_map[data['residence_type']]],
            'avg_glucose_level': [float(data['avg_glucose_level'])],
            'bmi': [float(data['bmi'])],
            'smoking_status': [smoking_map[data['smoking_status']]]
        })[feature_names]

        prob_stroke = model.predict_proba(new_data)[0][1]
        prediction = int(prob_stroke >= best_threshold)

        return jsonify({
            "prediction": "STROKE" if prediction == 1 else "TIDAK STROKE",
            "probability": round(prob_stroke * 100, 2),
            "threshold": round(best_threshold * 100, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    load_model()
    app.run(debug=True, port=5000)
