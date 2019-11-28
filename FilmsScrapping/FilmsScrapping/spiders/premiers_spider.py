import scrapy


class PremiersSpider(scrapy.Spider):
    name = 'premiers_spider'

    def start_requests(self):
        start_urls = []

    def parse(self, response):
        pass
    pass
