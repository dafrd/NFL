import scrapy
import json
from scrapy.crawler import CrawlerProcess
import os
import logging


class ESPNScoresSpider(scrapy.Spider):
    name = 'espnscores'

    urls_year=[]
    for week in range(1,19):
        for year in range(2017,2022,1):
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
                idgame = scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get()
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
                    'idgame' : scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get(),
                    'awayteam global record' : scores.css('span.ScoreboardScoreCell__Record::text').get(),
                    'awayteam away record' : scores.css('span.ScoreboardScoreCell__Record::text').extract()[1],
                    'hometeam global record' : scores.xpath('//*[@id="'+idgame+'"]/div[1]/div/div[1]/div/div/ul/li[2]/div[1]/div[2]/span[1]/text()').get(),
                    'hometeam home record' : scores.xpath('//*[@id="'+idgame+'"]/div[1]/div/div[1]/div/div/ul/li[2]/div[1]/div[2]/span[2]/text()').get()
                }
            #except:
        #return super().parse(response, **kwargs)
        #next_page = response.css('a.nfl-o-table-pagination__next').attrib['href']
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)

# Name of the file where the results will be saved
filename = "../../json/espn_scores.json"

# if th file exist, remove this
if filename in os.listdir():
    os.remove(filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.DEBUG,
    #'FEED FORMAT' : ,
    'FEED URI' : '../../json/',
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

# Start the crawling using the spider you defined above
process.crawl(ESPNScoresSpider)
process.start()

