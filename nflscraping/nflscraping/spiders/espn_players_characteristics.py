from os import link
from unicodedata import name
import json
import scrapy
import pandas as pd

class ESPNPlayersCharacteristicsSpider(scrapy.Spider):
    name = 'espnplayerscharacteristics'

    def __init__(self):
        with open('../json/espn_rosters.json', encoding='utf-8') as data_file:
            self.data = json.load(data_file)

    def start_requests(self):
        urls = []
        for url in self.data:
            #request = scrapy.Request(players['player_url'], callback=self.parse)
            #request.meta['game'] = game['boxscore']
            #yield request
            urls.append(url['player_url'])
        urls = list(set(urls))
        for player in urls:
            request = scrapy.Request(player, callback=self.parse)
            yield request

    def parse(self, response):
        #game = response.meta['game']
        #game['game_detail'] = []
        split = response.url.split("/")
        for head in response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div').get():
            if response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[5]/div[2]/div/span/text()').get() is not None:
                yield{
                    "id player" : split[7],
                    "first name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[1]/text()').get(),
                    "last name" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/h1/span[2]/text()').get(),
                    "actual team" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a/text()').get(),
                    "status" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[5]/div[2]/div/span/text()').get(),
                    "team url" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[1]/a/@href').get(),
                    "#" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[2]/text()').get(),
                    "position" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[3]/text()').get(),
                    "HT/WT" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[1]/div[2]/div/text()').get(),
                    "Birthdate" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[2]/div[2]/div/text()').get(),
                    "College" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[3]/div[2]/div/a/text()').get(),
                    "Draft" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[2]/div/ul/li[4]/div[2]/div/text()').get(),
                    "Fantasy Draft Rank" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[2]/div[2]/section/div/div[1]/div[1]/div[2]/span/text()').get(),
                    "Fantasy '%' rostered" : response.xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[2]/div[2]/section/div/div[1]/div[2]/div[2]/span/text()').get()
                }