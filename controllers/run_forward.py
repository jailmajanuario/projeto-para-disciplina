import sys
import json
import traceback
from semanticscholar import SemanticScholar
import re
import hashlib

BASE_URL = 'https://doi.org/'

def slugify(text):
    # Gera slug com base no título (limpo e curto)
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)[:50]

def generate_paper_id(title):
    if not title:
        return "id-desconhecido"
    slug = slugify(title)
    return slug or hashlib.md5(title.encode()).hexdigest()[:10]

def search_sscholar(doi):
    sch = SemanticScholar(timeout=100)
    cleaned_doi = doi.split('doi.org/')[-1]
    try:
        paper = sch.get_paper(f'DOI:{cleaned_doi}')
        return paper
    except Exception as e:
        print(f"Erro buscando o artigo: {e}")
        return None

def parse_citations(paper):
    citations = []

    if not paper or paper._data.get('citations') is None:
        return citations

    for c in paper._data.get('citations', []):
        title = c.get('title', '-')
        year = c.get('year', '-')
        venue = c.get('venue', '-')
        doi = c.get('externalIds', {}).get('DOI', '-')
        abstract = c.get('abstract', '-')

        # Processar autores
        autores = []
        for author in c.get('authors', []):
            autores.append({"name": author.get('name', '-')})

        citation_obj = {
            "paperId": generate_paper_id(title),  # ✅ Adiciona identificador único
            "title": title,
            "authors": autores,
            "year": year,
            "venue": venue,
            "doi": doi if doi else '-',
            "abstract": abstract
        }

        citations.append(citation_obj)
    return citations

def main():
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"error": "Uso: python run_forward.py <DOI>"}))
            sys.exit(1)

        doi = sys.argv[1]
        sch_paper = search_sscholar(doi)

        if not sch_paper:
            print(json.dumps({"error": f"Artigo com DOI {doi} não encontrado."}))
            sys.exit(1)

        # --------- Informações do artigo semente ---------
        title = sch_paper._data.get('title', '-')
        year = sch_paper._data.get('year', '-')
        venue = sch_paper._data.get('venue', '-')
        abstract = sch_paper._data.get('abstract', '-')
        paper_doi = sch_paper._data.get('doi', doi)

        # Processar citações
        citations = parse_citations(sch_paper)
        citations_count = len(citations)

        result = {
            "input_doi": paper_doi,
            "title": title,
            "year": year,
            "venue": venue,
            "abstract": abstract,
            "citations_count": citations_count,
            "citations": citations
        }

        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(json.dumps(result))

    except Exception as e:
        traceback.print_exc()
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
