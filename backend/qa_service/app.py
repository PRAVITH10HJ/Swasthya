from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Load Models and Data on Startup ---
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("faiss_index.bin")
with open("text_chunks.pkl", 'rb') as f:
    text_chunks = pickle.load(f)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    question_embedding = model.encode([question])
    _, indices = index.search(np.array(question_embedding).astype('float32'), 1)
    
    if indices.size > 0:
        answer = text_chunks[indices[0][0]]
    else:
        answer = "Sorry, I couldn't find a relevant answer in my knowledge base."
        
    return jsonify({"answer": answer, "source": "WHO / IFRC Knowledge Base"})

if __name__ == '__main__':
    app.run(port=5003)