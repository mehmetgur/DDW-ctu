import scrapy                                                               
import logging                                                              
                                                                            
logging.getLogger('scrapy').setLevel(logging.WARNING)                       
                                                                            
                                                                            
class SpiderMg(scrapy.Spider):
    name = 'ImdbSpider'                                                     
    start_urls = ['http://www.imdb.com/chart/boxoffice']
    
    def parse(self, response):
        for e in response.css('div#boxoffice>table>tbody>tr'):
            yield {
                
                'weekend': ''.join(e.css('td.ratingColumn')[0].css('::text').extract()).strip(),
                'gross': ''.join(e.css('td.ratingColumn')[1].css('span.secondaryInfo::text').extract()).strip(),
                'weeks': ''.join(e.css('td.weeksColumn::text').extract()).strip(),
                'image': e.css('td.posterColumn img::attr(src)').extract_first(),
                'title': ''.join(e.css('td.titleColumn>a::text').extract()).strip(),
            }



