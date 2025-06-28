from flask import Flask, render_template, request
from arxiv_service import get_latest_papers
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('ARXIV_API_URL')
print("ARXIV_API_URL =", url)

app = Flask(__name__)

@app.route('/')
def home():
    return list_papers()


@app.route('/papers')
def list_papers():
    area = request.args.get('area', 'physics')
    papers = get_latest_papers(area)
    return render_template('papers.html', papers=papers)

if __name__ == '__main__':
    app.run(debug=True)