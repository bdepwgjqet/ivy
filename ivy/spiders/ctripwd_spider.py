#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re

class CtripwdSpider(scrapy.Spider):
    name = "ctripwd"
    allowed_domains = ["you.ctrip.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://you.ctrip.com/searchsite/hotel/?query=%E5%90%88%E8%82%A5%E4%B8%87%E8%BE%BE&isAnswered=&isRecommended=&publishDate=&PageNo=1",
        "http://you.ctrip.com/searchsite/hotel/?query=%E5%90%88%E8%82%A5%E4%B8%87%E8%BE%BE&isAnswered=&isRecommended=&publishDate=&PageNo=2",
        "http://you.ctrip.com/searchsite/hotel/?query=%E5%8D%97%E6%98%8C%E4%B8%87%E8%BE%BE&isAnswered=&isRecommended=&publishDate=&PageNo=1",
        "http://you.ctrip.com/searchsite/hotel/?query=%E5%8D%97%E6%98%8C%E4%B8%87%E8%BE%BE&isAnswered=&isRecommended=&publishDate=&PageNo=2"
    ]

    def parse(self, response):
        urllist = response.css('li.cf a.pic').xpath('@href').extract()
        for url in urllist:
            furl = "http://you.ctrip.com" + url
            yield scrapy.Request(furl, callback=self.hotel_list, dont_filter=True)

    def hotel_list(self, response):
        price = response.css('p.hdetail_price em').xpath('text()').extract()
        name = response.css('div.hdetail_title h1').xpath('text()').extract()
        hot = response.css('li.current a span').xpath('text()').extract()
        tags = response.css('div#CommentTag.hot_words a').xpath('text()').extract()
        url = response.url
        rhtml = response.body
        hotelid = re.search('hotelId: (\d+)', rhtml)
        hotelid = hotelid.group(1) if hotelid else ""

        price = price[0].encode('utf-8') + "起" if len(price) > 0 else ""
        name = name[0].encode('utf-8') if len(name) > 0 else ""
        hot = hot[0].encode('utf-8').replace("(","").replace(")","") if len(hot) > 0 else ""

        print name + "\t" + price  + "\t" + hot + "\t" \
        + "/".join([x.encode('utf-8').strip() for x in tags]) + "\t" + url + "\t" + hotelid
