from flask import Flask, jsonify, request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
REMITENTE = os.getenv("REMITENTE")
DESTINATARIO = os.getenv(
    "DESTINATARIO"
)  # En producción, usar request.args o request.form


@app.route("/")
def home():
    return "Hola, Flask está funcionando correctamente!"


@app.route("/send-newsletter", methods=["POST"])
def send_newsletter_view():
    # Simulación de 5 papers (normalmente vendrían de una base de datos o del body)
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
        {
            "titulo": "Machine Learning interpretativo",
            "url": "https://ejemplo.com/paper4",
        },
        {"titulo": "IA en videojuegos", "url": "https://ejemplo.com/paper5"},
    ]

    # Validación básica
    if not SENDGRID_API_KEY or not REMITENTE or not DESTINATARIO:
        return (
            jsonify({"status": "error", "message": "Faltan variables de entorno"}),
            500,
        )
    if not papers:
        return jsonify({"status": "error", "message": "No hay papers para enviar"}), 400

    # Crear HTML
    contenido_html = "<html><body><h2 style='font-family:sans-serif'>🧠 Recomendaciones de Papers</h2><ul>"
    for paper in papers[:5]:
        if "titulo" not in paper or "url" not in paper:
            return (
                jsonify({"status": "error", "message": "Formato inválido en papers"}),
                400,
            )
        contenido_html += f'<li><a href="{paper["url"]}">{paper["titulo"]}</a></li>'
    contenido_html += "</ul><p style='font-size:12px;color:gray'>Newsletter enviado automáticamente con SendGrid 🚀</p></body></html>"

    # Alternativa texto plano
    texto_plano = "🧠 Recomendaciones:\n" + "\n".join(
        f"- {p['titulo']}: {p['url']}" for p in papers[:5]
    )

    # Crear mensaje
    mensaje = Mail(
        from_email=REMITENTE,
        to_emails=DESTINATARIO,
        subject="📰 Newsletter de Papers",
        plain_text_content=texto_plano,
        html_content=contenido_html,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(mensaje)
        return jsonify({"status": "enviado"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
