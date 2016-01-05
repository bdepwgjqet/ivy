import scrapy
import json
import re
import codecs
from scrapy.selector import Selector
from ivy.extractor import dbmv

class DbmvSpider(scrapy.Spider):
    name = "dbmv"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "http://movie.douban.com/tag/"
    ]

    def parse(self, response):
        url_list = response.css('a[href^="http"]').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("http://www.douban.com/tag/\d{4}/\?focus=movie$",x)]
        #return scrapy.Request(url_list[0], callback=self.parse_tag, dont_filter=True)
        for url in url_list:
            print "Step into tag: "+url
            yield scrapy.Request(url, callback=self.parse_tag, dont_filter=True)

    def parse_tag(self, response):
        url_list = response.css('a.more-links').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("^http://www.douban.com/link2/.*?mod=movie$",x)]
        if len(url_list) == 1:
            print "Step into movie list page of this tag:" + url_list[0]
            yield scrapy.Request(url_list[0], callback=self.parse_movie_list, dont_filter=True)

    def parse_movie_list(self, response):
        url_list = response.css('a[href^="http"].title').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("http://movie.douban.com/subject/\d+",x)]

        #return scrapy.Request(url_list[0], callback=self.parse_movie_detail, dont_filter=True)
        for url in url_list:
            print "Step into movie detail page: " + url
            yield scrapy.Request(url, callback=self.parse_movie_detail, dont_filter=True)

        #fetch next page of movie list
        if len(url_list) > 0:
            next_url = response.css('span.next a').xpath('@href').extract()
            if len(next_url) == 1:
                nurl = re.sub('\?start=\d+','',response.url) + next_url[0]
                print nurl
                # c = re.match('\?start=(\d+)',next_url[0])
                # if int(c.group(1)) < 30:
                #     yield scrapy.Request(nurl, callback=self.parse_movie_list, dont_filter=True)

                yield scrapy.Request(nurl, callback=self.parse_movie_list, dont_filter=True)

    def parse_movie_detail(self, response):
        item = dbmv.extract(response)
        return item
