# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from datetime import datetime
from spider.config import START_POINTS
from spider.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class CCTVSpider(scrapy.Spider):
    name = 'cctv'
    start_urls = [START_POINTS['cctv']]

    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if "//news.cctv.com/2018/" in link.url:
                yield Request(url=link.url, callback=self.parse_article)

    def parse_article(self, response):
        """In this parser, a new article item would be created and
        in `pipeline.py` it would be stored into database."""
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'cctv')
        loader.add_value('crawled_at', datetime.now().strftime('%Y-%m-%d'))
        content_list1 = response.xpath('//div[contains(@class,"cnt_bd")]')
        content_list = content_list1.xpath('.//p/text()')
        content = ""

        for content_one in content_list:
            content += content_one.extract().strip()
        loader.add_value('content', content)

        published = response.xpath('//span[@class="info"]')
        published_at = published.xpath('./text()').extract()
        loader.add_value('published_at', published_at)

        item = loader.load_item()
        yield item
