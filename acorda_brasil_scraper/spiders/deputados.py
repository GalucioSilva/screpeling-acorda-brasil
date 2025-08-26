import scrapy
import json


class DeputadosSpider(scrapy.Spider):
    name = "deputados"
    allowed_domains = ["dadosabertos.camara.leg.br"]
    start_urls = [
        "https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome&formato=json"
    ]

    def parse(self, response):
        data = json.loads(response.text)

        for dep in data.get("dados", []):
            yield {
                "api_id": dep.get("id"),
                "api_uri": dep.get("uri"),
                "nome": dep.get("nome"),
                "siglaPartido": dep.get("siglaPartido"),
                "siglaUf": dep.get("siglaUf"),
                "urlFoto": dep.get("urlFoto"),
                "email": dep.get("email"),
                "cargo": "DeputadoFederal",
            }

        # Paginação
        for link in data.get("links", []):
            if link.get("rel") == "next":
                yield scrapy.Request(link["href"] + "&formato=json", callback=self.parse)
