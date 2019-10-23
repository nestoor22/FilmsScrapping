import scrapy


class ExFsNetFilmsSpider(scrapy.Spider):
    name = 'ex_fs_net_films_spider'

    def start_requests(self):
        start_urls = ['http://ex-fs.net/films/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for link in response.css('div[class="MiniPost"]'):
            link = link.css('a[class="MiniPostPoster"]::attr(href)').get()
            yield scrapy.Request(url=link, callback=self.parse_info)
        if response.css('div[class="navigations"]'):
            next_link = response.css('div[class="navigations"] a::attr(href)').getall()[-1]
            yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_info(self, response):
        info = dict()
        info['name_rus'] = response.css('h1[class="view-caption"]::text').get()
        info['name_eng'] = response.css('h2[class="view-caption2"]::text').get()
        yield info
