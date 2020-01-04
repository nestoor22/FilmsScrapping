import scrapy
import mtranslate

translate_for_keys = {'Год': 'release_date', 'Страна': 'country', 'Жанр': 'genre'}


# for running - scrapy crawl ex_fs_net_spider
class ExFsNetSpider(scrapy.Spider):
    # Spider name
    name = 'ex_fs_net_spider'

    def start_requests(self):
        start_urls = ['http://ex-fs.net/series/', 'http://ex-fs.net/films/', 'http://ex-fs.net/cartoon/']

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for page_link in response.css('div[class="MiniPost"]'):
            # Get link from each mini-poster to film page
            page_link = page_link.css('a[class="MiniPostPoster"]::attr(href)').get()
            start_url = response.request.url
            if 'series' in start_url:
                tv_show_type = 'serie'
            elif 'cartoon' in start_url:
                tv_show_type = 'cartoon'
            else:
                tv_show_type = 'film'
            yield scrapy.Request(url=page_link, callback=self.parse_info,  meta={'tv_show_type': tv_show_type})

        # Get next page if exist and make recursion call
        if response.css('div[class="navigations"]'):
            next_page_link = response.css('div[class="navigations"] a::attr(href)').getall()[-1]

            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_info(self, response):
        # Create a dict for storing information
        information_about_film = dict()
        information_about_film['poster_url'] = 'http://ex-fs.net/' + response.css('div[class="FullstoryFormLeft"]'
                                                                                  ' img::attr(src)').get()
        information_about_film['tv_show_type'] = response.meta.get('tv_show_type')

        # Save film name in english and russian.
        information_about_film['name_rus'] = clean_strings_from_bad_characters(response.css('h1[class="view-'
                                                                                            'caption"]::text').get())
        information_about_film['name_eng'] = clean_strings_from_bad_characters(response.css('h2[class="view-'
                                                                                            'caption2"]::text').get())

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
                if 'country' in information_about_film:
                    information_about_film['country_rus'] = information_about_film['country']
                    information_about_film['country_eng'] = []
                    for country in information_about_film['country_rus']:
                        information_about_film['country_eng'].append(mtranslate.translate(country, 'en'))
            information_index += 1

        information_about_film['release_date'] = int(information_about_film['release_date'][0])
        information_about_film['plot_rus'] = clean_strings_from_bad_characters(response.css('div[class="Fullstory'
                                                                                            'SubFormText"]::text').get())

        information_about_film['plot_eng'] = mtranslate.translate(information_about_film['plot_rus'], 'en')

        information_about_film['actors_rus'] = response.css('div[class="FullstoryKadrFormImgAc"] '
                                                            'a[class="MiniPostNameActors"]::text').getall()
        information_about_film['actors_eng'] = []
        for actor in information_about_film['actors']:
            information_about_film['actors_eng'].append(mtranslate.translate(actor, 'en'))

        yield information_about_film


def clean_strings_from_bad_characters(string):
    import regex as re
    if string:
        string = string.strip()
        return re.sub(r"[^\w\d\. ]", '', str(string))


def get_image_from_url_as_base64(image_url):
    import base64
    import requests

    return base64.b64encode(requests.get('http://ex-fs.net/' + image_url).content)

