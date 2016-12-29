#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import time
from scrapy.spiders import CrawlSpider
from selenium import webdriver

class CtripSpider(scrapy.Spider):
    name = "ctrip"
    allowed_domains = ["you.ctrip.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://you.ctrip.com/photos/aachen1677/r1677-19722106.html"
    ]

    def __init__(self):
        #CrawlSpider.__init__(self)
        self.browser = webdriver.Firefox()

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        with open('output/ctripcityimg.tsv','a') as f:
            f.write(response.html)
