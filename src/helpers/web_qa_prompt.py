from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

def web_qa_chain():
    # Definir el prompt directo
    template = """
Eres una inteligencia artificial especializada en generar interfaces web en Angular.

Tu tarea es generar un JSON siguiendo EXACTAMENTE el siguiente formato de componentes CanvasComponent. No debes usar ningún otro tipo de estructura ni inventar propiedades.

Todos los componentes deben estar posicionados con las propiedades `top` y `left` dentro de `style`, y deben tener `children: []` (o el arreglo correspondiente). Puedes anidar componentes solo si el ejemplo lo muestra. Usa la interfaz proporcionada.

Debes generar objetos del siguiente tipo (las llaves dobles indican que son literales, no variables del prompt):

export interface CanvasComponent {
  id: string;
  type?: string; // 'div' | 'label' | 'input' | etc.
  style: {
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
  };
  children?: CanvasComponent[];
  parentId?: string | null;
  content?: string; // contenido textual para tags como label
  checked?: boolean; // para checkbox y radio
  groupName?: string; // para agrupar radio buttons
  label?: string; // etiqueta alternativa para checkbox/radio
}

Ejemplo de salida válida (no lo repitas, es solo referencia):

[
  {
    "id": "3412d8da-7d37-416f-bd40-4c8de54fcabd",
    "type": "div",
    "style": {
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
    },
    "content": "Nuevo Div",
    "children": [
      {
        "id": "636eb093-b909-4f7a-8631-856c39724343",
        "type": "div",
        "style": {
          "top": "78px",
          "left": "29px",
          "width": "100px",
          "height": "60px",
          "backgroundColor": "#d0d0ff",
          "color": "#004040",
          "border": "2px solid #004040",
          "borderRadius": "10px",
          "position": "absolute"
        },
        "content": "div hijo",
        "children": [],
        "parentId": "3412d8da-7d37-416f-bd40-4c8de54fcabd"
      }
    ],
    "parentId": null
  },
  {
    "id": "81f6aa7c-489e-4638-96e0-a197b258b678",
    "type": "label",
    "style": {
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
    },
    "content": "Pagina 1",
    "children": [],
    "parentId": null
  },
  {
    "id": "fb962bba-62c9-4a41-a07b-a09261afd59a",
    "type": "checkbox",
    "style": {
      "top": "473px",
      "left": "167px",
      "position": "absolute",
      "fontSize": "14px",
      "fontFamily": "Arial, sans-serif",
      "textAlign": "center",
      "backgroundColor": "#f7f7f7",
      "color": "#9a3232",
      "border": "0 solid #cb1a1a"
    },
    "content": "Hecho?",
    "checked": false,
    "children": [],
    "parentId": null
  },
  {
    "id": "43ee1101-1cc7-4c35-8bbe-1c1c4ea19178",
    "type": "radio",
    "style": {
      "top": "532px",
      "left": "155px",
      "position": "absolute",
      "fontSize": "14px",
      "fontFamily": "Arial, sans-serif"
    },
    "content": "Opción de radio",
    "checked": false,
    "groupName": "radioGroup1",
    "children": [],
    "parentId": null
  },
  {
    "id": "6efd3d2f-af66-4abd-aa0c-1b53679b4270",
    "type": "select",
    "style": {
      "top": "328px",
      "left": "325px",
      "width": "160px",
      "height": "40px",
      "backgroundColor": "#ffffff",
      "color": "#000000",
      "border": "1px solid #cccccc",
      "borderRadius": "4px",
      "position": "absolute",
      "fontSize": "14px",
      "fontFamily": "Arial, sans-serif"
    },
    "content": "",
    "children": [
      {
        "id": "4ec35b49-1f71-481b-9fa0-565e83d4e3f7",
        "type": "option",
        "style": {},
        "content": "Opción 1",
        "children": [],
        "parentId": null
      },
      {
        "id": "4899f01a-bb75-4937-b1d6-7f03939970c2",
        "type": "option",
        "style": {},
        "content": "Opción 2",
        "children": [],
        "parentId": null
      },
      {
        "id": "f60c3f83-add3-4927-9d4f-c08e9266df9a",
        "type": "div",
        "style": {
          "top": "10px",
          "left": "10px",
          "width": "100px",
          "height": "60px",
          "backgroundColor": "#d0d0ff",
          "color": "#004040",
          "border": "2px solid #004040",
          "borderRadius": "10px",
          "position": "absolute"
        },
        "content": "div hijo",
        "children": [],
        "parentId": "6efd3d2f-af66-4abd-aa0c-1b53679b4270"
      }
    ],
    "parentId": null
  },
  {
    "id": "ec8b2e44-fa72-4fd6-885d-8c283b823c51",
    "type": "button",
    "style": {
      "top": "432px",
      "left": "380px",
      "width": "120px",
      "height": "40px",
      "backgroundColor": "#4f46e5",
      "color": "#ffffff",
      "border": "none",
      "borderRadius": "6px",
      "position": "absolute",
      "fontSize": "14px",
      "fontFamily": "Arial, sans-serif",
      "cursor": "pointer",
      "textAlign": "center",
      "lineHeight": "40px",
      "fontWeight": "bold",
      "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
      "transition": "all 0.2s ease",
      "display": "inline-block"
    },
    "content": "Click me",
    "children": [],
    "parentId": null
  },
  {
    "id": "2c1ef5fc-69ad-43f7-9af4-beeb2233b39e",
    "type": "checkbox",
    "style": {
      "top": "637px",
      "left": "204px",
      "position": "absolute",
      "fontSize": "14px",
      "fontFamily": "Arial, sans-serif"
    },
    "content": "Opción de checkbox",
    "checked": false,
    "children": [],
    "parentId": null
  },
  {
    "id": "c368a081-87ad-4eba-b664-e309f7a4debe",
    "type": "table",
    "style": {
      "top": "566px",
      "left": "433px",
      "width": "400px",
      "height": "auto",
      "border": "1px solid #000",
      "position": "absolute",
      "backgroundColor": "#ffffff"
    },
    "children": [
      {
        "id": "80ba12d8-edab-49ce-846a-fa30cf303fd7",
        "type": "tr",
        "children": [
          {
            "id": "9bfa0231-2dbc-4baf-bf4d-39d229997c68",
            "type": "td",
            "content": "Col 1",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          },
          {
            "id": "307f1bf0-1a74-4385-b13e-2e0f71e4671e",
            "type": "td",
            "content": "Col 2",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          },
          {
            "id": "15d1d855-4972-496b-bd78-d70b398579b8",
            "type": "td",
            "content": "Col 3",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          }
        ],
        "style": {},
        "parentId": null
      },
      {
        "id": "d1ec492b-e16d-478a-9b93-6af1642d30fc",
        "type": "tr",
        "children": [
          {
            "id": "2f121231-3773-4068-8a89-dd1676f72695",
            "type": "td",
            "content": "Dato 1",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          },
          {
            "id": "caf35363-c1bc-4a05-b6f5-22524f84abd1",
            "type": "td",
            "content": "Dato 2",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          },
          {
            "id": "114b4088-e03c-492d-9f5b-ccc19027a4c2",
            "type": "td",
            "content": "Dato 3",
            "style": {
              "border": "1px solid #ccc"
            },
            "children": [],
            "parentId": null
          }
        ],
        "style": {},
        "parentId": null
      }
    ],
    "content": "",
    "parentId": null
  },
  {
    "id": "09f7d6f9-9c43-4e9a-9a5a-0f4b86c38c48",
    "type": "label",
    "style": {
      "top": "764px",
      "left": "253px",
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
    },
    "content": "Etiqueta:",
    "children": [],
    "parentId": null
  }
]

===

Teniendo en cuenta ese formato, genera un diseño web en Angular cumpliendo con los siguientes requerimientos:

{{question}}

Recuerda:
- No debes modificar la estructura general.
- No inventes nuevos tipos de componentes ni propiedades.
- No incluyas comentarios en el JSON.
- Usa exclusivamente `top` y `left` para ubicar los elementos (en style).
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

def analyze_image_web(image_path, prompt="Describe la imagen para una interfaz web en Angular"):
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