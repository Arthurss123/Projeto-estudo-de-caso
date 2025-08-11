
from pathlib import Path
import time
import re

from extracao import processar_pasta, extrair_texto
from classificar import ClassificadorDocumentos, gerar_rotulo_automatico
from busca import criar_indice, buscar
from chat import gerar_resposta_com_contexto

PASTA_PROJETO = Path(__file__).parent.parent
PASTA_DADOS = PASTA_PROJETO / "data"
PASTA_INDICE = PASTA_PROJETO / "indice_whoosh"
ARQUIVO_CLASSIFICADOR = PASTA_PROJETO / "classificador.pkl"

def encontrar_arquivo_correspondente(query_usuario: str) -> str | None:
    if not PASTA_DADOS.is_dir():
        return None
    query_normalizada = re.sub(r'[\s_.-]', '', query_usuario).lower()

    correspondencias = []
    arquivos_disponiveis = [f.name for f in PASTA_DADOS.glob("*.pdf")]

    for nome_arquivo in arquivos_disponiveis:
        nome_normalizado = re.sub(r'[\s_.-]', '', nome_arquivo.replace('.pdf', '')).lower()
        
        if nome_normalizado.startswith(query_normalizada):
            correspondencias.append(nome_arquivo)

    if len(correspondencias) == 1:
        print(f"Arquivo encontrado: {correspondencias[0]}")
        return correspondencias[0]
    
    elif len(correspondencias) > 1:
        print("Muitos arquivos são iguais em sua busca. Qual deles você quer?")
        for i, nome in enumerate(correspondencias):
            print(f"  [{i+1}] {nome}")
        
        try:
            escolha = int(input(">> Digite o número do arquivo desejado: "))
            if 1 <= escolha <= len(correspondencias):
                return correspondencias[escolha - 1]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return None
            
    else:
        print(f"Nenhum arquivo correspondente a '{query_usuario}' foi encontrado.")
        return None

def preparar_ambiente():
    print("INICIANDO PREPARAÇÃO")
    if not PASTA_DADOS.is_dir() or not any(PASTA_DADOS.glob('*.pdf')):
        print(f"Pasta '{PASTA_DADOS}' não encontrada ou está vazia.")
        return
    print("\nExtraindo texto dos PDFs...")
    documentos = processar_pasta(PASTA_DADOS)
    print("\nTreinando modelo de classificação...")
    textos, nomes_arquivos = list(documentos.values()), list(documentos.keys())
    rotulos = [gerar_rotulo_automatico(nome) for nome in nomes_arquivos]
    classificador = ClassificadorDocumentos()
    classificador.treinar(textos, rotulos)
    classificador.salvar(str(ARQUIVO_CLASSIFICADOR))
    print("\nCriando índice de busca...")
    criar_indice(str(PASTA_INDICE), documentos)
    print("\nPREPARAÇÃO CONCLUÍDA")


def executar_busca(query: str):
    # ... (esta função não muda)
    if not PASTA_INDICE.is_dir():
        print("O ambiente ainda não foi preparado. Escolha a opção [1] primeiro.")
        return
    print(f"\n🔎 Buscando por: '{query}'")
    resultados = buscar(str(PASTA_INDICE), query)
    if not resultados: print("Nenhum documento relevante encontrado.")
    else:
        print("\nResultados da Busca")
        for res in resultados:
            print(f"Arquivo: {res['nome_arquivo']} (Score: {res['score']:.2f})")
            print(f"   Trecho: ...{res['trecho_relevante'].replace(chr(10), ' ')}...")
            print("-" * 20)


def executar_chat(busca_arquivo: str, pergunta: str):
    nome_arquivo = encontrar_arquivo_correspondente(busca_arquivo)

    if not nome_arquivo:
        return

    caminho_arquivo = PASTA_DADOS / nome_arquivo
    
    print(f"Carregando '{nome_arquivo}'para o chat")
    contexto = extrair_texto(caminho_arquivo)
    
    if not contexto.strip():
        print(f"Não foi possível extrair texto do '{nome_arquivo}'.")
        return
    
    print("Gerando")
    resposta = gerar_resposta_com_contexto(pergunta, contexto)
    print("\n--- Resposta do llm ---")
    print(resposta)

def main():
    while True:
        print("\n" + "="*40)
        print("CONSULTA INTELIGENTE DE PDFS")
        print("="*40)
        print("\nO que você gostaria de fazer?")
        print("[1] Preparar Ambiente (executar apenas uma vez)")
        print("[2] Buscar por um termo em todos os documentos")
        print("[3] Conversar com um documento específico (aqui se utiliza LLM)")
        print("[4] Sair")
        
        escolha = input(">> Digite o número da sua escolha: ")

        if escolha == '1':
            preparar_ambiente()
        elif escolha == '2':
            query = input("Digite o que você deseja buscar: ")
            executar_busca(query)
        elif escolha == '3':
            busca_arquivo = input("Digite parte do nome do arquivo: ")
            pergunta = input("Qual é a sua pergunta sobre este documento?: ")
            executar_chat(busca_arquivo, pergunta)
        elif escolha == '4':
            print("\nSaindo do programa.")
            time.sleep(1)
            break
        else:
            print("\nOpção inválida! Por favor, digite um número de 1 a 4.")
            time.sleep(2)
        
        input("\nPressione Enter para continuar")
if __name__ == "__main__":
    main()