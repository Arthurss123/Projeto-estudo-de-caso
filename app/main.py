# app/main.py

from pathlib import Path
import time
import re

# Importa as ferramentas dos outros arquivos
from extracao import processar_pasta, extrair_texto
from classificar import ClassificadorDocumentos, gerar_rotulo_automatico
from busca import criar_indice, buscar
from chat import gerar_resposta_com_contexto

# --- Configuração de Caminhos ---
# (Esta parte continua igual)
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
        print(f"✅ Arquivo encontrado: {correspondencias[0]}")
        return correspondencias[0]
    
    elif len(correspondencias) > 1:
        print("Múltiplos arquivos correspondem à sua busca. Qual deles você quer?")
        for i, nome in enumerate(correspondencias):
            print(f"  [{i+1}] {nome}")
        
        try:
            escolha = int(input(">> Digite o número do arquivo desejado: "))
            if 1 <= escolha <= len(correspondencias):
                return correspondencias[escolha - 1]
        except (ValueError, IndexError):
            print("❌ Escolha inválida.")
            return None
            
    else:
        print(f"❌ Nenhum arquivo correspondente a '{query_usuario}' foi encontrado.")
        return None

def preparar_ambiente():
    # ... (esta função não muda)
    print("--- INICIANDO PREPARAÇÃO COMPLETA ---")
    if not PASTA_DADOS.is_dir() or not any(PASTA_DADOS.glob('*.pdf')):
        print(f"❌ ERRO: Pasta '{PASTA_DADOS}' não encontrada ou está vazia. Adicione seus PDFs.")
        return
    print("\n[1/3] Extraindo texto dos PDFs...")
    documentos = processar_pasta(PASTA_DADOS)
    print("\n[2/3] Treinando modelo de classificação...")
    textos, nomes_arquivos = list(documentos.values()), list(documentos.keys())
    rotulos = [gerar_rotulo_automatico(nome) for nome in nomes_arquivos]
    classificador = ClassificadorDocumentos()
    classificador.treinar(textos, rotulos)
    classificador.salvar(str(ARQUIVO_CLASSIFICADOR))
    print("\n[3/3] Criando índice de busca...")
    criar_indice(str(PASTA_INDICE), documentos)
    print("\n✅ PREPARAÇÃO CONCLUÍDA!")


def executar_busca(query: str):
    # ... (esta função não muda)
    if not PASTA_INDICE.is_dir():
        print("❌ ERRO: O ambiente ainda não foi preparado. Escolha a opção [1] primeiro.")
        return
    print(f"\n🔎 Buscando por: '{query}'")
    resultados = buscar(str(PASTA_INDICE), query)
    if not resultados: print("Nenhum documento relevante encontrado.")
    else:
        print("\n--- Resultados da Busca ---")
        for res in resultados:
            print(f"📄 Arquivo: {res['nome_arquivo']} (Score: {res['score']:.2f})")
            print(f"   Trecho: ...{res['trecho_relevante'].replace(chr(10), ' ')}...")
            print("-" * 20)


def executar_chat(busca_arquivo: str, pergunta: str):
    # --- MUDANÇA PRINCIPAL AQUI ---
    # Em vez de usar a busca_arquivo diretamente, usamos nossa função inteligente
    nome_exato_arquivo = encontrar_arquivo_correspondente(busca_arquivo)
    
    # Se a função não encontrar um arquivo claro, ela para aqui.
    if not nome_exato_arquivo:
        return

    caminho_arquivo = PASTA_DADOS / nome_exato_arquivo
    
    print(f"Carregando '{nome_exato_arquivo}' para o chat...")
    contexto = extrair_texto(caminho_arquivo)
    
    if not contexto.strip():
        print(f"❌ ERRO: Não foi possível extrair texto do '{nome_exato_arquivo}'.")
        return
    
    print("🤖 LLM está pensando... (Isso pode levar um momento)")
    resposta = gerar_resposta_com_contexto(pergunta, contexto)
    print("\n--- Resposta do Assistente ---")
    print(resposta)


# --- Loop Principal do Menu Interativo (com texto de ajuda alterado) ---

def main():
    while True:
        print("\n" + "="*40)
        print("    CONSULTA INTELIGENTE DE PDFS    ")
        print("="*40)
        print("\nO que você gostaria de fazer?")
        print("[1] Preparar Ambiente (executar apenas uma vez)")
        print("[2] Buscar por um termo em todos os documentos")
        print("[3] Conversar com um documento específico (Chat)")
        print("[4] Sair")
        
        escolha = input(">> Digite o número da sua escolha: ")

        if escolha == '1':
            preparar_ambiente()
        elif escolha == '2':
            query = input("🔎 Digite o que você deseja buscar: ")
            executar_busca(query)
        elif escolha == '3':
            # --- MUDANÇA NO TEXTO DE AJUDA AQUI ---
            busca_arquivo = input("📄 Digite parte do nome do arquivo (ex: lei 9394): ")
            pergunta = input("❓ Qual é a sua pergunta sobre este documento?: ")
            executar_chat(busca_arquivo, pergunta)
        elif escolha == '4':
            print("\nSaindo do programa. Até logo!")
            time.sleep(1)
            break
        else:
            print("\n❌ Opção inválida! Por favor, digite um número de 1 a 4.")
            time.sleep(2)
        
        input("\n-- Pressione Enter para continuar --")


if __name__ == "__main__":
    main()