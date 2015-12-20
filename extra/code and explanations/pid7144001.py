# -*- coding: utf-8 -*-
from func import *


### update urlsToScrapeDict with all urls to scrape and their category
# input file containing all the links is inputLinks.csv
urlsToScrapeDict= dict()
finh = open(inputFile)
urlsToScrapeDict = obtainUrlsToScrape(finh)
finh.close()

###### Main Loop
mainBeginTime = datetime.datetime.now()
for categoryUrl in urlsToScrapeDict:
    plog(f_log_h,'I',"Scraping: " + categoryUrl + "\n")
    categoryBegin = datetime.datetime.now()
    # create category soup
    categorySoup = urlGetbs4Obj(categoryUrl)
    #### get category data ()
    getCategoryData(categoryUrl,categorySoup,outputPath)
    # write runtime data for the category in log file
    categoryEnd = datetime.datetime.now()   
    categoryDiff =  categoryEnd - categoryBegin  
    plog(f_log_h,'I',"CATEGORY TIME: " + str(categoryDiff.total_seconds())+ "\n")

mainEndTime =  datetime.datetime.now()
mainDiff = mainEndTime - mainBeginTime
plog(f_log_h,'I',"MAIN TIME: "+ str(mainDiff.total_seconds()) + "\n")
f_log_h.close()
