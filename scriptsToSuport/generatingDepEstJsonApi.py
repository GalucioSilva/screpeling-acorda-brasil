# Re-generate the JSON file with the matrix of state assemblies and strategies
import json, datetime, os

today = datetime.date.today().isoformat()

schema = {
    "version": "1.0",
    "generated_at": today,
    "notes": (
        "Matriz inicial para coleta de deputados(as) ESTADUAIS em exercício por UF. "
        "Campos 'strategy': 'api' (endpoint JSON/CSV), 'sapl' (API do SAPL/Interlegis), 'html' (scraping)."
    ),
    "items": []
}

rows = [
    ("AC", "Acre", "Assembleia Legislativa do Estado do Acre", "sapl", [
        "https://sapl.al.ac.leg.br/api/schema/swagger-ui/"
    ]),
    ("AL", "Alagoas", "Assembleia Legislativa do Estado de Alagoas", "html", []),
    ("AM", "Amazonas", "Assembleia Legislativa do Estado do Amazonas", "html", []),
    ("AP", "Amapá", "Assembleia Legislativa do Estado do Amapá", "html", []),
    ("BA", "Bahia", "Assembleia Legislativa do Estado da Bahia", "api", [
        "https://albalegis.nopapercloud.com.br/dados-abertos.aspx"
    ]),
    ("CE", "Ceará", "Assembleia Legislativa do Estado do Ceará", "api", [
        "https://www2.al.ce.gov.br/api/"
    ]),
    ("DF", "Distrito Federal", "Câmara Legislativa do Distrito Federal", "api", [
        "https://dadosabertos.cl.df.leg.br/"
    ]),
    ("ES", "Espírito Santo", "Assembleia Legislativa do Estado do Espírito Santo", "api", [
        "https://www.al.es.gov.br/dados-abertos"
    ]),
    ("GO", "Goiás", "Assembleia Legislativa do Estado de Goiás", "html", []),
    ("MA", "Maranhão", "Assembleia Legislativa do Estado do Maranhão", "html", []),
    ("MG", "Minas Gerais", "Assembleia Legislativa do Estado de Minas Gerais", "api", [
        "https://dadosabertos.almg.gov.br/api/"
    ]),
    ("MS", "Mato Grosso do Sul", "Assembleia Legislativa do Estado de Mato Grosso do Sul", "html", []),
    ("MT", "Mato Grosso", "Assembleia Legislativa do Estado de Mato Grosso", "html", []),
    ("PA", "Pará", "Assembleia Legislativa do Estado do Pará", "html", []),
    ("PB", "Paraíba", "Assembleia Legislativa do Estado da Paraíba", "html", []),
    ("PE", "Pernambuco", "Assembleia Legislativa do Estado de Pernambuco", "html", []),
    ("PI", "Piauí", "Assembleia Legislativa do Estado do Piauí", "html", []),
    ("PR", "Paraná", "Assembleia Legislativa do Estado do Paraná", "api", [
        "https://transparencia.assembleia.pr.leg.br/servicos/dados-abertos"
    ]),
    ("RJ", "Rio de Janeiro", "Assembleia Legislativa do Estado do Rio de Janeiro", "html", []),
    ("RN", "Rio Grande do Norte", "Assembleia Legislativa do Estado do Rio Grande do Norte", "html", []),
    ("RO", "Rondônia", "Assembleia Legislativa do Estado de Rondônia", "api", [
        "https://transparencia.al.ro.leg.br/DadosAbertos/"
    ]),
    ("RR", "Roraima", "Assembleia Legislativa do Estado de Roraima", "html", []),
    ("RS", "Rio Grande do Sul", "Assembleia Legislativa do Estado do Rio Grande do Sul", "html", []),
    ("SC", "Santa Catarina", "Assembleia Legislativa do Estado de Santa Catarina", "html", []),
    ("SE", "Sergipe", "Assembleia Legislativa do Estado de Sergipe", "html", []),
    ("SP", "São Paulo", "Assembleia Legislativa do Estado de São Paulo", "api", [
        "https://www.al.sp.gov.br/repositorioDados/deputados/"
    ]),
    ("TO", "Tocantins", "Assembleia Legislativa do Estado do Tocantins", "html", []),
]

for uf, estado, nome, strategy, endpoints in rows:
    schema["items"].append({
        "uf": uf,
        "estado": estado,
        "assembleia_nome": nome,
        "strategy": strategy,
        "status": "needs_verification",
        "endpoints": endpoints,
        "listing_url": "",
        "notes": ""
    })

os.makedirs("/mnt/data", exist_ok=True)
path = "/mnt/data/apis_estaduais_deputados.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(schema, f, ensure_ascii=False, indent=2)

path