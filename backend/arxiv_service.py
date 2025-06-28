import requests
import xml.etree.ElementTree as ET
import os

# funcion que hace solucitud a la api y trae datos
def get_latest_papers(area):
    url = os.getenv('ARXIV_API_URL')
    print("🌐 URL base:", url)

    query = f'search_query=cat:{area}&start=0&max_results=5&sortBy=lastUpdatedDate&sortOrder=descending'
    full_url = f"{url}?{query}"
    print("🔍 URL completa:", full_url)

    response = requests.get(full_url, timeout=10)
    print("📡 Código de respuesta:", response.status_code)
    print("📄 XML recibido (primeros 300 chars):", response.text[:300])

    if response.status_code != 200:
        return []

    
    
    root = ET.fromstring(response.text)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    papers = []
    
    
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        pdf_url = next((l.attrib['href'] for l in entry.findall('atom:link', ns) if l.attrib.get('type') == 'application/pdf'), '')
        doi_tag = entry.find("atom:arxiv:doi", {'arxiv': 'http://arxiv.org/schemas/atom'})
        doi = doi_tag.text if doi_tag is not None else 'Sin DOI'
        
        papers.append({
            'title': title,
            'authors': authors,
            'pdf_url': pdf_url,
            'doi': doi
        })
        
    return papers