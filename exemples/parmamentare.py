#!/usr/bin/env python3
import os
import json
import requests
import xml.etree.ElementTree as ET

# Diretório de saída
OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

# Arquivos de saída
FILE_DEPUTADOS = os.path.join(OUT_DIR, "deputados.json")
FILE_SENADORES = os.path.join(OUT_DIR, "senadores.json")

# URLs das APIs
URL_DEPUTADOS = "https://dadosabertos.camara.leg.br/api/v2/deputados"
URL_SENADORES = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual"


def baixar_deputados():
    print("📥 Baixando lista de deputados...")
    resp = requests.get(URL_DEPUTADOS, headers={"Accept": "application/json"})
    resp.raise_for_status()
    data = resp.json()

    with open(FILE_DEPUTADOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Deputados salvos em {FILE_DEPUTADOS}")


def baixar_senadores():
    print("📥 Baixando lista de senadores...")
    resp = requests.get(URL_SENADORES)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)

    senadores = []
    for senador in root.findall(".//Parlamentar"):
        s = {
            "id": senador.findtext("IdentificacaoParlamentar/CodigoParlamentar"),
            "nome": senador.findtext("IdentificacaoParlamentar/NomeParlamentar"),
            "nomeCompleto": senador.findtext("IdentificacaoParlamentar/NomeCompletoParlamentar"),
            "sexo": senador.findtext("IdentificacaoParlamentar/SexoParlamentar"),
            "uf": senador.findtext("IdentificacaoParlamentar/UFParlamentar"),
            "partido": senador.findtext("IdentificacaoParlamentar/SiglaPartidoParlamentar"),
            "email": senador.findtext("IdentificacaoParlamentar/EmailParlamentar"),
        }
        senadores.append(s)

    with open(FILE_SENADORES, "w", encoding="utf-8") as f:
        json.dump(senadores, f, indent=2, ensure_ascii=False)

    print(f"✅ Senadores salvos em {FILE_SENADORES}")


if __name__ == "__main__":
    try:
        baixar_deputados()
        baixar_senadores()
        print("🎉 Concluído com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
