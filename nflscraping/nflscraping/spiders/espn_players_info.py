from os import link
from types import NoneType
from unicodedata import name
import json
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import os
import logging

class ESPNPlayersInfoSpider(scrapy.Spider):
    name = 'espnplayersinfo'
    #print(os.listdir())
    def __init__(self):
        with open('../../json/espn_players_urls.json', encoding='utf-8') as data_file:
            self.data = json.load(data_file)

    def start_requests(self):
        for i in self.data:
            request = scrapy.Request(self.data[i], callback=self.parse)
            yield request

    def parse(self, response):
        #game = response.meta['game']
        #game['game_detail'] = []
        split = response.url.split("/")
        position = response.xpath('//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div/ul/li[3]/text()').get()
        #for head in response.css('div.ResponsiveWrapper').get():
        if position != 'null':
            yield{
                "id player" : split[7],
                "url" : response.url,
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

# Name of the file where the results will be saved
filename = "../../json/espn_players_info.json"

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
    'FEED URI': '../../json/',
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

#process = CrawlerProcess()
process.crawl(ESPNPlayersInfoSpider)
process.start()