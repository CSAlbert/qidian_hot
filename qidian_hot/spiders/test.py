# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/9/1 19:54
@File     : test.py
@Describe : TODO
"""
from scrapy import Spider
from scrapy import Request

from qidian_hot.items import QidianHotItem


class HotSalesSpider(Spider):
    name = 'qidian_hot'
    current_page = 1

    # 获取初始化
    def start_requests(self):
        url = "https://www.qidian.com/rank/hotsales/page1/"
        yield Request(url, callback=self.qidian_parse)

    # 解析函数
    def qidian_parse(self, response):
        # 使用xpath定位到该页面单个小说内容的div元素，保持到列表
        list_selector = response.xpath("//*[@class='book-mid-info']")

        # 依次读取每部小说的元素，从中获取名称、作者、类型和形式
        for one_selector in list_selector:
            name = one_selector.xpath("h2/a/text()").extract()[0]
            author = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            type = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            form = one_selector.xpath("p[1]/span/text()").extract()[0]
            item = QidianHotItem()
            item["name"] = name
            item["author"] = author
            item["type"] = type
            item["form"] = form

            yield item

        # 获取下一页URL，并生成Request请求，提交给引擎
        # 1. 获取下一页URL
        self.current_page += 1
        if self.current_page <= 5:
            next_url = "https://www.qidian.com/rank/hotsales/page{}/".format(self.current_page)
            print("***********" + next_url)

            # 2. 根据URL生成Request，使用yield返回给引擎
            yield Request(next_url, callback=self.qidian_parse)
