# 3. Start by writing code in the script to:
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

# 4. Create a first spider called imdb_spider with:

class NlfSpiderProFoot(scrapy.Spider):
    # Name of your spider
    name = "nlf_scrap_ProFoot"

    # Url to start your spider from 

    urls_year=[]
    for an in range(2001,2022,1):
        for week in range(1,19):
            urls_year.append("https://www.pro-football-reference.com/years/" + 
            str(an) + 
            "/week_" +
            str(week)+
            ".htm")

    # Starting URL
    start_urls =urls_year
    
    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"

    def parse(self, response):
       
        # raccourci
        match = response.xpath('//*[@id="content"]/div[4]')

        # nb_week= response.xpath('//*[@id="div_week_games"]/div/div')
        
        # number matchs / week
        nb_match = len(response.xpath('//*[@id="content"]/div[4]/div'))                       
        
        for i in range(nb_match):
            i = i + 1
            # print(i)
            yield {
                'week' : response.xpath(f'//*[@id="content"]/div[3]/h2/text()').get(),
                'date' : match.xpath(f'div[{i}]/table[1]/tbody/tr[1]/td/text()').get(),                 
                'team1' : match.xpath(f'div[{i}]/table[1]/tbody/tr[2]/td[1]/a/text()').get(),
                'team2' : match.xpath(f'div[{i}]/table[1]/tbody/tr[3]/td[1]/a/text()').get(),
                'score1' : match.xpath(f'div[{i}]//table[1]/tbody/tr[2]/td[2]/text()').get(),
                'score2' : match.xpath(f'div[{i}]/table[1]/tbody/tr[3]/td[2]/text()').get(),
            
            }    
    
# Name of the file where the results will be saved
filename = "ProFoot_nlf.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
print(os.listdir())
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.ERROR,
    "FEEDS": {
        'src/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(NlfSpiderProFoot)
process.start()

