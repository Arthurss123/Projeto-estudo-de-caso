from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import re

def regra_tipo_documento(nome_arquivo: str, texto: str) -> str:
    """
    Define a classe usando hierarquia:
    1. Nome do arquivo
    2. Cabeçalho do texto
    3. Retorna None caso precise usar o modelo
    """
    nome = nome_arquivo.lower()

    # 1️⃣ Prioriza o nome do arquivo
    if "lei" in nome:
        return "Lei"
    if "portaria" in nome:
        return "Portaria"
    if "resolucao" in nome or "resolução" in nome:
        return "Resolucao"

    # 2️⃣ Se o nome não define, analisa cabeçalho do texto
    cabecalho = texto.upper()[:2000]
    if re.search(r"LEI\s*N[º°]", cabecalho):
        return "Lei"
    if re.search(r"PORTARIA\s*N[º°]", cabecalho):
        return "Portaria"
    if re.search(r"RESOLUÇÃO?\s*N[º°]", cabecalho):
        return "Resolucao"

    # 3️⃣ Se nada foi encontrado, deixa o modelo decidir
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
        print("✅ Modelo treinado com sucesso!")

    def classificar(self, nome_arquivo: str, texto: str) -> str:
        """
        Classificação híbrida:
        1. Nome → 2. Cabeçalho → 3. Modelo.
        """
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
    """
    Define um rótulo inicial usando o nome do arquivo como pista.
    """
    nome = nome_arquivo.lower()
    if "lei" in nome:
        return "Lei"
    elif "portaria" in nome:
        return "Portaria"
    elif "resolucao" in nome or "resolução" in nome:
        return "Resolucao"
    else:
        return "Outro"


if __name__ == '__main__':
    from extracao import processar_pasta

    dados = processar_pasta("data")
    if not dados:
        raise RuntimeError("❌ Nenhum arquivo processado. Verifique o caminho dos PDFs.")

    textos_treino = list(dados.values())
    nomes_arquivos_treino = list(dados.keys())

    rotulos_treino = [gerar_rotulo_automatico(nome) for nome in nomes_arquivos_treino]
    print("📌 Rótulos atribuídos automaticamente:", rotulos_treino)

    classificador = ClassificadorDocumentos()
    classificador.treinar(textos_treino, rotulos_treino)
    classificador.salvar()

    modelo_carregado = ClassificadorDocumentos.carregar_modelo()
    if modelo_carregado:
        print("\n📊 Resultados da classificação de todos os arquivos:")
        for nome, texto in zip(nomes_arquivos_treino, textos_treino):
            previsao = modelo_carregado.classificar(nome, texto)
            print(f"📄 {nome} → {previsao}")
