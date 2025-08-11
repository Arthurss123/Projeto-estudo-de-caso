# Projeto: Consulta Inteligente de PDFs Jurídicos

Este projeto é uma ferramenta para extração, classificação, busca e consulta inteligente em documentos PDF jurídicos, usando técnicas de processamento de texto, aprendizado de máquina e modelos de linguagem (LLM).

---
## Funcionalidades principais

- **Extração de texto** de PDFs em uma pasta.
- **Classificação automática** dos documentos em categorias (Lei, Portaria, Resolução, Outro) combinando regras e modelo ML.
- **Indexação e busca textual** Usando Whoosh, com resultados relevantes e trechos destacados.
- **Consulta conversacional (chat)** com documentos, usando o modelo de linguagem Ollama para responder perguntas baseadas no conteúdo do PDF.

---
## Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- **Dependências Python**:
  - pdfplumber
  - scikit-learn
  - whoosh
  - ollama (cliente Python, e Ollama instalado no sistema, não é necessário o uso de GPU)
---
## Instalação

1. Clone este repositório:
   ```bash
   git clone <[https://github.com/Arthurss123/Projeto-estudo-de-caso.git]>
   cd <nome-pasta-salvar>
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
2. Instale o Ollama e certifique-se que ele está rodando localmente:
   ```bash
   ollama run gemma:2b
## Como usar

1. Preparar o ambiente (executar **uma vez** após adicionar PDFs):

- Coloque seus arquivos PDF dentro da pasta `data/`.
- Execute o script principal:
```
python app/main.py
```
No menu, escolha:
```bash
[1] Preparar Ambiente (executar apenas uma vez)
```
Esse processo irá:
-   Extrair texto de todos os PDFs na pasta `data/`.
-   Treinar o classificador automático para identificar o tipo de documento.
-   Criar o índice de busca para os textos extraídos.

2. Buscar termos nos documentos
escolha:
```bash
[2] Buscar por um termo em todos os documentos
```

Digite a palavra, frase ou expressão que deseja pesquisar. O sistema mostrará os documentos relevantes com trechos destacados e uma pontuação de relevância


3. Conversar com um documento específico (Chat)
escolha:
```bash
[3] Conversar com um documento específico (aqui se utiliza LLM)
```
1.  Digite parte do nome do arquivo para localizar o documento.
    
2.  Se houver múltiplos arquivos correspondentes, escolha o desejado.
    
3.  Digite a pergunta que deseja fazer sobre o documento.
    

O modelo responderá com base no conteúdo do documento, sem inventar informações.

---
## Desenvolvimento e manutenção

-   Para atualizar os documentos ou falar sobre novos documentos, basta colocar os novos PDFs na pasta `data/` e executar novamente a preparação (opção 1).
