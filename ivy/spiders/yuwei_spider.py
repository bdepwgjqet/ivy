#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
import re
import codecs
import base64
from scrapy.selector import Selector

class YuweiSpider(scrapy.Spider):
    name = "yuwei"
    allowed_domains = ["youyuwei.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.youyuwei.com/"
    ]

    def parse(self, response):
        urls = response.css('ul.MDD_z.china li a.cor_bs').xpath('@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.hotel_list, dont_filter=True)

    def hotel_list(self, response):
        urllist = response.css('div.rest_single a.note_title').xpath('@href').extract()
        lat = response.css('div.reset div.rest_single').xpath('@lat').extract()
        lon = response.css('div.reset div.rest_single').xpath('@lng').extract()
        with open('output/yuwei.tsv','a') as f:
            try:
                for i in range(len(urllist)):
                    f.write(urllist[i]+"\t"+lat[i]+"\t"+lon[i]+"\n")
            except:
                print len(urllist),len(lat),len(lon)
