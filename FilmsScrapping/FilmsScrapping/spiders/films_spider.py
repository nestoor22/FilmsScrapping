import scrapy
import mtranslate


# for running - scrapy crawl ex_fs_net_spider
class ExFsNetSpider(scrapy.Spider):
    # Spider name
    name = 'movie_db_spider'

    def start_requests(self):
        start_urls = ['https://www.themoviedb.org/movie/', 'https://www.themoviedb.org/tv/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for page_link in response.css('div[class="item poster card"]'):
            # Get link from each mini-poster to film page
            page_link = page_link.css('a[class="result"]::attr(href)').get()
            page_link = 'https://www.themoviedb.org' + page_link
            start_url = response.request.url
            if 'tv' in start_url:
                tv_show_type = 'serie'
            else:
                tv_show_type = 'film'
            yield scrapy.Request(url=page_link, callback=self.parse_info,  meta={'tv_show_type': tv_show_type})

        # Get next page if exist and make recursion call
        if response.css('div[class="pagination"]'):
            next_page_link = response.css('div[class="pagination"] a::attr(href)').getall()[-1]
            print("NEXT PAGE:", next_page_link)
            yield scrapy.Request(url='https://www.themoviedb.org'+ next_page_link, callback=self.parse)

    def parse_info(self, response):
        # Create a dict for storing information
        information_about_film = dict()
        information_about_film['poster_url'] = response.css('div[class="image_content"] a::attr(href)').get()
        information_about_film['showtype'] = response.meta.get('tv_show_type')
        information_about_film['title'] = response.css('div[class="title"] h2::text').get()
        information_about_film['release_date'] = response.css('div[class="title"] '
                                                              'span[class="release_date"]::text').get().replace('(', '').replace(')', '')
        information_about_film['plot'] = response.css('div[class="overview"] p::text').get()
        information_about_film['genres'] = response.css('section[class="genres right_column"] a::text').getall()

        yield scrapy.Request(url=response.request.url+'/cast/', callback=self.parse_cast,
                             meta={'information_about_film': information_about_film})

    def parse_cast(self, response):
        information_about_film = response.meta.get('information_about_film')
        information_about_film['cast'] = []
        cast = response.css('div[class="info"] a::attr(href)').getall()
        for link in cast:
            if 'person' in link:
                actor_name = link.split('/')[-1]
                if '-' in actor_name:
                    actor_name = actor_name[actor_name.index('-'):].replace('-', ' ')
                    information_about_film['cast'].append(actor_name.strip())
        yield information_about_film

    def get_actor_name(self, response):
        yield response.css('div[class="title"] h2::text').get()
