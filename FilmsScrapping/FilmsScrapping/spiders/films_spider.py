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
        info['imdb_rating'] = float(response.css('div[class="in_kp_imdb"] div[class="in_name_imdb"]::text').get())
        story_info_keys = response.css('div[class="FullstoryInfo"] h4[class="FullstoryInfoTitle"]::text').getall()
        story_info_values = response.css('div[class="FullstoryInfo"] p[class="FullstoryInfoin"]')
        i = 0
        info['info'] = {}
        for one_select in story_info_values:
            one_property = one_select.css('a::text').getall()
            if one_select.css('a::text').getall():
                info['info'][story_info_keys[i]] = one_property
            i += 1
        yield info
