# -*- coding: utf-8 -*-
import scrapy
import requests
import bs4
import logging

logger = logging.getLogger('s0925')


class S0925Spider(scrapy.Spider):
    name = 's0925'
    allowed_domains = ["*"]

    def __init__(self, sdate, edate, *args, **kwargs):
        super(S0925Spider, self).__init__(*args, **kwargs)
        self.base_url = "http://202.96.26.102/index/lists?scpzrq_start=" + sdate + "&scpzrq_end=" + edate
        self.sdate = sdate
        self.edate = edate

        # 获取数据总条数
        response = requests.get(self.base_url)
        soup = bs4.BeautifulSoup(response.text)
        div_obj = soup.select_one('div .pagination')
        self.max_page = int(div_obj.attrs.get('data-total', 10)) if div_obj else 10

    # 启动根请求
    def start_requests(self):
        for page in range(self.max_page):
            page_url = self.base_url + "&page=%d" % (page) if page != 0 else self.base_url
            print(page_url)
            yield scrapy.Request(url=page_url)

    # 解析处理函数
    def parse(self, response):
        logger.info(response.body)
