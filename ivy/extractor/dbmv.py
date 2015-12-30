#!/bin/python
# -*- coding: utf-8 -*-

import scrapy
import re
from ivy.utils import listutils
from ivy.items import DbmvItem
import codecs
import json

def extract(response):
    '''Extractor for douban movie detail page

    Url Pattern:
        http://movie.douban.com/subject/\d+/

    Attributes:
        response: scrapy request response
    '''

    # title
    title = response.css('[property="v:itemreviewed"]::text').extract();
    title = title[0] if title else None
    cn_title = title.split(" ")[0] if title else ""
    other_title = " ".join(title.split(" ")[1:]) if title else ""

    # akas
    xcondition = "text()[preceding-sibling::span='"+"又名:".decode('utf-8')+"']"
    akas = response.css('div#info').xpath(xcondition).extract();
    akas = akas[0].split("/") if akas else [] 
    akas = [x.strip(' ') for x in akas]

    # directors
    director_elems = response.css('a[rel="v:directedBy"]')
    directors = []
    for e in director_elems:
        url = listutils.fetch(e.xpath('@href').extract(),0,"")
        url = "http://movie.douban.com" + url if url else ""
        directors.append({
            "name": listutils.fetch(e.xpath('text()').extract(),0,""),
            "url": url
            })

    # actors
    actor_elems = response.css('a[rel="v:starring"]')
    actors = []
    for a in actor_elems:
        url = listutils.fetch(a.xpath('@href').extract(),0,"")
        url = "http://movie.douban.com" + url if url else ""
        actors.append({
            "name": listutils.fetch(a.xpath('text()').extract(),0,""),
            "url": url
            })

    # release_dates
    release_date_elems = response.css('span[property="v:initialReleaseDate"]').xpath('text()').extract()
    release_dates = []
    for r in release_date_elems:
        match = re.search('([0-9-]+)\((.*?)\)',r)
        date = match.group(1) if match and match.group(1) else r
        location = match.group(2) if match and match.group(2) else ""
        release_dates.append({
            "date": date,
            "location": location
            })

    # intro
    intro = response.css('span[property="v:summary"]').xpath('text()[normalize-space()]').extract()
    intro = "".join([ x.strip() for x in intro ])

    # countries
    xcondition = "text()[preceding-sibling::span='"+"制片国家/地区:".decode('utf-8')+"']"
    countries = response.css('div#info').xpath(xcondition).extract();
    countries = countries[0].split("/") if akas else [] 
    countries = [x.strip(' ') for x in countries]

    # languages
    xcondition = "text()[preceding-sibling::span='"+"语言:".decode('utf-8')+"']"
    languages = response.css('div#info').xpath(xcondition).extract();
    languages = languages[0].split("/") if akas else [] 
    languages = [x.strip(' ') for x in languages]

    # comment_count
    comment = response.css('div#comments-section h2 span.pl a').xpath('text()').extract();
    comment = comment[0] if comment else ""
    comment = re.search('(\d+)',comment)
    comment_count = comment.group(1) if comment and comment.group(1) else ""

    # review_count
    review_count = response.css('div#review_section h2 span.pl a').xpath('text()').extract();
    review_count = review_count[0] if review_count else ""
    review_count = re.search('(\d+)',review_count)
    review_count = review_count.group(1) if review_count and review_count.group(1) else ""

    # imdb_key
    xcondition = "text()[preceding-sibling::span='"+"IMDb链接:".decode('utf-8')+"']"
    imdb_key = response.css('div#info').xpath(xcondition).extract();
    imdb_key = imdb_key[0].split("/") if akas else [] 
    imdb_key = [x.strip(' ') for x in imdb_key]

    # hot reviews
    blocks = response.css('div.review')
    hot_reviews = []
    for i in range(len(blocks)):
        hot_reviews.append({
            "title": response.css('div.review-hd').xpath('h3/a[@onclick]/text()').extract()[i],
            "url": response.css('div.review-hd').xpath('h3/a[@onclick]/@href').extract()[i],
            "author": response.css('div.review-hd-info a').xpath('text()').extract()[i],
            "reply_num": response.css('div.review-short-ft a').xpath('text()').re('(\d+)')[i],
            "rating": int(response.css('div.review-hd-info span').xpath('@class').re('(\d+)')[i])/10
            })

    # final subject
    subject = {
            "category": "movie",
            "cn_title": cn_title,
            "title": other_title,
            "akas": akas,
            "url": response.url,
            "picture": listutils.fetch(response.css('a.nbgnbg img').xpath('@src').extract(),0,""),
            "wap_url": "",
            "html5_url": "",
            "directors": directors,
            "actors": actors,
            "year": listutils.fetch(response.css('.year').xpath('text()').extract(),0,"").lstrip('(').rstrip(')'),
            "release_dates": release_dates,
            "duration": listutils.fetch(response.css('span[property="v:runtime"]').xpath('text()').extract(),0,""),
            "types": response.css('span[property="v:genre"]').xpath('text()').extract(),
            "intro": intro,
            "website": "",
            "countries": countries,
            "languages": languages,
            "rating": listutils.fetch(response.css('strong[property="v:average"]').xpath('text()').extract(),0,""),
            "rating_count": listutils.fetch(response.css('span[property="v:votes"]').xpath('text()').extract(),0,""),
            "comment_count": comment_count,
            "comment_url": listutils.fetch(response.css('div#comments-section h2 span.pl a').xpath('@href').extract(),0,""),
            "review_count": review_count,
            "review_url": listutils.fetch(response.css('div#review_section h2 span.pl a').xpath('@href').extract(),0,""),
            "hot_reviews": hot_reviews,
            "has_schedule": "",
            "is_bookable": "",
            "current_season": "",
            "season_count": "",
            "episode_count": "",
            "tv_channel": "",
            "trailer_url": "",
            "video_url": "",
            "schedule_url": "",
            "ticket_url": "",
            "more_related_url": "",
            "imdbKey": listutils.fetch(imdb_key,0,"")
    }

    # test
    filename = response.url.split("/")[-2] + '.json'
    #filename = 'detail.html'
    output_folder = "output/"
    f = codecs.open(output_folder + filename,'wb',encoding='utf-8')
    f.write(json.dumps(subject).decode('unicode_escape').replace("\n",""))

    sid = re.search('(\d+)',response.url)
    sid = sid.group(1) if sid else -1 
    item = DbmvItem(_id=sid,subject=json.dumps(subject).decode('unicode_escape').replace("\n",""))
    return item
