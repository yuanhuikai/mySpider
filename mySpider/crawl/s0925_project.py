#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-11 19:33:59
# @Author  : yhk
"""
==============================================
   s0925启动文件         
==============================================
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="zhangshuai  0925")
    parser.add_argument("-sdate", help="start date")
    parser.add_argument("-edate", help="end date")
    args = parser.parse_args()
    print(args.sdate, args.edate)
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl("s0925", sdate=args.sdate, edate=args.edate)
    process.start()
