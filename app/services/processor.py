import os
import language_tool_python
import httpx  # Recomendado para chamar a sua API de IA

IA_SERVICE_URL = os.getenv("IA_SERVICE_URL");

# Inicializa a ferramenta uma única vez no carregamento do módulo
async def processar_texto_completo(texto: str):
    tool = language_tool_python.LanguageTool('pt-BR')
    matches = tool.check(texto)
    duplas_para_ia = []
    
    for match in matches:
        if match.replacements:
            incorreta = texto[match.offset : match.offset + match.error_length]
            correta = match.replacements[0]
            duplas_para_ia.append({"errada": incorreta, "correta": correta})

    if not duplas_para_ia:
        return []

    # 2. Chamada para a API de IA
    async with httpx.AsyncClient() as client:
        try:
            # Envelopa a lista dentro de um dicionário com a chave "items"
            payload = {"items": duplas_para_ia} 
            # Use o argumento timeout se a IA demorar um pouco na primeira chamada
            response = await client.post(IA_SERVICE_URL, json=payload, timeout=30.0)
            
            response.raise_for_status() # Levanta erro se não for 200 OK
            return response.json()
        except Exception as e:
            return {"erro": "IA Service offline", "detalhes": str(e)}