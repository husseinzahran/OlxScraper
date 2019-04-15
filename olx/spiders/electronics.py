# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from olx.items import OlxItem


class ElectronicsSpider(scrapy.Spider):
    name = "electronics"
    

    def start_requests(self):
        urls = [
        'https://www.olx.com.pk/computers-accessories_c443',
                
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
                
    def parse(self, response):
        item_links = response.css('ul[data-aut-id="itemsList"] a::attr(href)').extract()
        print("#############################Parsing######################")
        print(item_links)
        for a in item_links:
            #print(a) 
            yield scrapy.Request("https://www.olx.com.pk"+a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print("#############################Page Detail######################")
        title = response.css('h1[data-aut-id="itemTitle"]::text').extract()[0].strip()
        price = response.css('span[data-aut-id="itemPrice"]::text').extract()[0]
        image = response.css('figure *::attr("src")').extract_first()
        item = OlxItem()
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        item['image'] = image
        yield item
