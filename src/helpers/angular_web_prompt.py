from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

def angular_web_chain():
    # Definir el prompt directo
    template = """
Eres una inteligencia artificial especializada en generar interfaces web en Angular.

Tu tarea es generar un JSON siguiendo EXACTAMENTE el siguiente formato de componentes CanvasComponent. No debes usar ningún otro tipo de estructura ni inventar propiedades.

Todos los componentes deben estar posicionados con las propiedades `top` y `left` dentro de `style`, y deben tener `children: []` (o el arreglo correspondiente). Puedes anidar componentes solo si el ejemplo lo muestra. Usa la interfaz proporcionada.

Debes generar objetos del siguiente tipo:

export interface CanvasComponent {{
  id: string;
  type?: string; // 'div' | 'label' | 'input' | etc.
  style: {{
    top?: string;
    left?: string;
    width?: string;
    height?: string;
    backgroundColor?: string;
    color?: string;
    border?: string;
    borderRadius?: string;
    position?: string;
    fontSize?: string;
    fontFamily?: string;
    fontWeight?: string;
    cursor?: string;
    textAlign?: string;
    lineHeight?: string;
    boxShadow?: string;
    transition?: string;
    display?: string;
    padding?: string;
    margin?: string;
    marginBottom?: string;
    marginRight?: string;
    marginTop?: string;
    marginLeft?: string;
    paddingLeft?: string;
    paddingRight?: string;
    paddingTop?: string;
    paddingBottom?: string;
    borderBottom?: string;
    borderTop?: string;
    borderLeft?: string;
    borderRight?: string;
    justifyContent?: string;
    alignItems?: string;
    flexDirection?: string;
    transform?: string;
    bottom?: string;
    right?: string;
    textDecoration?: string;
    zIndex?: string;
  }};
  children?: CanvasComponent[];
  parentId?: string | null;
  content?: string; // contenido textual para tags como label
  checked?: boolean; // para checkbox y radio
  groupName?: string; // para agrupar radio buttons
  label?: string; // etiqueta alternativa para checkbox/radio
}}

Ejemplo de salida válida (no lo repitas, es solo referencia):

[
  {{
    "id": "3412d8da-7d37-416f-bd40-4c8de54fcabd",
    "type": "div",
    "style": {{
      "top": "48px",
      "left": "66px",
      "width": "239px",
      "height": "152px",
      "backgroundColor": "#f0f0f0",
      "color": "#000000",
      "border": "1px solid #cccccc",
      "borderRadius": "4px",
      "position": "absolute",
      "fontSize": "16px",
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "textAlign": "center",
      "lineHeight": "40px"
    }},
    "content": "Nuevo Div",
    "children": [
      {{
        "id": "636eb093-b909-4f7a-8631-856c39724343",
        "type": "div",
        "style": {{
          "top": "78px",
          "left": "29px",
          "width": "100px",
          "height": "60px",
          "backgroundColor": "#d0d0ff",
          "color": "#004040",
          "border": "2px solid #004040",
          "borderRadius": "10px",
          "position": "absolute"
        }},
        "content": "div hijo",
        "children": [],
        "parentId": "3412d8da-7d37-416f-bd40-4c8de54fcabd"
      }}
    ],
    "parentId": null
  }},
  {{
    "id": "81f6aa7c-489e-4638-96e0-a197b258b678",
    "type": "label",
    "style": {{
      "top": "234px",
      "left": "162px",
      "width": "100px",
      "height": "20px",
      "backgroundColor": "transparent",
      "color": "#000000",
      "position": "absolute",
      "fontSize": "16px",
      "fontFamily": "Arial, sans-serif",
      "fontWeight": "bold",
      "textAlign": "center",
      "lineHeight": "40px"
    }},
    "content": "Pagina 1",
    "children": [],
    "parentId": null
  }}
]

Además, puedes crear múltiples páginas como en este ejemplo:

{{
  "roomCode": "G1T0",
  "lastUpdated": "2025-07-21T15:45:48.858Z",
  "pages": [
    {{
      "id": "ac93bb89-8084-4be8-89a7-1616065bcf48",
      "name": "Página 1",
      "components": [
        {{
          "id": "3412d8da-7d37-416f-bd40-4c8de54fcabd",
          "type": "div",
          "style": {{
            "top": "48px",
            "left": "66px",
            "width": "239px",
            "height": "152px",
            "backgroundColor": "#f0f0f0",
            "color": "#000000",
            "border": "1px solid #cccccc",
            "borderRadius": "4px",
            "position": "absolute",
            "fontSize": "16px",
            "fontFamily": "Arial, sans-serif",
            "fontWeight": "bold",
            "textAlign": "center",
            "lineHeight": "40px"
          }},
          "content": "Nuevo Div",
          "children": [],
          "parentId": null
        }}
      ]
    }},
    {{
      "id": "01081d27-2ed6-4ef4-bf4c-fa43bedec333",
      "name": "Página 2",
      "components": [
        {{
          "id": "cf688311-d8c1-4bd8-900e-4ff9d2f5b1ea",
          "type": "label",
          "style": {{
            "top": "123px",
            "left": "113px",
            "width": "100px",
            "height": "20px",
            "backgroundColor": "transparent",
            "color": "#000000",
            "position": "absolute",
            "fontSize": "16px",
            "fontFamily": "Arial, sans-serif",
            "fontWeight": "bold",
            "textAlign": "center",
            "lineHeight": "40px"
          }},
          "content": "Pagina2",
          "children": [],
          "parentId": null
        }}
      ]
    }}
  ]
}}

===

Teniendo en cuenta ese formato, genera un diseño web en Angular cumpliendo con los siguientes requerimientos:

{question}

Recuerda:
- No debes modificar la estructura general.
- No inventes nuevos tipos de componentes ni propiedades.
- No incluyas comentarios en el JSON.
- Usa exclusivamente `top` y `left` para ubicar los elementos (en style).
- Responde exclusivamente con la estructura JSON solicitada.
- Puedes generar una estructura de múltiples páginas si el requerimiento lo necesita.
"""

    # Crear plantilla del prompt
    prompt = ChatPromptTemplate.from_template(template)

    # Definir el modelo LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)

    # Cadena de procesamiento
    qa_chain = (
        prompt
        | llm
        | StrOutputParser()
    )
    return qa_chain

def analyze_image_angular(image_path, prompt="Describe la imagen para una interfaz web en Angular"):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

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

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_angular_components(prompt):
    """Genera componentes Angular basados en un prompt"""
    chain = angular_web_chain()
    return chain.invoke({"question": prompt})