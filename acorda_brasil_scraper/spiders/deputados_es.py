import re
import zlib
import hashlib
import scrapy
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


LIST_URL = "https://www.al.es.gov.br/Deputado/Lista"
UF = "ES"
CARGO = "Deputado Estadual"
STATE_PREFIX = 320_000_000  # prefixo numérico estável p/ ES (IBGE 32 → 320M)

def stable_id(nome: str, perfil_url: str = "") -> int:
    """
    Gera um inteiro estável no range [320_000_000, 329_999_999]
    com base no nome + URL do perfil. Assim você tem um api_id
    consistente entre execuções mesmo que o site não forneça ID numérico.
    """
    base = f"{UF}:{nome}:{perfil_url}".lower().encode("utf-8")
    n = zlib.adler32(base) % 9_999_999
    return STATE_PREFIX + n

def clean_text(s: str | None) -> str:
    return re.sub(r"\s+", " ", s or "").strip()

def absolute_url(base: str, src: str | None) -> str:
    if not src:
        return ""
    return urljoin(base, src)


class DeputadosESSpider(scrapy.Spider):
    name = "deputados_es"
    custom_settings = {
        # reduza o risco de bloqueio
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_DELAY": 0.5,
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            LIST_URL,
            meta={
                "playwright": True,
                # Espera a página terminar de carregar chamadas XHR
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    # tenta esperar por algo “tabeloso”/lista
                    PageMethod("wait_for_selector", "css=table, css=ul, css=.card, css=[class*='deputad']"),
                ],
            },
        )

    def parse(self, response):
        """
        A lista na ALES costuma vir como cards ou uma tabela.
        Abaixo trato múltiplos layouts possíveis para ser resiliente.
        Para cada item, tento extrair: nome, partido, foto e link do perfil.
        Depois sigo para o perfil para captar e-mail e confirmar dados.
        """
        # 1) TENTATIVA: tabela (tbody > tr)
        rows = response.css("table tbody tr")
        if rows:
            for tr in rows:
                yield from self._from_container(response, tr)

        # 2) TENTATIVA: lista não ordenada de cards
        cards = response.css("ul li, .cards .card, .card-deputado, .parlamentares__lista li")
        for li in cards:
            # só processe se houver link que leve a /Deputado/ALGUMA_COISA
            if li.css("a[href*='/Deputado/']"):
                yield from self._from_container(response, li)

        # 3) fallback: qualquer coisa que contenha link /Deputado/
        links = response.css("a[href*='/Deputado/']")
        for a in links:
            container = a.root  # usa o próprio <a> como “container”
            yield from self._from_container(response, a)

    def _from_container(self, response, sel):
        nome = clean_text(
            sel.css("a[href*='/Deputado/']::text").get()
            or sel.css("h3::text, h2::text, .nome::text, .title::text, td:nth-child(1)::text").get()
        )
        if not nome:
            return

        perfil_url = response.urljoin(
            sel.css("a[href*='/Deputado/']::attr(href)").get(default="")
        )

        sigla = clean_text(
            sel.css(".partido::text, .sigla::text, td:nth-child(2)::text").get()
        )

        foto = absolute_url(response.url, sel.css("img::attr(src)").get())

        item_base = {
            "api_id": None,            # preenchido no parse_profile
            "api_uri": perfil_url or "",   # se não achar Wikipedia, usamos o perfil oficial
            "nome": nome,
            "siglaPartido": sigla,
            "sigleUf": UF,             # mantendo a chave como você pediu
            "urlFoto": foto,
            "email": "",
            "cargo": CARGO,
        }

        if perfil_url:
            yield scrapy.Request(
                perfil_url,
                callback=self.parse_profile,
                cb_kwargs={"partial": item_base},
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_selector", "css=body"),
                    ],
                },
            )
        else:
            # sem perfil: ainda assim gere o api_id estável
            item_base["api_id"] = stable_id(nome, "")
            yield item_base

    def parse_profile(self, response, partial):
        """
        Extrai e-mail (mailto ou texto), confirma partido/foto caso não tenha vindo na lista.
        Mantém o formato desejado.
        """
        html = response.text

        # e-mail: tenta link mailto; senão regex
        email = clean_text(response.css("a[href^='mailto:']::attr(href)").get(""))
        if email.lower().startswith("mailto:"):
            email = email.split(":", 1)[1]

        if not email:
            m = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", html)
            email = m.group(0) if m else ""

        # partido (reconfirma se vazio)
        if not partial.get("siglaPartido"):
            sigla = clean_text(
                response.css(".partido::text, .sigla::text, .info li::text, .dados li::text").re_first(r"[A-Z]{2,6}")
            )
        else:
            sigla = partial["siglaPartido"]

        # foto (reconfirma se veio vazia/thumbnail)
        foto = partial.get("urlFoto") or ""
        if not foto or "data:image" in foto:
            foto = absolute_url(response.url, response.css("img[src*='Deputad'], img[src*='foto'], img::attr(src)").get())

        # monta final
        item = dict(partial)
        item["email"] = email
        item["siglaPartido"] = sigla or partial.get("siglaPartido", "")
        item["urlFoto"] = foto or partial.get("urlFoto", "")
        item["api_uri"] = partial.get("api_uri") or response.url
        item["api_id"] = stable_id(item["nome"], item["api_uri"])

        yield item
