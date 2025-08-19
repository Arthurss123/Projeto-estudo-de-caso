from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
import re

SCHEMA = Schema(
    nome_arquivo=ID(stored=True, unique=True),
    conteudo=TEXT(stored=True)
)

def criar_indice(caminho_indice: str, documentos: dict):
    if not os.path.exists(caminho_indice):
        os.mkdir(caminho_indice)
    
    ix = create_in(caminho_indice, SCHEMA)
    writer = ix.writer()
    
    for nome_arquivo, conteudo in documentos.items():
        writer.add_document(nome_arquivo=nome_arquivo, conteudo=conteudo)
        print(f"Indexando: {nome_arquivo}")
    
    writer.commit()
    print("Indexação concluída.")

def buscar(caminho_indice: str, query_string: str) -> list:
    ix = open_dir(caminho_indice)
    resultados_finais = []
    
    with ix.searcher() as searcher:
        parser = QueryParser("conteudo", ix.schema)
        query = parser.parse(query_string)
        
        resultados = searcher.search(query, limit=5) # Limita aos 5 mais relevantes
        
        for resultado in resultados:
            resultados_finais.append({
                "nome_arquivo": resultado['nome_arquivo'],
                "score": resultado.score,
                "trecho_relevante": resultado.highlights("conteudo") # Mostra onde a busca bateu
            })
            
    return resultados_finais

def extrair_contexto(texto, termo, janela=200):
    termo_lower = termo.lower()
    texto_lower = texto.lower()

    idx = texto_lower.find(termo_lower)
    if idx == -1:
        return texto[:janela*2]

    inicio = max(0, idx - janela)
    fim = min(len(texto), idx + len(termo) + janela)
    return texto[inicio:fim]

def limpar(texto):
    return re.sub(r'<.*?>', '', texto)

if __name__ == '__main__':
    from extracao import processar_pasta
    documentos = processar_pasta("data")
    caminho_do_indice = "indice_whoosh"
    criar_indice(caminho_do_indice, documentos)

    query = "qual segundo artigo da LEI Nº 9.784" 
    resultados_busca = buscar(caminho_do_indice, query)
    print(f"\n--- Resultados para a busca: '{query}' ---")
    if not resultados_busca:
        print("Nenhum documento relevante encontrado.")
    else:
        for res in resultados_busca:
            print(f"Arquivo: {res['nome_arquivo']}")
            print(f"Relevância (Score): {res['score']:.2f}")
            texto_original = documentos[res['nome_arquivo']]
            trecho_limpo = extrair_contexto(texto_original, query, janela=250)
            print(f"Trecho: ...{limpar(trecho_limpo)}...")
            print("-" * 10)