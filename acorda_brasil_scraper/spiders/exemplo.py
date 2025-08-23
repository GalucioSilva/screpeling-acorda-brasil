import scrapy


class ExemploSpider(scrapy.Spider):
    name = "exemplo"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        pass
