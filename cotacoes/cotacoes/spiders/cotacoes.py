import scrapy
import json
import datetime

from cotacoes.items import dolarItem

class Cotacoes(scrapy.Spider):
    name = "cotacoes"
    complemento = '/currency/interday/list/paged/?format=JSON&fields=bidvalue,askvalue,maxbid,minbid,variationbid,variationpercentbid,openbidvalue,date&currency=1&size=6&'
    urls = [ 'https://api.cotacoes.uol.com' ]

    header = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://economia.uol.com.br',
        'Referer': 'https://economia.uol.com.br/cotacoes/cambio/dolar-comercial-estados-unidos/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116'
    }

    def start_requests(self):

        for url in self.urls:

            yield scrapy.Request(url + self.complemento, callback=self.parse, headers=self.header, dont_filter=True)

    def parse(self, response):

        documentoNotReady = response.body

        if documentoNotReady is not None:

            documentReady = json.loads(documentoNotReady)

            tokenNext = documentReady['next']

            for data in documentReady['docs']:

                item = dolarItem()

                item['compra'] = data['bidvalue']
                item['venda'] = data['askvalue']

                date = data['date']
                ano = date[0:4]
                mes = date[4:6]
                dia = date[6:8]
                
                date = dia + '/' + mes + '/' + ano

                dateMongo = datetime.datetime.strptime(date, '%d/%m/%Y')
                self.log(dateMongo)

                item['data'] = dateMongo 

                yield item

            if tokenNext is not None:

                header2 = {
                    ':authority': 'api.cotacoes.uol.com',
                    ':method': 'GET',
                    ':path': self.complemento + 'next=' + tokenNext + '&',
                    ':scheme': 'https',
                    'Accept': 'application/json, text/plain, */*',
                    'Origin': 'https://economia.uol.com.br',
                    'Referer': 'https://economia.uol.com.br/cotacoes/cambio/dolar-comercial-estados-unidos/',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.116'
                }

                urlNextPage = response.urljoin(self.complemento + 'next=' + tokenNext + '&')

                self.log(urlNextPage)

                yield scrapy.Request(urlNextPage,callback=self.parse, headers=header2, dont_filter=True)

