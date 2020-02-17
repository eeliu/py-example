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
    # name = "quotes"

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        # format='%(levelname)s: %(message)s',
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.DEBUG
    )

    logger = logging.getLogger('naming')

    name = "quotes"
    start_urls = [
        # 'http://quotes.toscrape.com/page/1/',
        'http://xh.5156edu.com/bh/b28h44s8.html',
        # 'http://xh.5156edu.com/bh/b28h44s8_2.html',
        # 'http://xh.5156edu.com/bh/b28h44s8_3.html',
        # 'http://xh.5156edu.com/bh/b84h28s18.html'
        # 'http://xh.5156edu.com/html3/1952.html'
    ]

    def getAll(self,response):
        char = response.xpath("//td[@class='font_22']/text()").get()
        pinyin = response.xpath("//td[@class='font_14']/script/text()").get().split("\"")[1]
        Strokes = response.xpath("//tr[td[b[text()=\"笔划：\"]]]/td[4]/text()").get()
        QuotesSpider.logger.info("char %s pinyin %s Strokes:%d",char,pinyin,int(Strokes))


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