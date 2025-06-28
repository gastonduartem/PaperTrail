from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import PyPDF2 
load_dotenv()
api_key_ = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai",
    api_key= api_key_,
)

model = "deepseek/deepseek-r1"
stream = False  # or False
max_tokens = 900
def respuesta_ia(ruta_pdf):
    global texto
    texto = ""
    with open(ruta_pdf, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text() + "\n"

    texto_pdf = texto 

    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "you are a professional AI helper。",
            },
            {
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
        respuesta_limpia = re.sub(r"<think>.*?</think>", "", respuesta, flags=re.DOTALL).strip()
  
    return respuesta_limpia 

rp =respuesta_ia("documento.pdf")
print(rp)