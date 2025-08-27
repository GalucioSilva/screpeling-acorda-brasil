# spiders/deputados_sapl.py
import scrapy

# ===== Listas por estado (se quiser usar em memória) =====
dep_al = []
dep_ac = []
dep_am = []
dep_mt = []
dep_pi = []
dep_ro = []

class DeputadosSaplSpider(scrapy.Spider):
    name = "deputados_sapl"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_TIMEOUT": 30,
        "LOG_LEVEL": "INFO",
        "HTTPERROR_ALLOWED_CODES": [301, 302, 400, 401, 403, 404, 500, 502, 503],
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, */*;q=0.1",
            "User-Agent": "acorda_brasil_scraper/1.0",
        },
        # Se quiser garantir sobrescrita do feed a cada execução:
        # "FEED_STORE_OVERWRITE": True,
    }

    # UFs alvo
    rows = ["al", "ac", "am", "mt", "pi", "ro"]

    # Dois formatos comuns no SAPL (o 1º já funcionou nos seus logs)
    PATHS = [
        "/api/parlamentares/parlamentar/?page_size=100&ativo=True",
        "/api/parlamentar/?page_size=100&ativo=True",
    ]

    def start_requests(self):
        for uf in self.rows:
            base = f"https://sapl.al.{uf}.leg.br"
            for path in self.PATHS:
                url = f"{base}{path}"
                self.logger.info(f"[BOOT] {uf.upper()} → {url}")
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    errback=self.errback_log,
                    cb_kwargs={"uf": uf},
                    dont_filter=True,
                    meta={"handle_httpstatus_all": True},
                )

    def parse(self, response, uf):
        ct = response.headers.get("Content-Type", b"").decode().lower()
        self.logger.info(f"[{uf.upper()}] HTTP {response.status} CT={ct} URL={response.url}")

        if response.status != 200 or "application/json" not in ct:
            self.logger.warning(f"[{uf.upper()}] Sem JSON 200. Trecho: {response.text[:200]!r}")
            return

        try:
            data = response.json()
        except Exception as e:
            self.logger.error(f"[{uf.upper()}] Falha ao decodificar JSON: {e}")
            return

        results = data.get("results", [])
        self.logger.info(f"[{uf.upper()}] {len(results)} registros nesta página")

        for dep in results:
            item = {
                "api_id": dep.get("id"),
                "api_uri": "https://sapl.al.{uf}.leg.br/api/parlamentares/parlamentar/{id}/".format(id=dep.get("id"), uf=uf),
                "nome": dep.get("nome_parlamentar") or dep.get("__str__"),
                "siglaPatido": dep.get("partido"),
                "siglaUf": uf.upper(),
                "urlFoto": dep.get("fotografia") or dep.get("foto_url"),
                "email": dep.get("email"),
                "telefone": dep.get("telefone"),
                "cargo": "Deputado Estadual"
            }
            # mantém suas listas em memória
            self._append_to_state_list(uf, item)
            # >>> ESSENCIAL: exportar e passar no pipeline/FeedExporter
            yield item

        next_url = (data.get("pagination", {}).get("links", {}) or {}).get("next")
        if next_url:
            self.logger.info(f"[{uf.upper()}] Próxima página: {next_url}")
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                errback=self.errback_log,
                cb_kwargs={"uf": uf},
                meta={"handle_httpstatus_all": True},
            )

    def _append_to_state_list(self, uf, item):
        uf = uf.lower()
        if uf == "al":
            dep_al.append(item)
        elif uf == "ac":
            dep_ac.append(item)
        elif uf == "am":
            dep_am.append(item)
        elif uf == "mt":
            dep_mt.append(item)
        elif uf == "pi":
            dep_pi.append(item)
        elif uf == "ro":
            dep_ro.append(item)

    def errback_log(self, failure):
        req = failure.request
        uf = req.cb_kwargs.get("uf", "?")
        self.logger.error(f"[{uf.upper()}] ERRO de rede/conn: {getattr(req, 'url', '')} -> {failure!r}")

    def closed(self, reason):
        self.logger.info(
            "Coleta finalizada: "
            f"AL={len(dep_al)}, AC={len(dep_ac)}, AM={len(dep_am)}, "
            f"MT={len(dep_mt)}, PI={len(dep_pi)}, RO={len(dep_ro)}"
        )
