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
        
        
            yield{
                "game_id" : split[7],
                "away roster" : away,
                "home roster" : home,
                }

            for name in away:
                for player in response.css('tr:contains("'+name+'")'):
                    player_abbr = player.css('span.abbr::text').get()
                    player_name = player.css('td.name > a > span::text').get()
                    if player_abbr is not None:
                        yield{
                                "game_id" : split[7],
                                "team" : response.css('span.team-name::text').get(),
                                "player_name" : player.css('td.name > a > span::text').get(),
                                "player_url" : player.css('td.name > a::attr(href)').get(),
                                "pass completion" : player.css('td.c-att::text').get(),
                                #"pass yds" : player.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td[3]/text()').get(),
                                "pass td" : player.css('td.td::text').get(),
                                "pass int" : player.css('td.int::text').get(),
                                "sacks" : player.css('td.sacks::text').get(),
                                "qbr" : player.css('td.qbr::text').get(),
                                "rtg" : player.css('td.rtg::text').get(),
                                "rush car" : player.css('td.car::text').get(),
                                #"rush td" : awayteam.css('td.td::text').get(),
                                #"rush yds" : awayteam.css('td.yds::text').get(),
                                #"rush long" : player.css('td.long::text').get(),
                                #"rush avg" : player.css('td.avg::text').get(),
                                "receptions" : player.css('td.rec::text').get(),
                                #"rec yds" : player.css('td.yds::text').get(),
                                #"rec avg" : player.css('td.avg::text').get(),  
                                #"rec td" : awayteam.css('td.yds::text').get(),  
                                #"rec long" : player.css('td.long::text').get(),
                                "rec tgs" : player.css('td.tgts::text').get(),
                                "fumble" : player.css('td.fum::text').get(),
                                "lost" : player.css('td.lost::text').get(),
                                #"fumbles rec" : pl          
                    }
        
        for name in home:
            for player in response.css('tr:contains("'+name+'")'):
                player_abbr = player.css('span.abbr::text').get()
                player_name = player.css('td.name > a > span::text').get()
                if player_abbr is not None:
                    yield{
                                "game_id" : split[7],
                                "team" : response.css('span.team-name::text').extract()[1],
                                "player_name" : player.css('td.name > a > span::text').get(),
                                "player_url" : player.css('td.name > a::attr(href)').get(),
                                "pass completion" : player.css('td.c-att::text').get(),
                                #"pass yds" : player.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td[3]/text()').get(),
                                "pass td" : player.css('td.td::text').get(),
                                "pass int" : player.css('td.int::text').get(),
                                "sacks" : player.css('td.sacks::text').get(),
                                "qbr" : player.css('td.qbr::text').get(),
                                "rtg" : player.css('td.rtg::text').get(),
                                "rush car" : player.css('td.car::text').get(),
                                #"rush td" : awayteam.css('td.td::text').get(),
                                #"rush yds" : awayteam.css('td.yds::text').get(),
                                #"rush long" : player.css('td.long::text').get(),
                                #"rush avg" : player.css('td.avg::text').get(),
                                "receptions" : player.css('td.rec::text').get(),
                                #"rec yds" : player.css('td.yds::text').get(),
                                #"rec avg" : player.css('td.avg::text').get(),  
                                #"rec td" : awayteam.css('td.yds::text').get(),  
                                #"rec long" : player.css('td.long::text').get(),
                                "rec tgs" : player.css('td.tgts::text').get(),
                                "fumble" : player.css('td.fum::text').get(),
                                "lost" : player.css('td.lost::text').get(),
                                #"fumbles rec" : pl          
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

            