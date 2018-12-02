# -*- coding: utf-8 -*-
import logging

import bs4
import requests
import scrapy

logger = logging.getLogger("s0925")


class S0925Spider(scrapy.Spider):
    """
    爬取中国上市药品
    批准文号/注册证号	药品名称	剂型	规格	参比制剂	标准制剂	批准日期	上市许可持有人
    """
    main_info_list = [
        "批准文号/注册证号",
        "药品名称",
        "剂型",
        "规格",
        "参比制剂",
        "标准制剂",
        "批准日期",
        "上市许可持有人"
    ]

    detail_info_list = [
        "活性成分", "活性成分（英文）", "药品名称", "药品名称（英文）",
        "商品名", "商品名（英文）", "剂型", "给药途径", "规格	", "参比制剂",
        "标准制剂", "TE代码", "ATC代码", "批准文号/注册证号", "批准日期",
        "上市许可持有人", "生产厂商", "上市销售状况", "收录类别",
        "说明书", "审评报告",
    ]

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
        self.max_page = int(div_obj.attrs.get("item-total", 10)) if div_obj else 10
        self.max_page = 1

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
            item = {}
            for index, sub_scope in enumerate(scope.xpath("./td")):
                if index == 1:
                    # 获取药品名称
                    name = sub_scope.xpath("./a/text()").extract()[0]
                    href = sub_scope.xpath("./a/@href").extract()[0]
                    # 获取药品详细信息
                    info_url = "http://202.96.26.102" + href
                    item["name"] = name
                    data = self.parse_detail(info_url, item)
                    # yield scrapy.Request(info_url, meta={'item': item}, callback=self.parse_detail)
                else:
                    text = sub_scope.xpath("./text()")
                    item[self.main_info_list[index]] = text[0].extract() if text else ""

            logger.info(item)

    def parse_detail(self, response):
        """
        解析药品详细信息
        """
        for scope in response.xpath("//body/div[contains(@id, 'container')]/section/table/tbody/tr"):
            logger.info(scope)
        return 'TEST'
