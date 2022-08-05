from unicodedata import name
import scrapy

class ESPNScoresSpider(scrapy.Spider):
    name = 'espnscores'
    start_urls = ['https://www.espn.com/nfl/scoreboard/_/week/1/year/2021/seasontype/2']

    def parse(self, response):

        for scores in response.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between'):
            #try:
                yield{
                    'awayteam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').get(),
                    'hometeam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').extract()[1]
,
                }
            #except:
        #return super().parse(response, **kwargs)
        next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


