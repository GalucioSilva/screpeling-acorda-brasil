# Usamos uma imagem Python oficial como base
FROM python:3.12-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar requirements primeiro para aproveitar cache no build
COPY requirements.txt .

# Instalar dependências
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar o restante do código
COPY . .

# Comando padrão: abre o shell do Scrapy
CMD ["scrapy"]
