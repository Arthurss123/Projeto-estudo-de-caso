# app/chat.py

import ollama

def gerar_resposta_com_contexto(prompt: str, contexto: str) -> str:
    prompt_completo = f"""
    Você é um assistente de IA especialista em análise de documentos.
    Sua tarefa é responder à pergunta do usuário baseando-se estritamente no texto do documento fornecido abaixo.
    Não invente informações que não estejam no texto. Se a resposta não estiver no documento, diga "A informação não foi encontrada no documento fornecido."

    --- CONTEXTO DO DOCUMENTO ---
    {contexto}
    --- FIM DO CONTEXTO ---

    PERGUNTA DO USUÁRIO: {prompt}

    RESPOSTA:
    """

    try:
        response = ollama.chat(
            model='gemma:2b',
            messages=[
                {'role': 'user', 'content': prompt_completo},
            ]
        )
        return response['message']['content']
    except Exception as e:
        # Fornece um erro mais detalhado
        error_message = str(e)
        if "llama_new_context_with_model" in error_message:
             return "Erro de conexão com o Ollama.."
        return f"Erro ao contatar o modelo LLM: {e}"