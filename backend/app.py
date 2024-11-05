import numpy as np
import faiss
import os
import json
from flask import Flask, request, jsonify
import pdfplumber
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from config import REDIS_HOST, REDIS_PORT, REDIS_DB
import redis

app = Flask(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Define global variables
document_sections = None
output_index = None

def search(query, k=3, document_sections=None, index=None):
    query_embedding = model.encode([query]).astype('float32')
    _, indices = index.search(query_embedding, k)
    return [document_sections[idx] for idx in indices[0]]

def pipeline1(query, k=3, document_sections=None, index=None):
    answers = []
    for section in search(query, k, document_sections, index):
        result = qa_pipeline(question=query, context=section)
        answers.append(result['answer'])
    return ''.join(answers)

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        document_sections = []
        for page in pdf.pages:
            text = page.extract_text()
            text_segments = text.split("\n\n")
            for text in text_segments:
                if len(text) > 0:
                    document_sections.append(text)
    return document_sections

def generate_data():
    pdf_path1 = "./data/SOFI-2023.pdf"
    pdf_path2 = "./data/SOFI-2024.pdf"
    document_sections_1 = extract_text_from_pdf(pdf_path1)
    document_sections_2 = extract_text_from_pdf(pdf_path2)
    document_sections = document_sections_1 + document_sections_2
    print("document sctions generated!")
    return document_sections

def generate_embeddings(document_sections):
    embeddings = model.encode(document_sections)
    embeddings = np.array(embeddings).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print("embeddings generated!")
    return embeddings, index

# def save_embeddings(embeddings, file_path):
    # np.save(file_path, embeddings)

def save_embeddings(embeddings):
    key = "embeddings"
    # Check if the key exists in Redis
    if redis_client.exists(key):
        print("Embeddings already exist in Redis!")
    else:
        # Save embeddings if they do not already exist
        redis_client.set(key, embeddings.tobytes())
        print("Saved embeddings to Redis!")
    
# def load_embeddings(file_path):
#     return np.load(file_path)

def load_embeddings(dimension=384):
    key = "embeddings"
    embeddings_data = redis_client.get(key)
    if embeddings_data:
        print("Successfully retrieved embeddings from Redis!")
        return np.frombuffer(embeddings_data, dtype='float32').reshape(-1, dimension)
    print("Failed to retrieve embeddings from Redis!")
    return None

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print("Created FAISS index!")
    return index

# def save_data(data, file_path):
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# def load_data(file_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         return json.load(f)

def save_data(data):
    key="document_sections"
    # Store document sections in Redis as a JSON string
    redis_client.set(key, json.dumps(data))
    print("Saved data to Redis!")

def load_data():
    key="document_sections"
    # Try load document sections from Redis first
    data = redis_client.get(key)
    if data:
        print("Successfully retrive data from Redis!")
        return json.loads(data.decode('utf-8')) # Deserialize JSON to Python object
    print("Successfully retrive data from Redis!")
    return None

def init_app():
    global document_sections, output_index
    document_sections = load_data()
    if document_sections is None:
        document_sections = generate_data()
        save_data(document_sections)
    
    # Load embeddings from Redis if available, otherwise generate and save
    embeddings = load_embeddings()
    if embeddings is None:
        embeddings, output_index = generate_embeddings(document_sections)
        save_embeddings(embeddings)
    else:
        output_index = create_faiss_index(embeddings)

@app.route('/search', methods=['GET'])
def index():
    global document_sections, output_index
    query_params = request.args.get('message')
    print(query_params)
    result = pipeline1(query_params, document_sections=document_sections, index=output_index)
    return jsonify({'message': result})

if __name__ == '__main__':
    # data_file = './data/document_sections.json'
    # embeddings_file = './data/embeddings.npy'
    
    # if not os.path.exists(data_file):
    #     document_sections = generate_data()
    #     save_data(document_sections, data_file)
    # else:
    #     document_sections = load_data(data_file)

    # if not os.path.exists(embeddings_file):
    #     embeddings, index = generate_embeddings(document_sections)
    #     save_embeddings(embeddings, embeddings_file)
    # else:
    #     embeddings = load_embeddings(embeddings_file)
    #     index = create_faiss_index(embeddings)
    
    # Load document sections from Redis if available, otherwise generate and save
    init_app()

    app.run(debug=True)