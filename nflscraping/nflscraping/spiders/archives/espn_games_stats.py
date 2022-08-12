from os import link
from unicodedata import name
import json
import scrapy
import pandas as pd
import os
from scrapy.crawler import CrawlerProcess
import logging 

class ESPNGamesStatsSpider(scrapy.Spider):
    name = 'espnstats'

    def __init__(self):
        with open('../../json/espn_scores.json', encoding='utf-8') as data_file:
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
        
        awayteam = response.css('span.team-name::text').get()
        hometeam = response.css('span.team-name::text').extract()[1]
        player = 'TEAM'

        '''
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
        '''

        for stats in response.css('div.col.column-one.gamepackage-away-wrap'):
            #for player in response.css('tr:contains("'+name+'")'):
            #player_name = player.xpath('//span[text()='+player+']/div/div[1]/div/div/table/tbody/tr[1]/td[1]/a/span[1]).get())
            #player_name = player.css('td.name > a > span::text').get()
            #if player_abbr is not None:
            yield{
                    "game_id" : split[7],
                    "team" : response.css('span.team-name::text').get(),
                    #"player_name" : response.xpath('//td[text()="'+player+'"]/text()').get(),
                    #"player_url" : response.xpath('//span[text()="'+player+'"]/ancestor::a/@href').get(),
                    "pass completion" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td[text()="'+player+'"]/../../../td[@class="c-att"]/text()').get(),
                    "pass yds" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "pass avg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "pass td" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "pass int" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "sacks" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "qbr" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="qbr"]/text()').get(),
                    "rtg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="rtg"]/text()').get(),
                    "rush car" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="car"]/text()').get(),
                    "rush yds" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rush avg" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "rush td" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "rush long" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "receptions" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "rec yds" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rec avg" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),  
                    "rec td" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),  
                    "rec long" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "rec tgs" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="tgts"]/text()').get(),
                    "fumbles" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="fum"]/text()').get(),
                    "fumbles lost" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="lost"]/text()').get(),
                    "fumbles rec" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "defense tot" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="tot"]/text()').get(),
                    "defense solo" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="solo"]/text()').get(),
                    "defense sacks" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "defense tfl" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="tfl"]/text()').get(),
                    "defense pd" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="pd"]/text()').get(),
                    "defense qb hits" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="qb hts"]/text()').get(),
                    "defense td" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "interceptions" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "interceptions yds" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "interceptions td" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "kicks return no" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "kicks return yds" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "kicks return avg" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "kicks return long" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "kicks return td" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "punt return no" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "punt return yds" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "punt return avg" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "punt return long" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),               
                    "punt return td" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "kicking fg" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="fg"]/text()').get(),
                    "kicking pct" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="pct"]/text()').get(),                
                    "kicking long" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "kicking xp" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="xp"]/text()').get(),
                    "kicking pts" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="pts"]/text()').get(),
                    "punting no" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "punting yds" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "punting avg" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "punting tb" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="tb"]/text()').get(),
                    "punting in 20" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="in 20"]/text()').get(),
                    "punting long" : response.xpath('//*[@id="gamepackage-punting"]/div/div[1]/div/div/table/tbody/tr/td/[text()="'+player+'"]/../../../td[@class="long"]/text()').get()
                }   

        for player in response.css('div.col.column-two.gamepackage-home-wrap'):
            #for player in response.css('tr:contains("'+name+'")'):
            #player_name = player.xpath('//span[text()='+player+']/div/div[1]/div/div/table/tbody/tr[1]/td[1]/a/span[1]).get())
            #player_name = player.css('td.name > a > span::text').get()
            #if player_abbr is not None:
            yield{
                    "game_id" : split[7],
                    "team" : response.css('span.team-name::text').extract()[1],
                    "player_name" : response.xpath('//span[text()="'+player+'"]/text()').get(),
                    "player_url" : response.xpath('//span[text()="'+player+'"]/ancestor::a/@href').get(),
                    "pass completion" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="c-att"]/text()').get(),
                    "pass yds" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "pass avg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "pass td" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "pass int" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "sacks" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "qbr" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="qbr"]/text()').get(),
                    "rtg" : response.xpath('//*[@id="gamepackage-passing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rtg"]/text()').get(),
                    "rush car" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="car"]/text()').get(),
                    "rush yds" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rush avg" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "rush td" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "rush long" : response.xpath('//*[@id="gamepackage-rushing"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "receptions" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "rec yds" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "rec avg" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),  
                    "rec td" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),  
                    "rec long" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "rec tgs" : response.xpath('//*[@id="gamepackage-receiving"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tgts"]/text()').get(),
                    "fumbles" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="fum"]/text()').get(),
                    "fumbles lost" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="lost"]/text()').get(),
                    "fumbles rec" : response.xpath('//*[@id="gamepackage-fumbles"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="rec"]/text()').get(),
                    "defense tot" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tot"]/text()').get(),
                    "defense solo" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="solo"]/text()').get(),
                    "defense sacks" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="sacks"]/text()').get(),
                    "defense tfl" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tfl"]/text()').get(),
                    "defense pd" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="pd"]/text()').get(),
                    "defense qb hits" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="qb hts"]/text()').get(),
                    "defense td" : response.xpath('//*[@id="gamepackage-defensive"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "interceptions" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="int"]/text()').get(),
                    "interceptions yds" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "interceptions td" : response.xpath('//*[@id="gamepackage-interceptions"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "kicks return no" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "kicks return yds" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "kicks return avg" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "kicks return long" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "kicks return td" : response.xpath('//*[@id="gamepackage-kickReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "punt return no" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "punt return yds" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "punt return avg" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "punt return long" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),               
                    "punt return td" : response.xpath('//*[@id="gamepackage-puntReturns"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="td"]/text()').get(),
                    "kicking fg" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="fg"]/text()').get(),
                    "kicking pct" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="pct"]/text()').get(),                
                    "kicking long" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get(),
                    "kicking xp" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="xp"]/text()').get(),
                    "kicking pts" : response.xpath('//*[@id="gamepackage-kicking"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="pts"]/text()').get(),
                    "punting no" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="no"]/text()').get(),
                    "punting yds" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="yds"]/text()').get(),
                    "punting avg" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="avg"]/text()').get(),
                    "punting tb" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="tb"]/text()').get(),
                    "punting in 20" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="in 20"]/text()').get(),
                    "punting long" : response.xpath('//*[@id="gamepackage-punting"]/div/div[2]/div/div/table/tbody/tr/td/a/span[text()="'+player+'"]/../../../td[@class="long"]/text()').get()       
    
        }

# Name of the file where the results will be saved
filename = "../../json/espn_games_stats.json"

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
    'FEED URI': '../../json/',
    "FEEDS": {
        filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

# Start the crawling using the spider you defined above
process.crawl(ESPNGamesStatsSpider)
process.start()