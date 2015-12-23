#!/bin/python
# -*- coding: utf-8 -*-

import scrapy
from ivy.utils import listutils

def extract(response):
    '''Extractor for douban movie detail page

    Url Pattern:
        http://movie.douban.com/subject/\d+/

    Attributes:
        response: scrapy request response
    '''

    #title
    title = response.css('[property="v:itemreviewed"]::text').extract();
    title = title[0] if title else None
    cn_title = title.split(" ")[0] if title else ""
    other_title = " ".join(title.split(" ")[1:]) if title else ""

    #akas
    xcondition = "text()[preceding-sibling::span='"+"又名:".decode('utf-8')+"']"
    akas = response.css('div#info').xpath(xcondition).extract();
    akas = akas[0].split("/") if akas else [] 
    akas = [x.strip(' ') for x in akas]

    #directors
    director_elems = response.css('a[rel="v:directedBy"]')
    directors = []
    for e in director_elems:
        url = listutils.fetch(e.xpath('@href').extract(),0,"")
        url = "http://movie.douban.com" + url if url else ""
        directors.append({
            "name": listutils.fetch(e.xpath('text()').extract(),0,""),
            "url": url
            })

    #final subject
    subject = {
            "category": "movie",
            "cn_title": cn_title,
            "title": other_title,
            "akas": akas,
            "url": response.url,
            "picture": listutils.fetch(response.css('a.nbgnbg img').xpath('@src').extract(),0,""),
            "wap_url": "",
            "html5_url": "",
            "directors": directors
    }
    return subject

# and following-sibling::br
