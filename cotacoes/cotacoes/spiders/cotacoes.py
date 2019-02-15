import scrapy
import json

class Cotacoes(scrapy.Spider):
    name = "cotacoes"
    urls = [ 'https://api.cotacoes.uol.com/currency/interday/list/paged/?format=JSON&fields=bidvalue,askvalue,maxbid,minbid,variationbid,variationpercentbid,openbidvalue,date&size=6&currency=1&' ]

    def start_requests(self):

        for url in self.urls:

            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):

        # page = response.css('table.tabela-historic tbody tr.ng-scope::text').get()

        jsonWithoutParse = response.body

        jsonParse = json.loads(jsonWithoutParse)

        tokenNext = jsonParse['next']

        self.log(jsonParse)

        if tokenNext != None:

            urlNextPage = self.urls[0] + 'token=' + tokenNext

            scrapy.Request(urlNextPage, callback=self.parse)

