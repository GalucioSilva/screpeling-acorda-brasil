import scrapy


class GovernadoresSpider(scrapy.Spider):
    name = "governadores"
    allowed_domains = ["pt.wikipedia.org"]
    start_urls = [
        "https://pt.wikipedia.org/wiki/Lista_de_governadores_das_unidades_federativas_do_Brasil"
    ]

    def parse(self, response):
        # Seleciona a tabela logo após o título "Atuais governadores"
        tabela = response.xpath('//*[@id="Atuais_governadores"]/../following-sibling::table[1]')

        for linha in tabela.xpath(".//tbody/tr"):
            # Pega as colunas da linha
            colunas = linha.xpath(".//td")

            if not colunas:  # ignora linhas de cabeçalho ou vazias
                continue

            yield {
                "estado": colunas[0].xpath(".//a[1]/text()").get(default="").strip(),
                "governador": colunas[2].xpath(".//a/text()").get(default="").strip(),
                "partido": colunas[4].xpath(".//a/text()").get(default="").strip(),
                "inicio_mandato": colunas[5].xpath("string(.)").get(default="").strip(),
                "fim_mandato": colunas[6].xpath("string(.)").get(default="").strip(),
                "eleicoes": colunas[7].xpath("string(.)").get(default="").strip(),
                "vice": colunas[8].xpath("string(.)").get(default="").strip(),
            }
