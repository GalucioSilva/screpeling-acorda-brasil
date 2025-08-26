# 🕷️ Acorda Brasil Scraper

Coletor de dados de políticos e notícias brasileiras utilizando **[Scrapy](https://scrapy.org/)** e **[Playwright](https://playwright.dev/python/)**.  
O projeto permite baixar informações de **deputados, senadores, governadores** e também de portal de notícias, alualmente so está implementado para o**G1** é preciso fazer para os outros portais.

---

## 📦 Instalação

### 1. Usando Docker (recomendado)

```bash
# construir a imagem
docker compose build

# rodar um crawler (exemplo: deputados)
docker compose run --rm scraper crawl deputados
```

O resultado ficará na pasta `data_output/`.

---

### 2. Usando Python + Virtualenv

```bash
# criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# instalar dependências
pip install -r requirements.txt

# instalar Playwright browsers (necessário para news)
playwright install
```

Executando um crawler:

```bash
scrapy crawl deputados -O data_output/deputados.json
```

---

## 🚀 Executando os crawlers

Todos os crawlers geram um **.json** na pasta `data_output/`.

### Deputados
```bash
# Docker
docker compose run --rm scraper crawl deputados -O data_output/deputados.json

# venv
scrapy crawl deputados -O data_output/deputados.json
```

**Exemplo de saída (`deputados.json`):**
```json
{
  "dados": [
    {
      "id": 204379,
      "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/204379",
      "nome": "Acácio Favacho",
      "siglaPartido": "MDB",
      "uriPartido": "https://dadosabertos.camara.leg.br/api/v2/partidos/36899",
      "siglaUf": "AP",
      "idLegislatura": 57,
      "urlFoto": "https://www.camara.leg.br/internet/deputado/bandep/204379.jpg",
      "email": "dep.acaciofavacho@camara.leg.br"
    },
    {
      "id": 220714,
      "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/220714",
      "nome": "Adail Filho",
      "siglaPartido": "REPUBLICANOS",
      "uriPartido": "https://dadosabertos.camara.leg.br/api/v2/partidos/37908",
      "siglaUf": "AM",
      "idLegislatura": 57,
      "urlFoto": "https://www.camara.leg.br/internet/deputado/bandep/220714.jpg",
      "email": "dep.adailfilho@camara.leg.br"
    },
  ]
}
```

---

### Senadores
```bash
# Docker
docker compose run --rm scraper crawl senadores -O data_output/senadores.json

# venv
scrapy crawl senadores -O data_output/senadores.json
```

**Exemplo de saída (`senadores.json`):**
```json
[
  {
    "id": "5672",
    "nome": "Alan Rick",
    "nomeCompleto": "Alan Rick Miranda",
    "sexo": "Masculino",
    "uf": null,
    "partido": "UNIÃO",
    "email": "sen.alanrick@senado.leg.br"
  },
  {
    "id": "5982",
    "nome": "Alessandro Vieira",
    "nomeCompleto": "Alessandro Vieira",
    "sexo": "Masculino",
    "uf": null,
    "partido": "MDB",
    "email": "sen.alessandrovieira@senado.leg.br"
  },
]
```

---

### Governadores
```bash
# Docker
docker compose run --rm scraper crawl governadores -O data_output/governadores.json

# venv
scrapy crawl governadores -O data_output/governadores.json
```

**Exemplo de saída (`governadores.json`):**
```json
[
  {"titulo": "Haddad diz que bolsonarismo tem feito ataques ao BB: 'Estão tentando minar as instituições'", "link": "https://g1.globo.com/economia/noticia/2025/08/23/haddad-diz-que-bolsonarismo-tem-feito-ataques-ao-bb-estao-tentando-minar-as-instituicoes.ghtml", "resumo": "Para ministro, conteúdos falsos postados sobre o Banco do Brasil fazem parte de ação combinada, que inclui projetos no Congresso. Haddad deu entrevista ao 'Jornal GGN'."},
  {"titulo": "Alckmin defende diálogo e negociação e fala em 'abrir mais mercado' para frear tarifaço de Trump", "link": "https://g1.globo.com/sp/sao-paulo/noticia/2025/08/23/alckmin-defende-dialogo-e-negociacao-e-fala-em-abrir-mais-mercado-para-frear-tarifaco.ghtml", "resumo": "Vice-presidente, que é ministro da Indústria e Comércio, vai ao México para ampliar relação bilateral. Fala é no contexto de medidas positivas da semana, como socorro do BNDES e alívio para produtos derivados de aço e alumínio."},
]
```

---

### Notícias (G1 Política)

> Esse crawler usa **Scrapy + Playwright**, então precisa do Playwright instalado (já incluído no Docker).

```bash
# Docker
docker compose run --rm scraper crawl news -O data_output/noticias.json

# venv
scrapy crawl news -O data_output/noticias.json
```

**Exemplo de saída (`noticias.json`):**
```json
[
  {
    "titulo": "Haddad diz que bolsonarismo tem feito ataques ao BB: 'Estão tentando minar as instituições'",
    "link": "https://g1.globo.com/economia/noticia/2025/08/23/haddad-diz-que-bolsonarismo-tem-feito-ataques-ao-bb-estao-tentando-minar-as-instituicoes.ghtml",
    "resumo": "Para ministro, conteúdos falsos postados sobre o Banco do Brasil fazem parte de ação combinada, que inclui projetos no Congresso. Haddad deu entrevista ao 'Jornal GGN'."
  },
  {
    "titulo": "Banco do Brasil pede à AGU ação contra postagens falsas de bolsonaristas",
    "link": "https://g1.globo.com/politica/video/banco-do-brasil-pede-a-agu-acao-contra-postagens-falsas-de-bolsonaristas-13866506.ghtml",
    "resumo": null
  }
]
```

---

## 📂 Estrutura do projeto

```
acorda_brasil_scraper/
├── acorda_brasil_scraper/
│   ├── spiders/
│   │   ├── deputados.py
│   │   ├── senadores.py
│   │   ├── governadores.py
│   │   └── news.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   └── settings.py
├── data_output/
│   └── *.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📝 Notas

- Use **Docker** se quiser simplicidade e isolamento.  
- Use **venv** se quiser rodar direto no sistema com Python instalado.  
- Para rodar Playwright no Linux em servidores sem GUI, use `playwright install --with-deps`.

---

## 📜 Licença

Livre para uso educacional e projetos pessoais.
