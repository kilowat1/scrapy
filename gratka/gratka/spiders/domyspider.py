import scrapy
import requests

class DomyScrapper(scrapy.Spider):
    name = 'domy'
    start_urls = ['https://gratka.pl/nieruchomosci/domy']

    # url = "https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20Westminster%20W1H%201LJ%2C%20United%20Kingdom&apiKey=4b9bd8602e0541b6829e69a7a849d58e"

    # api = requests.get(url)

    # print(api.status_code)

    def parse(self, response):
        for houses in response.css('div.listing__teaserWrapper'):
            try:
                yield {
                    'location': houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip(),
                    'latitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip() + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lat'],
                    'longitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip() + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lon'],
                    'title': houses.css('h2.teaserUnified__title::text').get().strip(),
                    'description': houses.css('p.teaserUnified__description::text').get().strip(),
                    'total_price': houses.css('p.teaserUnified__price::text').get().strip(),
                    'additional_price': houses.css('span.teaserUnified__additionalPrice::text').get().replace('zł/m','').strip(),
                    'surface_area': houses.css('li.teaserUnified__listItem::text').get().replace('m','').strip()
                }
            except:
                yield {
                    'location': houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip(),
                    'latitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip() + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lat'],
                    'longitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + houses.css('span.teaserUnified__location::text').get().replace('                                ','').strip() + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lon'],
                    'title': houses.css('h2.teaserUnified__title::text').get().strip(),
                    'description': 'none',
                    'total_price': 'unknown',
                    'additional_price': 'none',
                    'surface_area': houses.css('li.teaserUnified__listItem::text').get().replace('m','').strip()
                }
            # next_page = response.css('a.pagination__nextPage').attrib['href']
            # if next_page is not None:
            #     yield response.follow(next_page, callback=self.parse)