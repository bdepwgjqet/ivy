#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re

class DianpingtrSpider(scrapy.Spider):
    name = "dianpingtr"
    allowed_domains = ["dianping.com"]

    """
    f = open('iqiyinotinsnapp.tsv')
    start_urls = [url.strip() for url in f.readlines()]
    """
    start_urls = [
        "http://www.dianping.com/beijing"
    ]

    cityres = {}

    def parse(self, response):
        urllist = response.css('div.group.clearfix a').xpath('@href').extract()
        citylist = response.css('div.group.clearfix a').xpath('text()').extract()

        cityurl = {}
        for i in range(len(urllist)):
            cityurl[citylist[i].encode('utf-8')] = urllist[i].encode('utf-8')
            #yield scrapy.Request(furl, callback=self.hotel_list, dont_filter=True)

        #print cityurl

        trf = open('input/TopResOfCity.tsv')
        trlines = [x.strip() for x in trf.readlines()]
        allres = []
        for line in trlines:
            cols = line.split('\t')
            if len(cols) < 4:
                continue
            if cols[3] == "广州深圳":
                allres.append((cols[0], "广州"))
                allres.append((cols[0], "深圳"))
            elif cols[3] == "江浙":
                allres.append((cols[0], "杭州"))
            elif cols[3] == "港澳":
                allres.append((cols[0], "香港"))
            else:
                allres.append((cols[0], cols[3]))

        for (r,c) in allres:
            if c not in self.cityres:
                self.cityres[c] = []
            self.cityres[c].append(r)

        for k in self.cityres:
            if k in cityurl:
                #print cityurl[k] + "--->"
                yield scrapy.Request(cityurl[k], callback=self.city_crawl, dont_filter=True)
                #break

        for k in self.cityres:
            cur = k + ":"
            for r in self.cityres[k]:
                cur += "\t" + r
            #print cur + "\n"


    def city_crawl(self, response):
        ccityid = response.css('div.search-bar input').xpath('@data-s-cityid').extract()
        ccityid = int(ccityid[0]) if len(ccityid) > 0 else -1
        cityname = response.css('a.city.J-city').xpath('text()').extract()
        cityname = cityname[0].encode('utf-8').strip("\"") if len(cityname) > 0 else ""

        #print ccityid, cityname

        if cityname in self.cityres:
            for res in self.cityres[cityname]:
                curl = "http://www.dianping.com/search/keyword/" + str(ccityid) \
                    + "/0_" + res
                #print curl
                yield scrapy.Request(curl, callback=self.res_list_crawl, dont_filter=True)

    def res_list_crawl(self, response):
        res_list = response.css('ul li div.txt div.tit a').xpath('@href').extract()
        res_list = "http://www.dianping.com" + res_list[0] if len(res_list) > 0 else ""
        #print res_list
        if res_list:
            yield scrapy.Request(res_list, callback=self.res_crawl, dont_filter=True)

    def res_crawl(self, response):
        cityname = response.css('a.city.J-city').xpath('text()').extract()
        cityname = cityname[0].encode('utf-8').strip("\"").strip() if len(cityname) > 0 else ""

        shopname = response.css('h1.shop-name').xpath('text()').extract()
        shopname = shopname[0].encode('utf-8').strip("\"").strip() if len(shopname) > 0 else ""

        ccnt = response.css('a.item.current span.sub-title').xpath('text()').extract()
        ccnt = ccnt[0].encode('utf-8').strip("(").strip(")") if len(ccnt) > 0 else ""

        tags = response.css('span.good.J-summary a').xpath('text()').extract()
        tagtext = ""
        for tag in tags:
            if tagtext:
                tagtext += " / "
            tagtext += tag.encode('utf-8')

        comments = response.css('div.content p.desc').xpath('text()').extract()
        comtext = ""
        for comment in comments:
            if comtext:
                comtext += "###SEP###"
            comtext += comment.encode('utf-8')

        print cityname + "\t" + shopname + "\t" + ccnt + "\t" + response.url + \
            "\t" + "\t" + "\t" + "\t" + comtext + "\t" + tagtext
