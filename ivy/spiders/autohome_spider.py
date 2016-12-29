#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re

class IqiyiSpider(scrapy.Spider):
    name = "autohome"
    allowed_domains = ["autohome.com.cn"]

    f = open('input/autohome.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.autohome.com.cn/grade/carhtml/B.html"
    ]
    """

    def parse(self, response):
        urllist = response.css('ul.rank-list-ul li h4 a').xpath('@href').extract()
        with open("output/autohome.out", 'a') as f:
            for url in urllist:
                f.write(re.sub(r'#levelsource=000000000_0&pvareaid=101594$','',url)+"\n")
