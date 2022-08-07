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
        for game in response.css('#gamepackage-box-score'):
            
            yield{
                "away" : response.css('span.abbrev::text').get(),
                "qb": game.css('span.abbr::text').get()
            }
    
                