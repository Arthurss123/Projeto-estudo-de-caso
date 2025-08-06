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