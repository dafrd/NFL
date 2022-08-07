from os import link
from unicodedata import name
import json
import scrapy

class ESPNGamesDetailSpider(scrapy.Spider):
    name = 'espngamesdetail'

    def __init__(self):
        with open('espnscores.json', encoding='utf-8') as data_file:
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
                            #"CMP" : hometeam.css('td.c-att::text').get()
                        }
                
            for hometeam in game.css('div.col.column-two.gamepackage-away-wrap'):
                for player in awayteam.css('td.name'):
                    player_name = player.css('span.abbr::text').get()
                    if player_name is not None:
                        yield{
                            "game_id" : split[7],
                            "team" : response.css('span.abbrev::text').extract()[1],
                            "player_name" : player.css('td.name > a > span::text').get(),
                            "player_url" : player.css('td.name > a::attr(href)').get(),
                            #"CMP" : awayteam.css('td.c-att::text').get()
                        }
    
                