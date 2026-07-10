import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

security = HTTPBearer()

clerk_jwks_cache = None

async def get_clerk_jwks():
    global clerk_jwks_cache
    if clerk_jwks_cache is None:
        from app.config import settings
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.CLERK_JWKS_URL)
            if response.status_code == 200:
                clerk_jwks_cache = response.json()
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="Não foi possível obter as chaves de verificação do Clerk."
                )
    return clerk_jwks_cache

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwks = Depends(get_clerk_jwks)
):
    token = credentials.credentials
    
    try:
        
        payload = jwt.decode(
            token, 
            jwks, 
            algorithms=["RS256"], 
            options={"verify_aud": False} # Geralmente o Clerk não exige a validação do aud no backend direto
        )
        
        clerk_user_id = payload.get("sub")
        if not clerk_user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID do usuário ausente."
            )
            
        # Retorna o ID do Clerk para a rota saber quem disparou a correção
        return {"clerk_user_id": clerk_user_id}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="O token de sessão expirou. Faça login novamente."
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido ou corrompido."
        )