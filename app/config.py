from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    HUGGINGFACE_API_KEY: str
    # A URL de chaves do Clerk (JWKS) para validar o token no backend
    # Geralmente fica no painel do seu Clerk: https://<your-clerk-instance>/.well-known/jwks.json
    CLERK_JWKS_URL: str 

    # Faz o Pydantic ler o arquivo .env automaticamente
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instancia as configurações para importarmos nas outras partes do código
settings = Settings()