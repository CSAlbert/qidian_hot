# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


# 对形式字段做转换的Item Pipeline
class QidianHotPipeline:
    def process_item(self, item, spider):
        if item["form"] == "连载":
            item["form"] = "LZ"
        else:
            item["form"] = "WJ"
        return item


# 去除重复作者的Item Pipeline
class DuplicatesPipeline(object):
    def __init__(self):
        # 定义一个保持作者姓名的集合
        self.author_set = set()

    def process_item(self, item, spider):
        if item['author'] in self.author_set:
            # 抛弃重复的Item项
            raise DropItem("查找到重复姓名的项目：%s" % item)
        else:
            self.author_set.add(item['author'])
        return item


# 将数据保存于文本文档中的Item Pipeline
class SaveToTxtPipeline(object):
    file_name = "hot.txt"  # 文件名称
    file = None  # 文件对象

    # Spider开启时，执行打开文件操作
    def open_spider(self, spider):
        # 以追加形式打开文件
        self.file = open(self.file_name, "a", encoding="utf-8")

    # 数据处理
    def process_item(self,item,spider):
        # 获取item中的各个字段，将其连接成一个字符串
        # 字段之间用分号隔开
        # 字符串结尾要有换行符
