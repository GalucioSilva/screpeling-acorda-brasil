import scrapy


partidos ={
    "Progressistas": "PP",
    "Movimento Democrático Brasileiro": "MDB",
    "Solidariedade": "SOLIDARIEDADE",
    "União Brasil": "UNIÃO",
    "Partido dos Trabalhadores": "PT",
    "Partido Social Democrático": "PSD",
    "Partido da Social Democracia Brasileira": "PSDB",
    "Partido Novo": "NOVO",
    "Partido Liberal": "PL",
    "Republicanos": "REPUBLICANOS",
    "Partido Socialista Brasileiro": "PSB",
}

estados = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}

class GovernadoresSpider(scrapy.Spider):
    name = "governadores"
    allowed_domains = ["pt.wikipedia.org"]
    start_urls = [
        "https://pt.wikipedia.org/wiki/Lista_de_governadores_das_unidades_federativas_do_Brasil"
    ]

    def parse(self, response):
        # Pega a segunda tabela de governadores em exercício
        linhas = response.xpath('//table[contains(@class,"wikitable")][2]/tbody/tr')

        id_counter = 200000000
        for linha in linhas[1:]:  # pula o cabeçalho
            estado = linha.xpath("./td[1]//a/text()").get(default="").strip()

            nome = linha.xpath("./td[3]//a/text()").get(default="").strip()

            partido = linha.xpath("./td[5]//a/text()").get(default="").strip()

            foto = linha.xpath("./td[2]//img/@src").get()
            if foto:
                foto = response.urljoin(foto)
                # pega o link do nome
            url_biografia = linha.xpath("./td[3]//a/@href").get()
            if url_biografia:
                url_biografia = response.urljoin(url_biografia)

            yield {
                "api_id": id_counter,
                "api_uri": url_biografia if url_biografia else "",
                "nome": nome,
                "siglaPartido": partidos[partido],
                "sigleUf": estados[estado],
                "urlFoto": foto if foto else "",
                "email": "",
            }

            id_counter += 1
