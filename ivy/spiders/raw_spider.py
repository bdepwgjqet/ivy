#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import base64


class RawSpider(scrapy.Spider):

    name = "raw"
    # allowed_domains = ["iqiyi.com", "douban.com", "letv.com", "qq.com"]

    f = open('input/urllist.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.iqiyi.com/lib/m_205517614.html"
    ]
    """

    def parse(self, response):
        content = response.body
        content = content.replace('\n', ' ').replace('\r', '')
        url = response.url
        b64c = base64.b64encode(content)
        with open('output/raw.tsv', 'a') as f:
            f.write(url+'\t'+content+'\n')
        with open('output/raw-base64.tsv', 'a') as f:
            f.write(url+'\t'+b64c+'\n')
