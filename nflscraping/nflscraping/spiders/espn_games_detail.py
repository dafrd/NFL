from os import link
from unicodedata import name
import json
import scrapy
import pandas as pd

class ESPNGamesDetailSpider(scrapy.Spider):
    name = 'espngamesdetail'

    def __init__(self):
        with open('espn_scores.json', encoding='utf-8') as data_file:
            self.data = json.load(data_file)

    def start_requests(self):
        for game in self.data:
            request = scrapy.Request(game['boxscore'], callback=self.parse)
            #request.meta['game'] = game['boxscore']
            yield request

    def parse(self, response):
        #game = response.meta['game']
        #game['game_detail'] = []

        split = response.url.split("/")

        away = []
        home = []

        for game in response.css('#gamepackage-box-score'):
            for awayteam in game.css('div.col.column-one.gamepackage-away-wrap'):
                for player in awayteam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        away.append(player.css('td.name > a > span::text').get())
                    away = list(set(away))
            for hometeam in game.css('div.col.column-two.gamepackage-home-wrap'):
                for player in hometeam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        home.append(player.css('td.name > a > span::text').get())
                    home = list(set(home))
        '''
        yield{
            "game_id" : split[7],
            "away roster" : away,
            "home roster" : home,
            }'''

        for player in away:
            #for player in response.css('tr:contains("'+name+'")'):
            #player_name = player.xpath('//span[text()='+player+']/div/div[1]/div/div/table/tbody/tr[1]/td[1]/a/span[1]).get())
            #player_name = player.css('td.name > a > span::text').get()
            #if player_abbr is not None:
            yield{
                    "game_id" : split[7],
                    "team" : response.css('span.team-name::text').get(),
                    "player_name" : response.xpath('//span[text()="'+player+'"]/text()').get(),
                    "player_url" : response.xpath('//span[text()="'+player+'"]/ancestor::a/@href').get(),
                    "pass completion" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="c-att"]/text()').get(),
                    "pass yds" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "pass avg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "pass td" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "pass int" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "sacks" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "qbr" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="qbr"]/text()').get(),
                    "rtg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rtg"]/text()').get(),
                    "rush car" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="car"]/text()').get(),
                    "rush yds" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rush avg" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "rush td" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "rush long" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "receptions" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "rec yds" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rec avg" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),  
                    "rec td" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),  
                    "rec long" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "rec tgs" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tgts"]/text()').get(),
                    "fumbles" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="fum"]/text()').get(),
                    "fumbles lost" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="lost"]/text()').get(),
                    "fumbles rec" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get()          
        }

        for player in home:
            #for player in response.css('tr:contains("'+name+'")'):
            #player_name = player.xpath('//span[text()='+player+']/div/div[1]/div/div/table/tbody/tr[1]/td[1]/a/span[1]).get())
            #player_name = player.css('td.name > a > span::text').get()
            #if player_abbr is not None:
            yield{
                    "game_id" : split[7],
                    "team" : response.css('span.team-name::text').get(),
                    "player_name" : response.xpath('//span[text()="'+player+'"]/text()').get(),
                    "player_url" : response.xpath('//span[text()="'+player+'"]/ancestor::a/@href').get(),
                    "pass completion" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="c-att"]/text()').get(),
                    "pass yds" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "pass avg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "pass td" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "pass int" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "sacks" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "qbr" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="qbr"]/text()').get(),
                    "rtg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rtg"]/text()').get(),
                    "rush car" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="car"]/text()').get(),
                    "rush yds" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rush avg" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "rush td" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "rush long" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "receptions" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "rec yds" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rec avg" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),  
                    "rec td" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),  
                    "rec long" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "rec tgs" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tgts"]/text()').get(),
                    "fumbles" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="fum"]/text()').get(),
                    "fumbles lost" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="lost"]/text()').get(),
                    "fumbles rec" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get()          
        }

            '''
            for game in response.css('#gamepackage-box-score'):
                for awayteam in game.css('div.col.column-one.gamepackage-away-wrap'):
                    for player in awayteam.css('td.name'):
                        player_name = player.css('span.abbr::text').get()
                        if player_name is not None:
                            yield{
                                "game_id" : split[7],
                                "team" : response.css('span.team-name::text').get(),
                                "player_name" : player.css('td.name > a > span::text').get(),
                                "player_url" : player.css('td.name > a::attr(href)').get(),
                                "pass completion" : awayteam.css('td.c-att::text').get(),
                                "pass yds" : awayteam.css('td.yds::text').get(),
                                "pass avg" : awayteam.css('td.avg::text').get(),
                                "pass td" : awayteam.css('td.td::text').get(),
                                "pass int" : awayteam.css('td.int::text').get(),
                                "sacks" : awayteam.css('td.sacks::text').get(),
                                "qbr" : awayteam.css('td.qbr::text').get(),
                                "rtg" : awayteam.css('td.rtg::text').get(),
                                "rush car" : awayteam.css('td.car::text').get(),
                                "rush yds" : awayteam.css('td.yds::text').get(),
                                "rush long" : awayteam.css('td.long::text').get()
                            }
                
            for hometeam in game.css('div.col.column-two.gamepackage-away-wrap'):
                for player in hometeam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        yield{
                            "game_id" : split[7],
                            "team" : response.css('span.team-name::text').extract()[1],
                            "player_name" : player.css('td.name > a > span::text').get(),
                            "player_url" : player.css('td.name > a::attr(href)').get(),
                            "pass completion" : hometeam.css('td.c-att::text').get(),
                            "pass yds" : hometeam.css('td.yds::text').get(),
                            "pass avg" : hometeam.css('td.avg::text').get(),
                            "pass td" : hometeam.css('td.td::text').get(),
                            "pass int" : hometeam.css('td.int::text').get(),
                            "sacks" : hometeam.css('td.sacks::text').get(),
                            "QB rating" : hometeam.css('td.qbr::text').get(),
                            "rtg" : hometeam.css('td.rtg::text').get(),
                            "car" : hometeam.css('td.car::text').get(),
                            "long" : hometeam.css('td.long::text').get()
                        }'''

            