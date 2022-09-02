# -*- coding: utf-8 -*-
"""
@Author   : chulang
@DateTime : 2022/9/2 17:26
@File     : xiechen.py
@Describe : TODO
"""
from scrapy import Request
from scrapy import Spider


class XieChenSpider(Spider):
    name = 'xie_chen'

    def start_requests(self):
        url = "https://hotels.ctrip.com/hotels/88610270.html?cityid=2#ctm_ref=www_hp_bs_lst"
        yield Request(url, callback=self.xiechen_parse)

    def xiechen_parse(self, response):
        list_selector = response.xpath("//*[@class='list'")

        for one_selector in list_selector:
            print(one_selector)

