import scrapy


translate_for_keys = {'Год': 'release_date', 'Страна': 'country', 'Жанр': 'genre'}


# for running - scrapy crawl ex_fs_net_films_spider
class ExFsNetFilmsSpider(scrapy.Spider):
    # Spider name
    name = 'ex_fs_net_films_spider'

    def start_requests(self):
        start_urls = ['http://ex-fs.net/films/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for film_page_link in response.css('div[class="MiniPost"]'):
            # Get link from each mini-poster to film page
            film_page_link = film_page_link.css('a[class="MiniPostPoster"]::attr(href)').get()
            yield scrapy.Request(url=film_page_link, callback=self.parse_info)

        # Get next page if exist and make recursion call
        if response.css('div[class="navigations"]'):
            next_page_link = response.css('div[class="navigations"] a::attr(href)').getall()[-1]
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_info(self, response):
        # Create a dict for storing information
        information_about_film = dict()

        information_about_film['poster_url'] = 'http://ex-fs.net/' + response.css('div[class="FullstoryFormLeft"]'
                                                                                        ' img::attr(src)').get()

        # Save film name in english and russian.
        information_about_film['name_rus'] = clean_strings_from_bad_characters(response.css('h1[class="view-caption"]::text').get())
        information_about_film['name_eng'] = clean_strings_from_bad_characters(response.css('h2[class="view-caption2"]::text').get())

        # Add IMDB rating
        information_about_film['imdb_rating'] = float(response.css('div[class="in_kp_imdb"] '
                                                                   'div[class="in_name_imdb"]::text').get())

        story_info_keys = response.css('div[class="FullstoryInfo"] h4[class="FullstoryInfoTitle"]::text').getall()
        story_info_keys = [translate_for_keys[key.replace(':', '')] for key in story_info_keys
                           if key.replace(':', '') in translate_for_keys]

        story_info_values = response.css('div[class="FullstoryInfo"] p[class="FullstoryInfoin"]')

        # Story information about years of release date, country and genre
        information_index = 0
        for one_select in story_info_values:
            one_property = one_select.css('a::text').getall()
            if one_property:
                information_about_film[story_info_keys[information_index]] = one_property
            information_index += 1

        information_about_film['release_date'] = int(information_about_film['release_date'][0])
        information_about_film['plot'] = clean_strings_from_bad_characters(response.css('div[class="FullstorySubFormText"]::text').get())

        information_about_film['actors'] = response.css('div[class="FullstoryKadrFormImgAc"] '
                                                        'a[class="MiniPostNameActors"]::text').getall()

        yield information_about_film


def clean_strings_from_bad_characters(string):
    import re
    if string:
        return re.sub(r'[^A-Za-zА-Яа-я\\.,\d?! ]', ' ', str(string))


def get_image_from_url_as_base64(image_url):
    import base64
    import requests

    return base64.b64encode(requests.get('http://ex-fs.net/' + image_url).content)

