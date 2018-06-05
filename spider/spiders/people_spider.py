# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from spider.config import START_POINTS
from spider.items import ArticleItem
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request


class PeopleSpider(scrapy.Spider):
    name = 'people'
    start_urls = [START_POINTS['people']]

    def parse(self, response):
        links = LinkExtractor(allow=()).extract_links(response)
        for link in links:  # 如果包含则继续爬取
            if "//world.people.com.cn" in link.url:
                yield Request(url=link.url, callback=self.parse_page)

    def parse_page(self, response):
        for link in LinkExtractor(allow=()).extract_links(response):
            if "//world.people.com.cn" in link.url:
                yield Request(url=link.url, callback=self.parse_article)
                yield Request(url=link.url, callback=self.parse_page)

    def parse_article(self, response):
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_css('title', 'h1::text')
        loader.add_value('uri', response.url)
        loader.add_value('source', 'people')
        loader.add_value('crawled_at', datetime.now().strftime('%Y-%m-%d'))
        # 将p标签里的文本内容合并到一起
        content_list1 = response.xpath('//div[contains(@id,"rwb_zw")]')
        content_list2 = response.xpath('//div[contains(@class,"content clear clearfix")]')
        content_list3 = response.xpath('//div[contains(@id,"p_content")]')
        content_list = content_list1.xpath('.//p/text()') + content_list2.xpath('.//p/text()') + content_list3.xpath(
            './/p/text()')
        content = ""
        for content_one in content_list:
            content += content_one.extract().strip()
        loader.add_value('content', content)
        edi = response.xpath('//div[@class="edit clearfix"]')
        editor = edi.xpath('./text()').extract()
        loader.add_value('editor', editor)
        item = loader.load_item()
        yield item
