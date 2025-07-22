from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import requests
import base64
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
load_dotenv()
def qa_chain():
    # Definir el prompt directo
    template = """
Eres una inteligencia artificial especializada en generar interfaces Flutter.

Tu tarea es generar un JSON siguiendo EXACTAMENTE el siguiente formato. No debes usar ningún otro widget que no esté en el ejemplo.

Todos los componentes deben estar posicionados con propiedades `top` y `left`, y deben tener `children: []`. No debes anidar componentes dentro de otros, ni usar la propiedad `alignment`.

Debes generar objetos del siguiente tipo (las llaves dobles indican que son literales, no variables del prompt):

interface CanvasComponent {{
  id: string;
  type: string;
  top?: number;
  left?: number;
  width?: number;
  height?: number;
  decoration?: {{
    color: string;
    border: {{
      color: string;
      width?: number;
    }};
    borderRadius: number;
  }};
  text?: string;

  options?: string[];
  icon?: string;
  tooltip?: string;
  navigateTo?: string;

  title?: string;
  centerTitle?: boolean;
  leading?: CanvasComponent | null;
  actions?: CanvasComponent[];

  children: CanvasComponent[];
  parentId: string | null;
  childrenLayout?: string;
  gap?: number;
  selectedOption?: string;

  fontSize?: number;
  textColor?: string;
  autoSize?: boolean;

  fontFamily?: string;
  textIndent?: number;
  textAlign?: 'left' | 'center' | 'right' | 'justify';

  checked?: boolean;
  checkColor?: string;
  labelPosition?: 'left' | 'right' | 'top' | 'bottom';
  labelGap?: number;
  checkSize?: number;
  onChangeAction?: string;
  activeColor?: string;
  borderColor?: string;
  borderWidth?: number;
  borderRadius?: number;
  scale?: number;

  labelText?: string;
  hintText?: string;
  value?: string;
  inputType?: 'text' | 'email' | 'password' | 'number' | 'tel';
  maxLength?: number;
  enabled?: boolean;
  obscureText?: boolean;
  borderType?: 'outline' | 'underline' | 'none';
  focusedBorderColor?: string;
  labelColor?: string;
  hintColor?: string;
  inputTextColor?: string;
  backgroundColor?: string;

  padding?: {{
    top?: number;
    right?: number;
    bottom?: number;
    left?: number;
  }};
  paddingAll?: number;
}}

Ejemplo de salida válida (no lo repitas, es solo referencia):

[
  {{
    "id": "76097a5a-2b9a-4415-a5b5-8cba58a17b8f",
    "type": "AppBar",
    "top": 0,
    "left": 0,
    "width": 360,
    "height": 70,
    "decoration": {{
      "color": "#2196f3",
      "border": {{
        "color": "#000000",
        "width": 0
      }},
      "borderRadius": 0
    }},
    "children": [],
    "parentId": null
  }},
  {{
    "id": "2a58b037-35bd-43b7-bc9f-1fee0a88173e",
    "type": "Text",
    "text": "Usuario",
    "fontSize": 16,
    "autoSize": true,
    "width": 62,
    "height": 30,
    "top": 50,
    "left": 0,
    "children": [],
    "parentId": null
  }},
  {{
    "id": "a8211c1c-0bf4-4393-aec1-5c714e0d7539",
    "type": "TextField",
    "top": 88,
    "left": 44,
    "width": 200,
    "height": 56,
    "decoration": {{
      "color": "#ffffff",
      "border": {{
        "color": "#e0e0e0",
        "width": 1
      }},
      "borderRadius": 4
    }},
    "hintText": "Ingresa el texto aquí",
    "value": "",
    "inputType": "text",
    "enabled": true,
    "borderType": "outline",
    "focusedBorderColor": "#2196f3",
    "labelColor": "#757575",
    "hintColor": "#9e9e9e",
    "inputTextColor": "#212121",
    "fontSize": 16,
    "children": [],
    "parentId": null
  }},
  {{
    "id": "a874a8fe-c941-40d8-83e7-3897e16ed12e",
    "type": "Text",
    "text": "Password",
    "fontSize": 16,
    "autoSize": true,
    "width": 73,
    "height": 30,
    "top": 152,
    "left": 46,
    "children": [],
    "parentId": null
  }},
  {{
    "id": "88ee284c-634d-45ac-8002-f6ba1267a9de",
    "type": "TextField",
    "top": 178,
    "left": 44,
    "width": 200,
    "height": 56,
    "decoration": {{
      "color": "#ffffff",
      "border": {{
        "color": "#e0e0e0",
        "width": 1
      }},
      "borderRadius": 4
    }},
    "hintText": "Ingresa el texto aquí",
    "value": "",
    "inputType": "text",
    "enabled": true,
    "borderType": "outline",
    "focusedBorderColor": "#2196f3",
    "labelColor": "#757575",
    "hintColor": "#9e9e9e",
    "inputTextColor": "#212121",
    "fontSize": 16,
    "children": [],
    "parentId": null
  }},
  {{
    "id": "4c1c014a-2fe6-4db5-ac26-fd75cb5db73d",
    "type": "TextButton",
    "top": 265,
    "left": 111,
    "width": 120,
    "height": 48,
    "decoration": {{
      "color": "#ffffff",
      "border": {{
        "color": "#000000",
        "width": 2
      }},
      "borderRadius": 8
    }},
    "navigateTo": "/pantalla2",
    "text": "Ingresar",
    "textColor": "#000000",
    "textAlign": "center",
    "fontSize": 16,
    "fontFamily": "inherit",
    "children": [],
    "parentId": null
  }}
]

===

Teniendo en cuenta ese formato, genera un diseño Flutter cumpliendo con los siguientes requerimientos:

{question}

Recuerda:
- No debes modificar la estructura general.
- No inventes nuevos widgets.
- No incluyas comentarios en el JSON.
- No anides componentes (deja siempre el `"children": []`).
- Usa exclusivamente `top` y `left` para ubicar los elementos.
- Nunca uses `alignment`.
- Responde exclusivamente con la estructura JSON solicitada.
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


def analyze_image(image_path, prompt="Describe la imagen"):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-vision-preview",
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
