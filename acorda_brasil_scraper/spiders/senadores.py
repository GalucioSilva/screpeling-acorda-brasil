import scrapy
import xmltodict


class SenadoresSpider(scrapy.Spider):
    name = "senadores"
    allowed_domains = ["legis.senado.leg.br"]
    start_urls = [
        "https://legis.senado.leg.br/dadosabertos/senador/lista/atual"
    ]

    def parse(self, response):
        # Converte XML -> dict
        data = xmltodict.parse(response.text)

        # Caminho até a lista
        senadores = data["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]

        for s in senadores:
            ident = s["IdentificacaoParlamentar"]

            # Telefone pode ser lista ou dict
            telefones = ident.get("Telefones", {}).get("Telefone", [])
            if isinstance(telefones, dict):
                telefone = telefones.get("NumeroTelefone")
            elif isinstance(telefones, list) and len(telefones) > 0:
                telefone = telefones[0].get("NumeroTelefone")
            else:
                telefone = None

            yield {
                "api_id": int(ident["CodigoParlamentar"]),
                "api_uri": ident.get("UrlPaginaParlamentar"),  # ✅ corrigido
                "nome": ident.get("NomeParlamentar"),
                "siglaPartido": ident.get("SiglaPartidoParlamentar"),
                "siglaUf": ident.get("UfParlamentar"),
                "urlFoto": ident.get("UrlFotoParlamentar"),
                "email": ident.get("EmailParlamentar"),
                "telefone": telefone,
            }
