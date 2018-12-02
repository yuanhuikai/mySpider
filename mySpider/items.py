# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class cdeItem(scrapy.Item):
    # define the fields for your item here like:
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
