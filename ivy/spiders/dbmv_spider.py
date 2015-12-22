import scrapy
import json
import re
import codecs
from scrapy.selector import Selector

class DbmvSpider(scrapy.Spider):
    name = "dbmv"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "http://movie.douban.com/tag/"
    ]

    def parse(self, response):
        url_list = response.css('a[href^="http"]').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("http://www.douban.com/tag/\d{4}/\?focus=movie$",x)]
        yield scrapy.Request(url_list[0], callback=self.parse_tag, dont_filter=True)
        '''
        for url in url_list:
            print "Step into tag: "+url
            yield scrapy.Request(url, callback=self.parse_tag, dont_filter=True)
        '''

    def parse_tag(self, response):
        url_list = response.css('a.more-links').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("^http://www.douban.com/link2/.*?mod=movie$",x)]
        if len(url_list) == 1:
            print "Step into movie list page of this tag:" + url_list[0]
            yield scrapy.Request(url_list[0], callback=self.parse_movie_list, dont_filter=True)

    def parse_movie_list(self, response):
        url_list = response.css('a[href^="http"]').xpath('@href').extract()
        url_list = [x for x in url_list if re.match("http://movie.douban.com/subject/\d+",x)]

        yield scrapy.Request(url_list[0], callback=self.parse_movie_detail, dont_filter=True)
        '''
        for url in url_list:
            print "Step into movie detail page: " + url
            yield scrapy.Request(url, callback=self.parse_movie_detail, dont_filter=True)
            '''

        #fetch next page of movie list
        next_url = response.css('span.next a').xpath('@href').extract()
        if len(next_url) == 1:
            nurl = re.sub('\?start=\d+','',response.url) + next_url[0]
            print nurl
            c = re.match('\?start=(\d+)',next_url[0])
            if int(c.group(1)) < 30:
                yield scrapy.Request(nurl, callback=self.parse_movie_list, dont_filter=True)

    def parse_movie_detail(self, response):
        subject = {
            "url": response.url,
            "title": unicode.encode(response.css('title::text').extract()[0],'utf-8'),
            "cn_title": response.css('[property="v:itemreviewed"]::text').extract()
        }

        filename = response.url.split("/")[-2] + '.json'
        #filename = 'detail.html'
        output_folder = "output/"
        f = codecs.open(output_folder + filename,'wb',encoding='utf-8')
        f.write(json.dumps(subject).decode('unicode_escape').replace("\n",""))
