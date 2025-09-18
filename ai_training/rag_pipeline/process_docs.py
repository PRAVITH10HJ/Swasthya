import os
import faiss
from sentence_transformers import SentenceTransformer
# from PyPDF2 import PdfReader
import numpy as np

# 1. Load and Chunk PDFs
print("Loading documents...")
text_chunks = []
pdf_folder_path = '../../backend/qa_service/knowledge_base/'
# ... (Add logic to loop through PDFs in the folder)
# reader = PdfReader(pdf_path)
# for page in reader.pages:
#     text_chunks.append(page.extract_text())

# 2. Load the Sentence Transformer Model
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2') # A good, fast model

# 3. Encode the Chunks into Embeddings
print("Encoding documents...")
embeddings = model.encode(text_chunks, show_progress_bar=True)

# 4. Build a FAISS Index
print("Building FAISS index...")
embedding_dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dimension)
index.add(np.array(embeddings).astype('float32'))

# 5. Save the Index
output_path = '../../backend/qa_service/faiss_index.bin'
faiss.write_index(index, output_path)
print(f"Index successfully built and saved to {output_path}")