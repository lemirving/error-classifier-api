import httpx
from typing import List, Dict, Any
from app.config import settings

class HuggingFaceClient:
    def __init__(self):

        self.space_url = "https://irvinglem-ia-pibec-corrector.hf.space/predict"
        
        self.headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }

    async def classificar_erros(self, pares_texto: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Envia os pares (errada, correta) para o classificador no Hugging Face.
        Espera uma lista de dicionários contendo os campos: errada, correta, classe, reconhecida, diff.
        """
        payload = {
            "items": pares_texto
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.space_url, json=payload, headers=self.headers)
                
                if response.status_code != 200:
                    raise Exception(f"Erro no Hugging Face Space: Status {response.status_code}")
                
                return response.json()
                
            except httpx.RequestError as exc:
                raise Exception(f"Falha de rede ao conectar com o modelo de IA: {exc}")