# -*- coding: utf-8 -*-

import time

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class MyspiderPipeline(object):
    """
    pizhunwh = scrapy.Field()  # 批准文号
    yaopinmc = scrapy.Field()  # 药品名称
    jixing = scrapy.Field()  # 剂型
    guige = scrapy.Field()  # 规格
    canbizj = scrapy.Field()  # 参比制剂
    biaozhunzj = scrapy.Field()  # 标准制剂
    pizhunrq = scrapy.Field()  # 批准日期
    shangshixukecyr = scrapy.Field()  # 上市许可参与人
    huoxingcf = scrapy.Field()  # 活性成分
    huoxingcf_en = scrapy.Field()  # 活性成分-英文
    yaopinmc_en = scrapy.Field()  # 药品名称-英文
    shangpinm = scrapy.Field()  # 商品名
    shangpinm_en = scrapy.Field()  # 商品名-英文
    geiyaotj = scrapy.Field()  # 给药途径
    tedaima = scrapy.Field()  # te 代码
    atcdaima = scrapy.Field()  # atc 代码
    shengchancs = scrapy.Field()  # 生产厂商
    shangshixiaoshouzk = scrapy.Field()  # 上市销售状况
    shoululb = scrapy.Field()  # 收录类别
    shuomingshu = scrapy.Field()  # 说明书
    pingshenbg = scrapy.Field()  # 审评报告
    url = scrapy.Field()  # 药品名称链接
    """

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append([
            '批准文号', '药品名称', '剂型', '规格', '参比制剂',
            '标准制剂', '批准日期', '上市许可参与人', '活性成分', '活性成分-英文',
            '药品名称-英文', '商品名', '商品名-英文', '给药途径', "TE 代码",
            "ATC 代码", "生产厂商", "上市销售状况", "收录类别", "说明书",
            "审评报告", "药品名称链接"
        ])

    def process_item(self, item, spider):
        self.ws.append([
            item['pizhunwh'], item["yaopinmc"], item["jixing"], item['guige'], item['canbizj'],
            item['biaozhunzj'], item['pizhunrq'], item['shangshixukecyr'], item['huoxingcf'], item['huoxingcf_en'],
            item['yaopinmc_en'], item['shangpinm'], item['shangpinm_en'], item['geiyaotj'], item['tedaima'],
            item['atcdaima'], item['shengchancs'], item['shangshixiaoshouzk'], item['shoululb'], item['shuomingshu'],
            item['pingshenbg'], item['url'],
        ])
        return item

    def close_spider(self, spider):
        """
        当爬虫关闭时调用
        :param spider:
        :return:
        """
        self.wb.save("~/" + time.strftime("%Y%m%d%H%M") + "中国上市药品.xlsx")
