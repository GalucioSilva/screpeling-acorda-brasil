# README — Uso de APIs para aquisição de Dados Abertos dos Senadores e Deputados


## Referências

- [Swagger — Dados Abertos da Câmara](https://dadosabertos.camara.leg.br/swagger/api.html)  
- [Portal de Dados Abertos do Senado](https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html)  
- [Exemplo de endpoint Senado](https://legis.senado.leg.br/dadosabertos/senador/lista/atual)  
---
## Como Usar os Exemplos Práticos

Este repositório contém exemplos prontos em **Shell Script** (`.sh`) e **Python** (`.py`) para baixar e salvar os dados localmente.

### 1. Criar e ativar ambiente virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# ou
.\.venv\Scriptsctivate    # Windows PowerShell
```

### 2. Instalar dependências

As bibliotecas necessárias estão listadas em `requirements.txt`.  
Gere o arquivo ou instale direto:

```bash
pip install requests
```

Se quiser exportar todas as libs da venv:

```bash
pip freeze > requirements.txt
```

E em outro ambiente basta:

```bash
pip install -r requirements.txt
```

### 3. Rodar os scripts de exemplo

- **Shell Script**  
  ```bash
  chmod +x exemplos/senador.sh exemplos/deputado.sh
  ./exemplos/senador.sh
  ./exemplos/deputado.sh
  ```

- **Python**  
  ```bash
  python exemplos/parlamentares.py
  ```

Os arquivos baixados serão salvos na pasta `data/`:
- `data/senadores.json`
- `data/deputados.json`

---
##  Índice

1. [Visão Geral](#visão-geral)  
2. [Requisitos](#requisitos)  
3. [Como Fazer Requisições](#como-fazer-requisições)  
   - 3.1 Deputados  
   - 3.2 Senadores *(via Senado Federal — Catálogo de Dados Abertos do Senado)*  
   - 3.3 Governadores *(disponibilidade limitada; podem ser obtidos em outros portais estaduais ou federais)*  
4. [Exemplos de Código](#exemplos-de-código)  
5. [Formatos de Resposta](#formatos-de-resposta)  

---

## Visão Geral

Este README explica como utilizar as APIs RESTful do portal de Dados Abertos do Governo Brasileiro para consultar informações sobre **deputados** e **senadores**.  
Ele também indica onde encontrar dados sobre **governadores**.  

Fontes principais:  
- **Câmara dos Deputados**: API REST com documentação Swagger.  
- **Senado Federal**: Portal de Dados Abertos com endpoints HTTP, CSV e XML.  

---

## Requisitos

- Qualquer linguagem ou ferramenta capaz de fazer requisições HTTP (`curl`, Postman, Python `requests`, etc.)  
- Formatos suportados: JSON, XML e CSV (dependendo do portal)  
- Opcional: ferramentas como `jq` para processar JSON ou `pandas` em Python  

---

## Como Fazer Requisições

### 3.1 Deputados (Câmara dos Deputados)

Para listar todos os deputados em exercício:
```
GET https://dadosabertos.camara.leg.br/api/v2/deputados
```

Exemplo filtrando por **nome**:
```
GET https://dadosabertos.camara.leg.br/api/v2/deputados?nome=Fulano
```

Exemplo filtrando por **estado**:
```
GET https://dadosabertos.camara.leg.br/api/v2/deputados?siglaUf=SP
```

---

### 3.2 Senadores (Senado Federal)

Os dados dos senadores podem ser acessados via **Dados Abertos do Senado**.  
A principal diferença é que o Senado não fornece a mesma interface Swagger da Câmara, mas disponibiliza endpoints diretos e arquivos em XML/CSV.  

#### Listagem de senadores em exercício
```
GET https://legis.senado.leg.br/dadosabertos/senador/lista/atual
```

#### Listagem de todos os senadores por legislatura
```
GET https://legis.senado.leg.br/dadosabertos/senador/lista/legislatura
```

#### Detalhes de um senador específico (exemplo: idSenador = 4981)
```
GET https://legis.senado.leg.br/dadosabertos/senador/4981
```

---

### 3.3 Governadores

Não há API centralizada no governo federal para governadores.  
Fontes alternativas:  
- **Portais estaduais de transparência**  
- **dados.gov.br** (buscando datasets por estado)  
- APIs regionais específicas em alguns estados  

---

## Exemplos de Código

### Deputados (Câmara)

```bash
# Deputados em exercício
curl -H "Accept: application/json" \
  "https://dadosabertos.camara.leg.br/api/v2/deputados"
```

### Senadores (Senado)

```bash
# Senadores em exercício (XML por padrão)
curl "https://legis.senado.leg.br/dadosabertos/senador/lista/atual"

# Converter resposta XML em JSON (Linux com xq)
curl "https://legis.senado.leg.br/dadosabertos/senador/lista/atual" | xq .
```

Em **Python**:

```python
import requests
import xml.etree.ElementTree as ET

# Lista de senadores em exercício
url = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual"
resp = requests.get(url)
root = ET.fromstring(resp.content)

# Exibir os 5 primeiros nomes
for senador in root.findall(".//Parlamentar")[:5]:
    print(senador.find("IdentificacaoParlamentar/NomeParlamentar").text)
```

---

## Formatos de Resposta

- **Câmara**: JSON e XML  
- **Senado**: XML (nativo) e CSV em alguns datasets  
- **Governadores**: variam conforme estado (JSON, CSV ou planilhas)  
---
