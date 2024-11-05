from flask import Flask, request, jsonify
import pdfplumber
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import faiss
from transformers import pipeline

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Generate embeddings for each section

def search(query, k=3, document_sections=None, index=None):
    query_embedding = model.encode([query]).astype('float32')

    # Search for the k most similar embeddings
    _, indices = index.search(query_embedding, k)
    
    # Return the sections
    return [document_sections[idx] for idx in indices[0]]

def pipeline1(query, k=3, document_sections=None, index=None):
    answers = []
    print("Searching for:", query)
    print("Top", k, "results:")
    print(len(document_sections))
    print(len(index))
    for section in search(query, k, document_sections, index):
        result = qa_pipeline(question=query, context=section)
        answers.append(result['answer'])
    
    return ''.join(answers)

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        document_sections = []
        for page in pdf.pages:
            text = page.extract_text()
            text_segments = text.split("\n\n")  # Split by paragraphs
    
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
    return document_sections

def generate_embeddings(document_sections):
    embeddings = model.encode(document_sections)
    embeddings = np.array(embeddings).astype('float32')
    dimension = embeddings.shape[1]  # Number of dimensions in the embeddings
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

document_sections =[]
index = []

@app.route('/search', methods=['GET'])
def index():
    query_params = request.args.get('message')
    result = pipeline1(query_params, 3, document_sections, index)
    return jsonify({'message': result})

if __name__ == '__main__':
    document_sections = generate_data()
    index = generate_embeddings(document_sections)
    # save document_sections and index to disk
    
    
    app.run(debug=True)