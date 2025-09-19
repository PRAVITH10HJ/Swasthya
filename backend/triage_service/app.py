from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import pickle

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- CONFIGURATION ---
CLASSIFIER_PATH = 'symptom_classifier_model.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

# ... (the rest of your code is the same) ...

with open(CLASSIFIER_PATH, 'rb') as f:
    classifier = pickle.load(f)
with open(VECTORIZER_PATH, 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/triage', methods=['POST'])
def triage_symptoms():
    data = request.get_json()
    symptoms = data.get('symptoms')
    if not symptoms or not isinstance(symptoms, list):
        return jsonify({"error": "Missing or invalid 'symptoms' list"}), 400

    symptom_text = " ".join(symptoms)
    symptom_vector = vectorizer.transform([symptom_text])
    prediction = classifier.predict(symptom_vector)
    triage_level = prediction[0]

    recommendations = {
        "Emergency": "Seek immediate medical attention.",
        "Urgent": "Consult a healthcare provider within 24 hours.",
        "Routine": "Monitor symptoms and consult a doctor if they worsen."
    }
    recommendation = recommendations.get(triage_level, "Consult a healthcare professional.")

    return jsonify({
        "triage_result": triage_level,
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(port=5001)