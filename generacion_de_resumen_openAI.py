from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import PyPDF2 
load_dotenv()
#Se consigue la api key del archivo .env
api_key_ = os.getenv("OPENAI_API_KEY")
#Se crea el objeto cliente y se configura la IA
client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key= api_key_
)
#Se selecciona el modelo de IA
model = "deepseek/deepseek-r1"
#Stream en False permite que la respuesta no aparezca por partes
stream = False  # or False
#Se limitan los token a usar
max_tokens = 900

def respuesta_ia(ruta_pdf):
    global texto
    #Variable donde se guardara el texto extraido del pdf
    texto = ""
    # Abrimos el archivo PDF en modo lectura binaria ("rb")
    with open(ruta_pdf, "rb") as archivo:
        # Creamos un lector de PDF usando la librería PyPDF2
        lector = PyPDF2.PdfReader(archivo)
        # Recorremos cada página del PDF
        for pagina in lector.pages:
            # Extraemos el texto de la página y lo agregamos a la variable 'texto'
            texto += pagina.extract_text() + "\n" # El "\n" agrega un salto de línea entre páginas
    #Se guarda el texto en la variable a enviarse a la IA
    texto_pdf = texto 
    #Se crea el obejeto que permite la comunicacion con la IA
    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "you are a professional AI helper。",
            },
            {  #El esquema que usamos como usuaria para comunicarnos con la IA
                "role": "user",
                "content": f"""Como un experto en resúmenes de documentos, por favor, realiza un resumen conciso del archivo PDF que te proporcionaré.
                              Instrucciones:
                              - Coloca el titulo principal del documento al inicio 
                              - El resumen debe contener un máximo de 3 párrafos.
                              - Utiliza un lenguaje sencillo y claro, evitando comentarios adicionales o juicios de valor.
                              - Asegúrate de captar los puntos clave y la esencia del contenido del documento.
                              Tu tarea es clarificar la información de manera accesible para cualquier lector. \n{texto_pdf}""",
            }
        ],
        stream=stream,
        max_tokens=max_tokens,
    )

    if stream:
        for chunk in chat_completion_res:
            print(chunk.choices[0].delta.content or "", end="")
    else:
        respuesta = chat_completion_res.choices[0].message.content
        #Se limpia la respuesta de la IA para tener no tener textos indeseados en la respuesta final
        respuesta_limpia = re.sub(r"<think>.*?</think>", "", respuesta, flags=re.DOTALL).strip()
  
    return respuesta_limpia 

