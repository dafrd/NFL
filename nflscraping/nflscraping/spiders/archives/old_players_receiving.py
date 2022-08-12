from unicodedata import name
import scrapy

class Playersreceiving2021Spider(scrapy.Spider):
    name = 'playersreceiving2021'
    start_urls = ['https://www.nfl.com/stats/player-stats/category/receiving/2021/reg/all/receivingreceptions/desc']

    def parse(self, response):

        for players in response.css('tbody > tr'):
            #try:
                yield{
                    'name': players.css('a.d3-o-player-fullname.nfl-o-cta--link::text').get(),
                    'rec': players.css('td:nth-child(2)::text').get(),
                    'yards': players.css('td:nth-child(3)::text').get(),
                    'td': players.css('td:nth-child(4)::text').get(),
                    '20+': players.css('td:nth-child(5)::text').get(),
                    '40+':players.css('td:nth-child(6)::text').get(),
                    'lng':players.css('td:nth-child(7)::text').get(),
                    'rec 1st':players.css('td:nth-child(8)::text').get(),
                    '1st %':players.css('td:nth-child(9)::text').get(),
                    'rec fum':players.css('td:nth-child(10)::text').get(),
                    'rec yac/r':players.css('td:nth-child(11)::text').get(),
                    'tgts':players.css('td:nth-child(12)::text').get(),
                }
            #except:
        #return super().parse(response, **kwargs)
        next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


