FROM python:3.12-slim

WORKDIR /app

# Dependências para Scrapy + Chromium headless
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libssl-dev \
    python3-dev \
    curl \
    wget \
    gnupg \
    # libs do chromium
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    fonts-liberation \
    libgtk-3-0 \
    fonts-unifont \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar playwright + scrapy-playwright
RUN pip install --no-cache-dir playwright scrapy-playwright \
    && playwright install chromium   # << sem --with-deps

# Copiar código
COPY . .

ENTRYPOINT ["scrapy"]
