# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.utils.log import configure_logging


# configure_logging(install_root_handler=False)
# logging.basicConfig(
#     filename='log.txt',
#     format='%(levelname)s: %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger('naming')

class QuotesSpider(scrapy.Spider):

    def __init__(self,*a, **kw):
        super().__init__(*a, **kw)
        self.data =[]

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.DEBUG
    )

    logger = logging.getLogger('naming')

    name = "quotes"
    start_urls = [
        'http://xh.5156edu.com/bh/b28h44s8.html',
        'http://xh.5156edu.com/bh/b28h44s8_2.html',
        'http://xh.5156edu.com/bh/b28h44s8_3.html',
        'http://xh.5156edu.com/bh/b13h22s13.html',
        'http://xh.5156edu.com/bh/b13h22s13_2.html',
        'http://xh.5156edu.com/bh/b13h22s13_3.html',
        'http://xh.5156edu.com/bh/b64h36s3.html',
        'http://xh.5156edu.com/bh/b67h69s23.html',
        'http://xh.5156edu.com/bh/b84h28s18.html',
        'http://xh.5156edu.com/bh/b84h28s18_2.html'
    ]

    class Hanzi(object):
        def __init__(self,char,pinyin,strokes):
            self.char = char
            self.pinyin = pinyin
            self.strokes = strokes




    def getAll(self,response):

        char = response.xpath("//td[@class='font_22']/text()").get()

        pinyin = response.xpath("//tr[td[b[text()=\"笔划：\"]]]/td[2]/script/text()").get().split("\"")[1]

        Strokes = response.xpath("//tr[td[b[text()=\"笔划：\"]]]/td[4]/text()").get()
        self.data.append(QuotesSpider.Hanzi(char,pinyin,Strokes))




    def parse(self, response):
        # tr = response.xpath("//tr[td[b[text()=\"笔划：\"]]]/td[4]/text()").get()
        # print(tr)
        # print(tr.xpath("//td[3]").get())
        # strokes = tr[3].xpath("text()").get()
        # print(strokes)
        # print(response.xpath(''))
        # for quote in response.css('div.table'):

        for a in response.xpath('//div[1]//a[@class]'):
            next_page = a.xpath('@href').get()
            yield response.follow(next_page, callback=self.getAll)

    def closed(self,reson):
        with open('naming.txt','w+',encoding='utf-8') as fd:
            for candidata in self.data:
                data = ("%s-%s-%s\n")%(candidata.char,candidata.pinyin,candidata.strokes)
                fd.write(data)


        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('span small::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     print("-------------------------------")
        #     print(next_page)
        #     print("-------------------------------")
        #     yield response.follow(next_page, callback=self.parse)