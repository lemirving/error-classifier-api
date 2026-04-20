import os
from supabase import create_client, Client
from dotenv import load_dotenv
from jose import jwt


load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str= os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(url,key)

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

def validar_professor(token:str):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=[ALGORITHM],
            audience="authenticated"
        )
        return payload
    except Exception as e:
        print(f"Erro na validação:{e}")
        return None
    