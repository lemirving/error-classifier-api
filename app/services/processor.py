import os
import httpx
import language_tool_python
from app.database import supabase # Garanta que o cliente supabase esteja aqui

IA_SERVICE_URL = os.getenv("IA_SERVICE_URL")

async def processar_texto_completo(texto: str):
    # 1. Gramática e Ortografia com LanguageTool Remoto
    tool = language_tool_python.LanguageTool('pt-BR', remote_server='https://api.languagetool.org/')
    matches = tool.check(texto)
    
    duplas_para_ia = []
    for match in matches:
        if match.replacements:
            incorreta = texto[match.offset : match.offset + match.error_length]
            correta = match.replacements[0]
            duplas_para_ia.append({"errada": incorreta, "correta": correta})

    if not duplas_para_ia:
        return []

    # 2. Chamada para a sua API de IA (Hugging Face / Classifier)
    async with httpx.AsyncClient() as client:
        try:
            payload = {"items": duplas_para_ia} 
            response = await client.post(IA_SERVICE_URL, json=payload, timeout=40.0)
            response.raise_for_status()
            
            # O retorno esperado é a lista de erros já com a 'classe'
            return response.json() 
        except Exception as e:
            print(f"Erro na IA: {e}")
            return None # Retornamos None para indicar falha crítica no processamento

async def task_processar_e_persistir(text_id: str, text: str):
    # 1. Obtém os resultados (IA + LanguageTool)
    resultado_ia = await processar_texto_completo(text)
    
    # Se a IA falhou ou não encontrou erros, tratamos aqui
    if resultado_ia is None:
        supabase.table("texts").update({"status": "error"}).eq("id", text_id).execute()
        return

    if not resultado_ia:
        # Se não há erros, apenas finaliza como revisado
        supabase.table("texts").update({"status": "revised"}).eq("id", text_id).execute()
        return

    # 2. Prepara o Bulk Insert para a tabela spelling_errors
    # Mapeamos o retorno da IA para os nomes das colunas no seu banco
    errors_to_save = [
        {
            "text_id": text_id,
            "word_found": erro.get("errada"),
            "suggestion": erro.get("correta"),
            "classification": erro.get("classe", "ortografia"), # Fallback caso falte a classe
            "is_corrected": False
        } for erro in resultado_ia
    ]

    try:
        # 3. Persistência no Supabase
        if errors_to_save:
            supabase.table("spelling_errors").insert(errors_to_save).execute()
        
        # 4. Atualiza o status na tabela principal
        supabase.table("texts").update({"status": "revised"}).eq("id", text_id).execute()
        print(f"Sucesso: Texto {text_id} processado e salvo.")
        
    except Exception as e:
        print(f"Erro ao persistir no banco: {e}")
        supabase.table("texts").update({"status": "error"}).eq("id", text_id).execute()