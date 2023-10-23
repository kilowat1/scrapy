import scrapy
import requests
import pymongo

class DomyScrapper(scrapy.Spider):
    name = 'domy'
    start_urls = ['https://gratka.pl/nieruchomosci/domy']

    # url = "https://api.geoapify.com/v1/geocode/search?text=38%20Upper%20Montagu%20Street%2C%20Westminster%20W1H%201LJ%2C%20United%20Kingdom&apiKey=4b9bd8602e0541b6829e69a7a849d58e"

    # api = requests.get(url)

    # print(api.status_code)

    def __init__(self, *args, **kwargs):
        super(DomyScrapper, self).__init__(*args, **kwargs)
        self.mongo_uri = 'mongodb://localhost:27017'
        self.mongo_db = 'dane'  
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db['datav2']  

    def parse(self, response):
        for houses in response.css('div.listing__teaserWrapper'):
            house_url = houses.css('a.teaserLink').attrib['href']
            yield response.follow(house_url, callback=self.house_parse)



        next_page = response.css('a.pagination__nextPage').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def house_parse(self,response):
        def innertext_quick(elements, delimiter=""):
            return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)

        location = str(innertext_quick(response.css('span.offerLocation'))).replace("['","").replace("']","")

        data = {
            'location': location,
            'latitude': requests.get(url=("https://api.geoapify.com/v1/geocode/search?text=") + location + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lat'],
            'longitude': requests.get(url=("https://api.geoapify.com/v1/geocode/search?text=") + location + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lon'],
            'title': response.css('h1.sticker__title::text').get().strip(),
            'total_price': response.css('span.priceInfo__value::text').get().strip(),
            'additional_price': response.css('span.priceInfo__additional::text').get().strip(),
            response.xpath("//ul[@class='parameters__singleParameters']/li[2]/b/preceding-sibling::span/text()").get(): response.xpath("//ul[@class='parameters__singleParameters']/li[2]/b/text()").get(),
            response.xpath("//ul[@class='parameters__singleParameters']/li[3]/b/preceding-sibling::span/text()").get(): response.xpath("//ul[@class='parameters__singleParameters']/li[3]/b/text()").get(),
            response.xpath("//ul[@class='parameters__singleParameters']/li[4]/b/preceding-sibling::span/text()").get(): response.xpath("//ul[@class='parameters__singleParameters']/li[4]/b/text()").get(),
            response.xpath("//ul[@class='parameters__singleParameters']/li[5]/b/preceding-sibling::span/text()").get(): response.xpath("//ul[@class='parameters__singleParameters']/li[5]/b/text()").get(),
            response.xpath("//ul[@class='parameters__singleParameters']/li[6]/b/preceding-sibling::span/text()").get(): response.xpath("//ul[@class='parameters__singleParameters']/li[6]/b/text()").get(),
            'description': str(innertext_quick(response.css('div.description__rolled.ql-container'))).replace("['","").replace("']","")
         }

        collection = self.db['datav2']
        collection.insert_one(data)
        # except:
        #     yield {
        #         'location': location,
        #         'latitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + location + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lat'],
        #         'longitude': requests.get(url = ("https://api.geoapify.com/v1/geocode/search?text=") + location + ("&apiKey=4b9bd8602e0541b6829e69a7a849d58e")).json()['features'][0]['properties']['lon'],
        #         'title': response.css('h1.sticker__title::text').get().strip(),
        #         'total_price': 'unkmown',
        #         'additional_price': 'unknown',
        #         'description': "unknown"
        #     }