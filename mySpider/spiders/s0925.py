# -*- coding: utf-8 -*-
import logging

import bs4
import requests
import scrapy

from ..items import cdeItem

logger = logging.getLogger("s0925")


class S0925Spider(scrapy.Spider):
    """
    爬取中国上市药品
    批准文号/注册证号	药品名称	剂型	规格	参比制剂	标准制剂	批准日期	上市许可持有人
    """
    main_info_list = [
        "pizhunwh",
        "yaopinmc",
        "jixing",
        "guige",
        "canbizj",
        "biaozhunzj",
        "pizhunrq",
        "shangshixukecyr"
    ]

    detail_info_list = [
        "huoxingcf", "huoxingcf_en", "yaopinmc", "yaopinmc_en",
        "shangpinm", "shangpinm_en", "jixing", "geiyaotj", "guige", "canbizj",
        "biaozhunzj", "tedaima", "atcdaima", "pizhunwh", "pizhunrq",
        "shangshixukecyr", "shengchancs", "shangshixiaoshouzk", "shoululb",
        "shuomingshu", "pingshenbg",
    ]

    detail_info_map = {
        "活性成分": "huoxingcf",
        "活性成分（英文）": "huoxingcf_en",
        "药品名称": "yaopinmc",
        "药品名称（英文）": "yaopinmc_en",
        "商品名": "shangpinm",
        "商品名（英文）": "shangpinm_en",
        "剂型": "jixing",
        "给药途径": "geiyaotj",
        "规格": "guige",
        "参比制剂": "canbizj",
        "标准制剂": "biaozhunzj",
        "TE代码": "tedaima",
        "ATC代码": "atcdaima",
        "批准文号/注册证号": "pizhunwh",
        "批准日期": "pizhunrq",
        "上市许可持有人": "shangshixukecyr",
        "生产厂商": "shengchancs",
        "上市销售状况": "shangshixiaoshouzk",
        "收录类别": "shoululb",
        "说明书": "shuomingshu",
        "审评报告": "pingshenbg",
    }

    name = "s0925"
    allowed_domains = ["*"]

    def __init__(self, sdate, edate, *args, **kwargs):
        super(S0925Spider, self).__init__(*args, **kwargs)
        self.base_url = "http://202.96.26.102/index/lists?scpzrq_start=" + sdate + "&scpzrq_end=" + edate
        self.sdate = sdate
        self.edate = edate

        # 获取数据总条数
        response = requests.get(self.base_url)
        soup = bs4.BeautifulSoup(response.text)
        div_obj = soup.select_one("div .pagination")
        self.max_page = 20

    def start_requests(self):
        """
        启动根请求
        :return:
        """
        for page in range(self.max_page):
            page_url = self.base_url + "&page=%d" % (page) if page != 0 else self.base_url
            yield scrapy.Request(url=page_url)

    def parse(self, response):
        """
        解析处理函数
        :param response:
        :return:
        """
        for scope in response.xpath(
                "//body/div[contains(@id, 'container')]/section/div[contains(@class, 'showBox')]/div/table/tbody/tr"):
            item = cdeItem()
            info_url = "http://202.96.26.102"
            for index, sub_scope in enumerate(scope.xpath("./td")):
                if index == 1:
                    # 获取药品名称
                    name = sub_scope.xpath("./a/text()").extract()
                    href = sub_scope.xpath("./a/@href").extract()
                    info_url += href[0].strip() if href else ""  # 药品信息信息链接
                    item[self.main_info_list[index]] = name[0].strip() if name else ""
                else:
                    text = sub_scope.xpath("./text()").extract()
                    item[self.main_info_list[index]] = text[0].strip() if text else ""
            yield scrapy.Request(info_url, meta={"item": item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        """
        解析药品详细信息
        """
        item = response.meta.get("item")
        for index, scope in enumerate(response.xpath("//section/table[contains(@class, 'drug-lists')]/tr")):
            if index != 19:
                text = scope.xpath("./td")[1].xpath("./text()")
                text = text[0].extract().strip() if text else ""
            else:
                text = scope.xpath("./td")[1].xpath("./a/@href")
                text = "http:" + text[0].extract().strip() if text else ""
            attr_name = scope.xpath("./td/text()")[0].extract().strip()
            attr_name_en = self.detail_info_map.get(attr_name, "")
            if attr_name_en:
                item[attr_name_en] = text
        item["url"] = response.url
        return item
