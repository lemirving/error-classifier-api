# Usamos uma imagem leve do Python
FROM python:3.11-slim

# Definimos a pasta de trabalho dentro do container
WORKDIR /app

# Instala o Java (JRE) para o LanguageTool rodar localmente sem limites
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu código (a pasta app, rotas, etc) para dentro do container
COPY . .

# Expõe a porta padrão da API
EXPOSE 8000

# O comando exato que acabamos de usar no terminal para ligar o Uvicorn, 
# mas escutando em todos os IPs (0.0.0.0) para a internet conseguir acessar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]