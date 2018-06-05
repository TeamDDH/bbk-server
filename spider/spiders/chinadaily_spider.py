# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from spider.config import START_POINTS
from spider.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class ChinadailySpider(scrapy.Spider):
    name = 'chinadaily'
    start_urls = [START_POINTS['chinadaily']]

    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:
            if "http://china.chinadaily.com.cn/" in link.url:
                yield Request(url=link.url, callback=self.parse_page)

    def parse_page(self, response):
        for link in LinkExtractor(allow=()).extract_links(response):
            if "http://china.chinadaily.com.cn/" in link.url:
                yield Request(url=link.url, callback=self.parse_article)
                yield Request(url=link.url, callback=self.parse_page)

    def parse_article(self, response):
        """In this parser, a new article item would be created and
        in `pipeline.py` it would be stored into database."""
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'chinadaily')
        loader.add_value('crawled_at', datetime.now().strftime('%Y-%m-%d'))
        # 将p标签里的文本内容合并到一起
        content_list1 = response.xpath('//div[contains(@id,"Content")]')
        content_list = content_list1.xpath('.//p/text()')
        content = ""
        for content_one in content_list:
            content += content_one.extract().strip()
        loader.add_value('content', content)
        published = response.xpath('//div[@id="source"]')
        published_at = published.xpath('./text()').extract()
        loader.add_value('published_at', published_at)
        # edi = response.xpath('//span[@class="ep_editor"]')
        # editor = edi.xpath('./text()').extract()
        # loader.add_value('editor', editor)
        time = response.xpath('//div[@id="pubtime"]')
        published_time = time.xpath('./text()').extract()
        loader.add_value('published_time', published_time)
        item = loader.load_item()
        yield item
