# PaperTrail
Una aplicación web ligera en Flask que te envía (al instante) un boletín con los **5 preprints más recientes** de arXiv en tu área de interés, junto con un **resumen automático** generado por IA.

---

## 🔍 Características

- **Búsqueda en arXiv**: consulta las últimas publicaciones por categoría.  
- **Descarga y parsing de PDF**: extrae texto completo con PyMuPDF.  
- **Resumen automático**: sintetiza los puntos clave con IA (OpenAI o modelo local).  
- **Newsletter por email**: envía el digest por SendGrid o SMTP de Gmail.  
- **UI minimalista**: formulario sencillo con dropdown de categorías.  

---

## 🚀 Tecnologías

| Capa               | Tecnologías                                        |
|--------------------|----------------------------------------------------|
| **Backend**        | Python 3.8+, Flask, python-dotenv                  |
| **PDF / Texto**    | PyMuPDF (`fitz`), requests                         |
| **IA**             | OpenAI SDK (o Hugging Face Transformers local)     |
| **Email**          | SendGrid API Client **o** `smtplib` / Gmail SMTP   |
| **Templates**      | Jinja2                                             |
| **Control de versiones** | Git / GitHub                              |

---

## 📦 Instalación

```bash
git clone https://github.com/TU_USUARIO/PaperTrail.git
cd PaperTrail/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
