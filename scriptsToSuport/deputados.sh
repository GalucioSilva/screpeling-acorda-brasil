#!/usr/bin/env bash
set -euo pipefail

# Diretório de saída
OUT_DIR="./data"
mkdir -p "$OUT_DIR"

# Arquivo de saída
OUT_FILE="$OUT_DIR/deputados.json"

# Endpoint oficial da Câmara (lista de deputados em exercício - JSON nativo)
URL="https://dadosabertos.camara.leg.br/api/v2/deputados"

echo "Baixando lista de deputados da Câmara dos Deputados..."
curl -s -H "Accept: application/json" "$URL" | jq '.' > "$OUT_FILE"

if [ -s "$OUT_FILE" ]; then
  echo "✅ Dados de deputados salvos em: $OUT_FILE"
else
  echo "❌ Erro: arquivo $OUT_FILE está vazio"
  exit 1
fi