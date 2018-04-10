import scrapy


class LocalWeb(scrapy.Spider):
    name = 'sunSpider'
    start_urls = ['https://www.thesun.co.uk/news/5883380/france-hostage-situation-trebes-super-u-supermarket-isis/']

    custom_settings = {
        'USER_AGENT': 'sunSpider',
        'DOWNLOAD_DELAY': 0.5,
        'FEED_EXPORT_ENCODING': 'utf-8', 
        'DEPTH_LIMIT': 30
    }

    def parseElement(self, article, selectors):
        for selector in selectors:
            options = article.css(selector).extract()
            for text in options:  
                if text is not None:
                    text = text.replace('\n', '')
                if text:
                    return text
        return None

    def parse(self, response):
        for article in response.css('article'):
            yield {'title': self.parseElement(article, ['h1.article__headline ::text',
                                                        'h1.article__headline--immersive--with-main-media ::text',
                                                        'h1.is-hidden ::text']),
                   'description': self.parseElement(article, ['p.article__content.article__content--intro ::text',
                                                              '.hide-on-mobile > div > meta ::attr(content)']),
                   'author': self.parseElement(article,
                                               ['a[rel="author"] > span ::text', 'span[itemprop="author"] ::text',
                                                'p[itemprop="author"] ::text']),
                   'published': self.parseElement(article, ['.article__published > span ::text']),
                   
                   'url': response.request.url
                   }

        related = response.css('.sun-row > li > div > div > div > div > div > a ::attr(href)').extract()
        for page in related:
            yield scrapy.Request(response.urljoin(page), callback=self.parse)

        main_cat = response.css('.submeta__section-labels > ul > li > a ::attr(href)').extract()
        for page in main_cat:
            yield scrapy.Request(response.urljoin(page), callback=self.parse)

        categories = response.css('.submeta__keywords > ul > li > a ::attr(href)').extract()
        for page in categories:
            yield scrapy.Request(response.urljoin(page), callback=self.parse)

        in_cat = response.css('.rail__item-content > a ::attr(href)').extract()
        for page in in_cat:
            yield scrapy.Request(response.urljoin(page), callback=self.parse)

        categ = response.css('div > div > div > a ::attr(href)').extract()
        for page in categ:
            yield scrapy.Request(response.urljoin(page), callback=self.parse)
