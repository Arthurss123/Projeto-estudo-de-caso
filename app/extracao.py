import pdfplumber
import os

def extrair_texto(caminho_do_arquivo: str) -> str:
  texto_completo = ""
  try:
    with pdfplumber.open(caminho_do_arquivo) as pdf:
      for pagina in pdf.pages:
        texto_da_pagina = pagina.extract_text()
        if texto_da_pagina:
          texto_completo += texto_da_pagina + "\n"
    return texto_completo
  except Exception as e:
    print("Erro no arquivo")
    return ""
  
def processar_pasta (caminho_da_pasta: str) -> dict:
  textos_dos_documentos = {}
  for nome_arquivo in os.listdir(caminho_da_pasta):
    if nome_arquivo.lower().endswith(".pdf"):
      caminho_completo = os.path.join(caminho_da_pasta, nome_arquivo)
      print(f"Extraindo texto de: {nome_arquivo}")
      textos_dos_documentos[nome_arquivo] = extrair_texto(caminho_completo)
  return textos_dos_documentos

if __name__ == '__main__':
    dados_extraidos = processar_pasta("data")
    for nome, texto in dados_extraidos.items():
        print(f"--- Documento: {nome} ---")
        print(f"{texto[:200]}...")
        print("-" * 20)