import os
import httpx
import language_tool_python
import traceback
from app.database import supabase 

IA_SERVICE_URL = os.getenv("IA_SERVICE_URL")

# INICIALIZAÇÃO GLOBAL (Fora das funções para economizar RAM e CPU)
# Usando remote_server para não precisar de Java no Render
tool = language_tool_python.LanguageTool('pt-BR', remote_server='https://api.languagetool.org/')

async def processar_texto_completo(texto: str):
    try:
        # Usa a tool global já inicializada
        matches = tool.check(texto)
        
        duplas_para_ia = []
        for match in matches:
            if match.replacements:
                # Use match.length (mais seguro que error_length em algumas versões)
                incorreta = texto[match.offset : match.offset + match.length]
                correta = match.replacements[0]
                duplas_para_ia.append({"errada": incorreta, "correta": correta})

        if not duplas_para_ia:
            return []

        async with httpx.AsyncClient() as client:
            payload = {"items": duplas_para_ia} 
            response = await client.post(IA_SERVICE_URL, json=payload, timeout=40.0)
            response.raise_for_status()
            return response.json() 
    except Exception as e:
        print(f"Erro na IA/LanguageTool: {e}")
        return None

async def task_processar_e_persistir(text_id: str, text: str):
    print(f"--- INICIANDO TASK PARA TEXTO {text_id} ---")
    try:
        resultado_ia = await processar_texto_completo(text)
        
        if resultado_ia is None:
            supabase.table("texts").update({"status": "error"}).eq("id", text_id).execute()
            return

        if not resultado_ia:
            supabase.table("texts").update({"status": "revised"}).eq("id", text_id).execute()
            return

        # Prepara o Bulk Insert (MUITO mais eficiente que loop)
        errors_to_save = [
            {
                "text_id": text_id,
                "word_found": erro.get("errada"),
                "suggestion": erro.get("correta"),
                "classification": erro.get("classe", "ortografia"),
                "is_corrected": False
            } for erro in resultado_ia
        ]

        if errors_to_save:
            print(f"Tentando salvar {len(errors_to_save)} erros no Supabase...")
            # IMPORTANTE: Use colunas que existem no seu schema do DB!
            supabase.table("spelling_errors").insert(errors_to_save).execute()
        
        supabase.table("texts").update({"status": "revised"}).eq("id", text_id).execute()
        print(f"--- TEXTO {text_id} FINALIZADO COM SUCESSO ---")

    except Exception as e:
        print(f"!!! ERRO CRÍTICO NA TASK: {str(e)}")
        traceback.print_exc()
        supabase.table("texts").update({"status": "error"}).eq("id", text_id).execute()