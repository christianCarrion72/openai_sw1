import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, request, jsonify
from langchain_core.messages import AIMessage, HumanMessage
from src.helpers.qa_chain import qa_chain
import base64
import requests

app = Flask(__name__)
CORS(app)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

qa_chain = qa_chain()

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No se proporcionó una pregunta"}), 400
    response = qa_chain.invoke({
        "question": question
    })
    
    return jsonify({"response": response})

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400
    image = request.files['image']
    prompt = request.form.get("prompt", "Describe la imagen")
    img_bytes = image.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(response.json())  # <-- Agrega esto para depurar
        result = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500