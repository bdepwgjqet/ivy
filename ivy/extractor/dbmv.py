import scrapy

def extract(response):
    '''Extractor for douban movie detail page

    Attributes:
        response: scrapy request response
    '''

    subject = {
        "url": response.url,
        "title": unicode.encode(response.css('title::text').extract()[0],'utf-8'),
        "cn_title": response.css('[property="v:itemreviewed"]::text').extract()
    }
    return subject
