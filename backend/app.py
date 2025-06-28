from flask import Flask, render_template, request
from arxiv_service import get_latest_papers
from dotenv import load_dotenv
import os
import requests
import fitz  # PyMuPDF
import smtplib
from email.message import EmailMessage

load_dotenv()
app = Flask(__name__)

# Ruta principal con formulario simple
@app.route('/')
def home():
    return render_template('suscripcion.html')  # solo email + área

@app.route('/suscribirse', methods=['POST'])
def suscribirse():
    email = request.form.get('email')
    area = request.form.get('tipo_noticia')
    

    # 1. Conseguir papers
    papers = get_latest_papers(area)
    if not papers:
        return "No se encontraron papers 😢"

    pdf_url = papers[0]['pdf_url']
    pdf_content = requests.get(pdf_url).content

    # 2. Guardar PDF temporalmente
    with open('temp.pdf', 'wb') as f:
        f.write(pdf_content)

    # 3. Extraer texto del PDF
    with fitz.open("temp.pdf") as doc:
        full_text = ""
        for page in doc:
            full_text += page.get_text()

    os.remove('temp.pdf')

    # 4. Resumir con IA (simulado por ahora)
    resumen = resumir_texto_con_ia(full_text)
    
    # 5. Armar cuerpo del mail
    titulos = "\n".join([f"- {p['title']}" for p in papers])
    cuerpo = f"Títulos de los últimos papers:\n{titulos}\n\nResumen del primero:\n{resumen}"

    # 5. Enviar email con resumen
    enviar_mail(email, resumen, cuerpo, pdf_content)

    return render_template('gracias.html')

# Simula llamada a la IA (reemplazá con OpenAI u otra)
def resumir_texto_con_ia(texto):
    return texto[:1000] + "..."  # recorta por ahora

# Función para enviar email
def enviar_mail(destinatario, cuerpo, adjunto_pdf):
    msg = EmailMessage()
    msg['Subject'] = 'Resumen de Paper Científico'
    msg['From'] = os.getenv('EMAIL_REMITENTE')
    msg['To'] = destinatario
    msg.set_content(cuerpo)
    msg.add_attachment(adjunto_pdf, maintype='application', subtype='pdf', filename='paper.pdf')

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_REMITENTE'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
