# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/9/1 18:43
@File     : qidian_hot_spider1.py
@Describe : 通过设置请求头、自定义实现解析函数
"""

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader

from qidian_hot.items import QidianHotItem


class HotSalesSpider(Spider):
    # 定义爬虫名称
    name = 'hot_item_loader'

    # 设置当前页，起始为1
    current_page = 1

    # 获取初始化
    def start_requests(self):
        url = "https://www.qidian.com/rank/hotsales/page1/"
        # 生成请求对象，设置url、headers、callback
        yield Request(url, callback=self.qidian_parse)

    # 解析函数
    def qidian_parse(self, response):
        # 使用xpath定位到小说内容的div元素，保存到列表中
        list_selector = response.xpath("//*[@class='book-mid-info']")

        # 依次读取每部小说的元素，从中获取名称、作者、类型和形式
        for one_selector in list_selector:
            # 生成ItemLoader的实例
            # 参数item接收QidianHotItem实例，selector接收一个选择器
            novel = ItemLoader(item=QidianHotItem(), selector=one_selector)
            # 使用XPath选择器获取小说名称
            novel.add_xpath("name", "h2/a/text()")
            # 使用XPath选择器获取作者
            novel.add_xpath("author", "p[1]/a[1]/text()")
            # 使用XPath选择器获取类型
            novel.add_xpath("type", "p[1]/a[2]/text()")
            # 使用CSS选择器获取小说形式（连载还是完本）
            novel.add_xpath("form", "p[1]/span/text()")
            # 将提取好的数据load出来，并使用yield返回
            yield novel.load_item()

        # for one_selector in list_selector:
        #     # print(one_selector)
        #     # 获取小说名称
        #     name = one_selector.xpath("h2/a/text()").extract()[0]
        #     # 获取作者
        #     author = one_selector.xpath("p[1]/a[1]/text()").extract()[0]
        #     # 获取类型
        #     type = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
        #     # 获取形式（连载/完本）
        #     form = one_selector.xpath("p[1]/span/text()").extract()[0]
        #     # 将爬取到的一部小说保存到字典中
        #     # hot_dict = {"name": name, "author": author, "type": type, "form": form}
        #     # 每接收一条数据就提交到引擎，进行后续处理，节省内存，提高执行效率
        #     # yield hot_dict
        #
        #     # 将爬取到的一部小说保存到item中
        #     # 定义QidianHotItem对象
        #     item = QidianHotItem()
        #     item["name"] = name
        #     item["author"] = author
        #     item["type"] = type
        #     item["form"] = form
        #
        #     # 使用yield返回item
        #     yield item

        # 获取下一页URL，并生成Request请求，提交给引擎
        # 1. 获取下一页URL
        self.current_page += 1
        if self.current_page <= 5:
            next_url = "https://www.qidian.com/rank/hotsales/page{}/".format(self.current_page)

            print(next_url)
            # 2. 根据URL生成Request，使用yield返回给引擎
            yield Request(next_url, callback=self.qidian_parse)
