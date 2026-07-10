FROM python:3.11-slim

WORKDIR /app

# 1. Instala o Java (JRE) que o LanguageTool exige para rodar o motor de correção
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Usamos a variável $PORT que o Render injeta automaticamente para não engessar na porta 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]