# importamos requests para hacer petisiones http a la api
import requests
# importamos el modulo para parsear XML
import xml.etree.ElementTree as ET
# importamos os para accedera variables de entorno
import os

# funcion principal que recibe un area de busqueda y devuelve los ultimos papers
def get_latest_papers(area):
    # obtenemos la url desde el archivo .env
    base_url = os.getenv('ARXIV_API_URL') or 'https://export.arxiv.org/api/query'
    print("🌐 URL base:", base_url)

    # parametros de busqueda para armar la url completa
    params = {
        'search_query': f'cat:{area}',
        'start': 0,
        'max_results': 5,
        'sortBy': 'lastUpdatedDate',
        'sortOrder': 'descending'
    }
    full_url = f"{base_url}?{'&'.join(f'{k}={v}' for k,v in params.items())}"
    print("🔍 URL completa:", full_url)

    # hacemos la peticion http a la api
    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("⚠️ Error en la peticion:", e) # si hubo error devuelve una lista vacia
        return []

    print("📄 XML recibido (primeros 300 chars):", response.text[:300])

    # 4) Parseo seguro del XML
    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print("⚠️ Error al parsear XML:", e)
        return []

    # namesapce que usa arxiv
    ATOM_NS = '{http://www.w3.org/2005/Atom}'
    ARXIV_NS = '{http://arxiv.org/schemas/atom}'

    #lista donde se guardan los papers que se encuentran
    papers = []

    for entry in root.findall(f'{ATOM_NS}entry'):
        title_el = entry.find(f'{ATOM_NS}title')
        title_text = title_el.text.strip() if title_el is not None and title_el.text else 'Sin título'

        authors = [
            a.find(f'{ATOM_NS}name').text
            for a in entry.findall(f'{ATOM_NS}author')
            if a.find(f'{ATOM_NS}name') is not None and a.find(f'{ATOM_NS}name').text
        ]

    # buscamos el link al pdf
        pdf_url = ''
        for link in entry.findall(f'{ATOM_NS}link'):
            if link.attrib.get('type') == 'application/pdf':
                pdf_url = link.attrib.get('href')
                break

        doi_el = entry.find(f'{ARXIV_NS}doi')
        doi_text = doi_el.text.strip() if doi_el is not None and doi_el.text else 'Sin DOI'

    # guardamos toda la info del paper como un diccionario
        papers.append({
            'title': title_text,
            'authors': authors,
            'pdf_url': pdf_url,
            'doi': doi_text
        })

    # retornamos la lista de papers para poder mostrar en el html
    return papers
