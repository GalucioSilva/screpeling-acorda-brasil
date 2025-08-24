import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        yield scrapy.Request(
            url="https://g1.globo.com/politica/",
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.wait_for_selector("div.feed-post-body")

        content = await page.content()
        sel = scrapy.Selector(text=content)

        for post in sel.css("div.feed-post-body"):
            # pega todos os <p elementtiming="text-csr">
            ps = post.css("p[elementtiming=text-csr]::text").getall()

            titulo = (
                post.css("a.feed-post-link::text").get()
                or post.css("a.feed-post-link span::text").get()
                or post.css("a.feed-post-link p::text").get()
                or (ps[0] if ps else None)  # primeiro <p> pode ser título
            )

            resumo = None
            if len(ps) > 1:
                resumo = ps[1]  # segundo <p> é o resumo
            elif not resumo:
                resumo = post.css("div.feed-post-body-resumo::text").get()

            link = (
                post.css("a.feed-post-link::attr(href)").get()
                or post.css("a::attr(href)").get()
            )

            yield {
                "titulo": titulo.strip() if titulo else None,
                "link": link,
                "resumo": resumo.strip() if resumo else None,
            }

        await page.close()
