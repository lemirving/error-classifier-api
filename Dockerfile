# Usamos uma imagem leve do Python
FROM python:3.11-slim

# Definimos a pasta de trabalho
WORKDIR /app

# Instala o Java (JRE) - Necessário para o LanguageTool
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN python -c "import language_tool_python; language_tool_python.LanguageTool('pt-BR')"

# Copia o restante do código
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para iniciar
# No Dockerfile, altere o CMD para:
CMD ["sh", "-c", "export _JAVA_OPTIONS='-Xmx256m' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]