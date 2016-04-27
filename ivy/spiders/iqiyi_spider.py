#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import json
import re
import codecs
import base64
from scrapy.selector import Selector

class IqiyiSpider(scrapy.Spider):
    name = "iqiyi"
    allowed_domains = ["iqiyi.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.iqiyi.com/lib/m_205517614.html"
    ]

    def parse(self, response):
        title = response.css('h1#widget-videotitle.mod-play-tit').xpath('text()').extract()
        title = title[0] if title else None
        title = title.strip()
        url = 'http://so.iqiyi.com/so/q_' + title + '?source=input&refersource=lib'
        print url
        yield scrapy.Request(url, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        url = response.css('h3.result_title a').xpath('@href').extract()
        url = url[0] if url else None
        url = url.split('?')
        url = url[0] if url else None
        match = re.match("^(http)://(www\.)?iqiyi\.com/lib/m_\d+\.html$", url)
        if match:
            with open('iqiyi.tsv','a') as f:
                f.write(url+'\n')
            yield scrapy.Request(url, callback=self.crawl_detail, dont_filter=True)

    def crawl_detail(self, response):
        content = response.body
        content = content.replace('\n',' ').replace('\r','')
        url = response.url
        b64c = base64.b64encode(content)
        with open('iqiyidetail.tsv','a') as f:
            f.write(url+'\t'+content+'\n')
        with open('iqiyidetail-b64.tsv','a') as f:
            f.write(url+'\t'+b64c+'\n')
