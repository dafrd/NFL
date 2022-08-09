#from os import link
#from unicodedata import name
import scrapy
import json
#from scrapy.linkextractors import LinkExtractor

class ESPNScoresSpider(scrapy.Spider):
    name = 'espnscores'

    urls_year=[]
    for week in range(1,19):
        for year in range(2012,2022,1):
            urls_year.append("https://www.espn.com/nfl/scoreboard/_/week/" + 
            str(week) + 
            "/year/" +
            str(year)+
            "/seasontype/2")

    start_urls=urls_year

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
        split = response.url.split("/")
        #print(split)

        for scores in response.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between'):
            #try:
            
                yield{
                    #'week': response.css('div.custom--week.is-active > span.week.week-range::text').get(),
                    'season' : split[9],
                    'week' : split[7],
                    'awayteam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').get(),
                    'hometeam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').extract()[1],
                    'awayscore' : scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').get(),
                    'homescore': scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').extract()[1],
                    'gamecast' : str('https://espn.com')+scores.css('a.AnchorLink.Button.Button--sm.Button--anchorLink.Button--alt.mb4.w-100.mr2::attr(href)').extract()[0],
                    'boxscore' : str('https://espn.com')+scores.css('a.AnchorLink.Button.Button--sm.Button--anchorLink.Button--alt.mb4.w-100.mr2::attr(href)').extract()[1],
                    'idgame' : scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get()
                }
            #except:
        #return super().parse(response, **kwargs)
        #next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)


