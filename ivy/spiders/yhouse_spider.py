#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
import re
import codecs
import base64
from scrapy.selector import Selector

class YhouseSpider(scrapy.Spider):
    name = "yhouse"
    site = "http://www.yhouse.com"
    allowed_domains = ["yhouse.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.yhouse.com/"
    ]

    def parse(self, response):
        urls = response.css('ul.clearfix li a').xpath('@href').extract()
        yield scrapy.Request("http://www.yhouse.com/city/2", callback=self.city_res, dont_filter=True)
        for url in urls:
            print "Curcity: " + self.site + url
            cityres = self.site + url
            yield scrapy.Request(cityres, callback=self.city_res, dont_filter=True)

    def city_res(self, response):
        restaurants = response.css('li.list-li a').xpath('@href').extract()
        with open('output/yhouse.tsv','a') as f:
            try:
                for url in restaurants:
                    f.write(self.site + url + "\t10\n")
            except:
                print len(restaurants) + ": " + restaurants

        pages = response.css('ul.pages li a').xpath('@href').extract()
        values = response.css('ul.pages li a').xpath('text()').extract()
        print values
        if u'\u4e0b\u4e00\u9875' in values:
            nextpage = self.site + pages[-1]
            print 'nextpage is: ' + nextpage
            yield scrapy.Request(nextpage , callback=self.city_res, dont_filter=True)
