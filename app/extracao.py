# extracao.py

import pdfplumber
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extrair_texto(caminho_do_arquivo: Path) -> str | None:
    """
    Extrai o texto completo de um arquivo PDF.

    Retorna o texto como uma string ou None se a extração falhar.
    """
    if not caminho_do_arquivo.is_file():
        logging.warning(f"Arquivo não encontrado: {caminho_do_arquivo}")
        return None

    texto_completo = ""
    try:
        with pdfplumber.open(caminho_do_arquivo) as pdf:
            for pagina in pdf.pages:
                texto_da_pagina = pagina.extract_text()
                if texto_da_pagina:
                    texto_completo += texto_da_pagina + "\n"
        return texto_completo
    except Exception as e:
        # Loga o erro específico e o nome do arquivo, o que ajuda a depurar
        logging.error(f"Falha ao extrair texto de '{caminho_do_arquivo.name}': {e}")
        return None

def processar_pasta(caminho_da_pasta: Path) -> dict[str, str]:
    """
    Processa todos os arquivos PDF em uma pasta e extrai seu texto.

    Retorna um dicionário com {nome_do_arquivo: texto_completo}.
    """
    textos_dos_documentos = {}
    logging.info(f"Iniciando processamento da pasta: {caminho_da_pasta}")
    
    arquivos_pdf = list(caminho_da_pasta.glob("*.pdf"))
    if not arquivos_pdf:
        logging.warning(f"Nenhum arquivo PDF encontrado em {caminho_da_pasta}")
        return {}

    for caminho_arquivo in arquivos_pdf:
        logging.info(f"Extraindo texto de: {caminho_arquivo.name}")
        texto = extrair_texto(caminho_arquivo)
        # Adiciona ao dicionário apenas se a extração foi bem-sucedida
        if texto:
            textos_dos_documentos[caminho_arquivo.name] = texto
            
    return textos_dos_documentos