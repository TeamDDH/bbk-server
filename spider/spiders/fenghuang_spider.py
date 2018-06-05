# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from spider.config import START_POINTS
from spider.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class FenghuangSpider(scrapy.Spider):
    name = 'fenghuang'
    start_urls = [START_POINTS['ifeng']]

    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if "//news.ifeng.com" in link.url:
                yield Request(url=link.url, callback=self.parse_article)

    def parse_article(self, response):
        """In this parser, a new article item would be created and
        in `pipeline.py` it would be stored into database."""
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'fenghuang')
        loader.add_value('crawled_at', datetime.now().strftime('%Y-%m-%d'))
        content_list1 = response.xpath('//div[contains(@id,"main_content")]')
        content_list2 = response.xpath('//div[contains(@id,"slidedesc2")]')
        content_list3 = response.xpath('//div[contains(@class,"yaow")]')
        content_list = content_list1.xpath('.//p/text()') + content_list2.xpath('.//p/text()') + content_list3.xpath(
            './/p/text()')
        content = ""
        for content_one in content_list:
            content += content_one.extract().strip()
        loader.add_value('content', content)
        published = response.xpath('//span[@class="ss03"]')
        published_at = published.xpath('./text()').extract()
        loader.add_value('published_at', published_at)
        edi = response.xpath('//p[@class="iphone_none"]')
        editor = edi.xpath('./text()').extract()
        loader.add_value('editor', editor)
        time = response.xpath('//span[@class="ss01"]')
        published_time = time.xpath('./text()').extract()
        loader.add_value('published_time', published_time)
        item = loader.load_item()
        yield item
