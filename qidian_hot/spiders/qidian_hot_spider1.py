# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/9/1 18:43
@File     : qidian_hot_spider1.py
@Describe : 通过设置请求头、自定义实现解析函数
"""

from scrapy import Request
from scrapy.spiders import Spider


class HotSalesSpider(Spider):
    # 定义爬虫名称
    name = 'hot1'

    # 更通用的做法是在配置文件中设置User-Agent
    # # 设置用户代理（浏览器类型）
    # qidian_headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

    # 获取初始化
    def start_requests(self):
        url = "https://www.qidian.com/rank/hotsales/page1/"
        # 生成请求对象，设置url、headers、callback
        yield Request(url,
                      # headers=self.qidian_headers,
                      callback=self.qidian_parse)


    # # 起始的URL列表
    # start_urls = ["https://www.qidian.com/rank/hotsales/page1/", "https://www.qidian.com/rank/hotsales/page2/"]

    # 解析函数
    def qidian_parse(self, response):
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
            # 每接收一条数据就提交到引擎，进行后续处理，节省内存，提高执行效率
            yield hot_dict
