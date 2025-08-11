from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import re
def regra_tipo_documento(nome_arquivo: str, texto: str) -> str:

    nome = nome_arquivo.lower()

    if "lei" in nome:
        return "Lei"
    if "portaria" in nome:
        return "Portaria"
    if "resolucao" in nome or "resolução" in nome:
        return "Resolucao"

    #Se o nome não define, analisa cabeçalho do texto
    cabecalho = texto.upper()[:2000]
    if re.search(r"LEI\s*N[º°]", cabecalho):
        return "Lei"
    if re.search(r"PORTARIA\s*N[º°]", cabecalho):
        return "Portaria"
    if re.search(r"RESOLUÇÃO?\s*N[º°]", cabecalho):
        return "Resolucao"
    return None

class ClassificadorDocumentos:
    def __init__(self):
        self.modelo = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())
        self.classes = []

    def treinar(self, textos: list, rotulos: list):
        if len(textos) != len(rotulos):
            raise ValueError(
                f"Número de textos ({len(textos)}) diferente do número de rótulos ({len(rotulos)})!"
            )
        self.classes = sorted(list(set(rotulos)))
        self.modelo.fit(textos, rotulos)
        print("Modelo treinado com sucesso!")

    def classificar(self, nome_arquivo: str, texto: str) -> str:
        tipo_regra = regra_tipo_documento(nome_arquivo, texto)
        if tipo_regra:
            return tipo_regra
        return self.modelo.predict([texto])[0]

    def salvar(self, caminho="classificador.pkl"):
        with open(caminho, "wb") as f:
            pickle.dump(self, f)
        print(f"✅ Modelo salvo em {caminho}")

    @staticmethod
    def carregar_modelo(caminho="classificador.pkl"):
        try:
            with open(caminho, "rb") as f:
                modelo = pickle.load(f)
            print(f"✅ Modelo carregado de {caminho}")
            return modelo
        except FileNotFoundError:
            print("❌ Arquivo de modelo não encontrado.")
            return None
        
def gerar_rotulo_automatico(nome_arquivo: str) -> str:
    nome = nome_arquivo.lower()
    if "lei" in nome:
        return "Lei"
    elif "portaria" in nome:
        return "Portaria"
    elif "resolucao" in nome or "resolução" in nome:
        return "Resolucao"
    else:
        return "Outro"