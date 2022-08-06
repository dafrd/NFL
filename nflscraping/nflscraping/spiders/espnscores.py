from unicodedata import name
import scrapy
import json

class ESPNScoresSpider(scrapy.Spider):
    name = 'espnscores'

    urls_year=[]
    for week in range(1,19):
        for year in range(2001,2022,1):
            urls_year.append("https://www.espn.com/nfl/scoreboard/_/week/" + 
            str(week) + 
            "/year/" +
            str(year)+
            "/seasontype/2")

    start_urls=urls_year

    '''
    start_urls = [  'https://www.espn.com/nfl/scoreboard/_/week/1/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/2/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/3/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/4/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/5/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/6/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/7/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/8/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/9/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/10/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/11/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/12/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/13/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/14/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/15/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/16/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/17/year/2021/seasontype/2',
                    'https://www.espn.com/nfl/scoreboard/_/week/18/year/2021/seasontype/2'
                    ]
                    '''

    def parse(self, response):
        '''
        script = [script for script in response.css("script::text") if "window.__renderData" in script.extract()]
        if script:
            script = script[0]
        data = script.extract().split("window.__renderData = ")[-1]
        json_data = json.loads(data[:-1])
        for weeks in json_data["plp"]["plp_products"]:
            for product in weeks["data"]:
                #yield {"productName":product["productName"]} # data from css:  a.shelf-product-name
                yield product
        '''

        for scores in response.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between'):
            #try:
                yield{
                    'week': response.css('div.custom--week.is-active > span.week.week-range::text').get(),
                    'awayteam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').get(),
                    'hometeam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').extract()[1],
                    'awayscore' : scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').get(),
                    'homescore': scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').extract()[1],
                }
            #except:
        #return super().parse(response, **kwargs)
        #next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)


