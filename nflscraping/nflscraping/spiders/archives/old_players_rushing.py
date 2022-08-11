from unicodedata import name
import scrapy

class Playersrushing2021Spider(scrapy.Spider):
    name = 'playersrushing2021'
    start_urls = ['https://www.nfl.com/stats/player-stats/category/rushing/2021/reg/all/rushingyards/desc']

    def parse(self, response):

        for players in response.css('tbody > tr'):
            #try:
                yield{
                    'name': players.css('a.d3-o-player-fullname.nfl-o-cta--link::text').get(),
                    'rush yards': players.css('td:nth-child(2)::text').get(),
                    'att': players.css('td:nth-child(3)::text').get(),
                    'td': players.css('td:nth-child(4)::text').get(),
                    '20+': players.css('td:nth-child(5)::text').get(),
                    '40+':players.css('td:nth-child(6)::text').get(),
                    'lng':players.css('td:nth-child(7)::text').get(),
                    'rush 1st':players.css('td:nth-child(8)::text').get(),
                    'rush 1st %':players.css('td:nth-child(9)::text').get(),
                    'rush fum':players.css('td:nth-child(10)::text').get(),
                }
            #except:
        #return super().parse(response, **kwargs)
        next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


