import faiss
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import numpy as np
import os
import pickle

# --- CONFIGURATION ---
KNOWLEDGE_BASE_PATH = '../../backend/qa_service/knowledge_base/'
INDEX_OUTPUT_PATH = '../../backend/qa_service/faiss_index.bin'
TEXT_CHUNKS_OUTPUT_PATH = '../../backend/qa_service/text_chunks.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'

# 1. Load and Chunk PDFs
print("Loading documents from:", KNOWLEDGE_BASE_PATH)
text_chunks = []
for filename in os.listdir(KNOWLEDGE_BASE_PATH):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(KNOWLEDGE_BASE_PATH, filename)
        print(f"Processing {filename}...")
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_chunks.append(text)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if not text_chunks:
    print("Error: No text was extracted from the PDFs.")
    exit()
print(f"Loaded {len(text_chunks)} pages.")

# 2. Load the Model, Encode, and Build Index
print(f"Loading model '{MODEL_NAME}'...")
model = SentenceTransformer(MODEL_NAME)
print("Encoding documents...")
embeddings = model.encode(text_chunks, show_progress_bar=True)
print("Building FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

# 3. Save the Index and Text Chunks
print(f"Saving FAISS index to {INDEX_OUTPUT_PATH}")
faiss.write_index(index, INDEX_OUTPUT_PATH)
print(f"Saving text chunks to {TEXT_CHUNKS_OUTPUT_PATH}")
with open(TEXT_CHUNKS_OUTPUT_PATH, 'wb') as f:
    pickle.dump(text_chunks, f)

print("\nPipeline complete.")