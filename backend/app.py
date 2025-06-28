# importamos flask y las funciones para renderizar templates
from flask import Flask, render_template, request, redirect
# funcion que se encarga de consultar a la api de arxiv 
from arxiv_service import get_latest_papers
# dotenv para poder leer variables de entorno
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ruta principal, redirige a la siguiente ruta papers
@app.route('/')
def home():
    return redirect('/papers?area=cs.AI')

@app.route('/papers')
def list_papers():
    area = request.args.get('area', 'physics')
    papers = get_latest_papers(area)
    # renderiza el html llamando al archivo html
    return render_template('papers.html', papers=papers)

if __name__ == '__main__':
    app.run(debug=True)
