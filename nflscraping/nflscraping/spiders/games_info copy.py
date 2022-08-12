from os import link
from unicodedata import name
import json
import scrapy

class ESPNGamesCastSpider(scrapy.Spider):
    name = 'espngamescast'

    def __init__(self):
        with open('espn_scores_gamescast.json', encoding='utf-8') as data_file:
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

        for game in response.css('#gamepackage-box-score'):
            for awayteam in game.css('div.col.column-one.gamepackage-away-wrap'):
                for player in awayteam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        yield{
                            "game_id" : split[7],
                            "team" : response.css('span.abbrev::text').get(),
                            "player_name" : player.css('td.name > a > span::text').get(),
                            "player_url" : player.css('td.name > a::attr(href)').get(),
                            "pass completion" : awayteam.css('td.c-att::text').get(),
                            "pass yds" : awayteam.css('td.yds::text').get(),
                            "avg" : awayteam.css('td.avg::text').get(),
                            "td" : awayteam.css('td.td::text').get(),
                            "int" : awayteam.css('td.int::text').get(),
                            "sacks" : awayteam.css('td.sacks::text').get(),
                            "qbr" : awayteam.css('td.qbr::text').get(),
                            "rtg" : awayteam.css('td.rtg::text').get(),
                            "car" : awayteam.css('td.car::text').get(),
                            "long" : awayteam.css('td.long::text').get()

                        }
                
            for hometeam in game.css('div.col.column-two.gamepackage-away-wrap'):
                for player in hometeam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        yield{
                            "game_id" : split[7],
                            "team" : response.css('span.abbrev::text').extract()[1],
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
                        }
    
                