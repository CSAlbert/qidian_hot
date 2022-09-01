# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/8/31 9:41
@File     : qidian_hot_spider.py
@Describe : 起点热门小说排行爬取
            执行：scrapy crawl hot -o hot.csv
"""

from scrapy import Request
from scrapy.spiders import Spider


class HotSalesSpider(Spider):
    # 定义爬虫名称
    name = 'hot'
    # 起始的URL列表
    start_urls = ["https://www.qidian.com/rank/hotsales/page1/", "https://www.qidian.com/rank/hotsales/page2/"]

    # 解析函数
    def parse(self, response):
        # 使用xpath定位到小说内容的div元素，保存到列表中
        list_selector = response.xpath("//*[@class='book-mid-info']")
        print(list_selector)

        # 依次读取每部小说的元素，从中获取名称、作者、类型和形式
        for one_selector in list_selector:
            # print(one_selector)
            # 获取小说名称
            name = one_selector.xpath("h2/a/text()").extract()[0]
            # 获取作者
            author = one_selector.xpath("p[1]/a[1]/text()").extract()[0]
            # 获取类型
            type = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            # 获取形式（连载/完本）
            form = one_selector.xpath("p[1]/span/text()").extract()[0]
            # 将爬取到的一部小说保存到字典中
            hot_dict = {"name": name, "author": author, "type": type, "form": form}

            yield hot_dict
