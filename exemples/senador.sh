#!/usr/bin/env bash
set -euo pipefail

# Diretório de saída
OUT_DIR="./data"
mkdir -p "$OUT_DIR"

# Arquivo de saída
OUT_FILE="$OUT_DIR/senadores.json"

# Endpoint oficial do Senado (lista de senadores em exercício - XML)
URL="https://legis.senado.leg.br/dadosabertos/senador/lista/atual"

echo "Baixando lista de senadores do Senado Federal..."
curl -s "$URL" | yq -p=xml -o=json > "$OUT_FILE"

if [ -s "$OUT_FILE" ]; then
  echo "✅ Dados de senadores salvos em: $OUT_FILE"
else
  echo "❌ Erro: arquivo $OUT_FILE está vazio"
  exit 1
fi