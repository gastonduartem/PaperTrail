import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# --- Cargar variables del .env ---
load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
REMITENTE = os.getenv("REMITENTE")
DESTINATARIO = os.getenv("DESTINATARIO")

# --- Lista de "papers" o artículos ---
papers = [
    {"titulo": "Deep Learning para NLP", "url": "https://ejemplo.com/paper1"},
    {
        "titulo": "Transformers y el futuro de la IA",
        "url": "https://ejemplo.com/paper2",
    },
    {
        "titulo": "Visión Computacional aplicada a Medicina",
        "url": "https://ejemplo.com/paper3",
    },
]

# --- Crear plantilla HTML dinámicamente ---
contenido_html = "<h2>🧠 Papers recomendados</h2><ul>"
for paper in papers:
    contenido_html += f'<li><a href="{paper["url"]}">{paper["titulo"]}</a></li>'
contenido_html += "</ul><p>Enviado automáticamente con SendGrid 🚀</p>"

# --- Crear y enviar correo ---
mensaje = Mail(
    from_email=REMITENTE,
    to_emails=DESTINATARIO,
    subject="📰 Newsletter de Papers",
    html_content=contenido_html,
)

try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    respuesta = sg.send(mensaje)
    print(f"✅ Correo enviado. Status: {respuesta.status_code}")
except Exception as e:
    print("❌ Error al enviar correo:", e)
