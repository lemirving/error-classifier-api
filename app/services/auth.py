from fastapi import Depends, HTTPException, Header

from app.database import validar_professor

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token faltando")
    
    # Remove o 'Bearer ' do cabeçalho
    token = authorization.replace("Bearer ", "")
    user = validar_professor(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    return user

