# -*- coding: iso-8859-1 -*-
from bs4 import NavigableString,BeautifulSoup
import requests
import time
import os
import datetime

############
now = datetime.datetime.now()
dateTimeStr = now.strftime("%Y-%m-%d_%H-%M")
currentDir = os.getcwd()
#outputPath = currentDir+"\output_"+dateTimeStr
outputPath = "output_"+dateTimeStr
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
    pagesPerLink = '20'
############

categoryUrlDict = dict()

#########################################
def getCategory(categorySoup):
    # this function will get the category name from bea crumbs located at
    # the top of teh screen
    try:
        crumbDiv = categorySoup.find('div',{'class':'beacrumb'})
        acrumbs = crumbDiv.findAll('a')
        catPreProcessing = acrumbs[len(acrumbs)-1].contents
        catPostProcessing = catPreProcessing[0].encode('utf-8').strip()
        return catPostProcessing
    except:
        return "NotValid"
##########################################

def urlGetbs4Obj (url):
    # get a url and return a beautiful soup object
    #html = urllib2.urlopen(url).read()
    try:
        r = requests.get(url)
    except r.exceptions.ConnectionError:
        plog( f_log_h, 'E', "Network problem")
    except r.exceptions.HTTPError:
        plog(f_log_h,'E',"An HTTP error occurred")
    except r.exceptions.Timeout:
        plog(f_log_h,'E',"The request timed out")
    else:
        html = r.content
        soup = BeautifulSoup(html)
        return soup
    
###########################################
def createCategoryDir(category):

    count,url = categoryUrlDict[category]
    path = outputPath + "\\" + str(count)
    if not os.path.exists(path):
        os.makedirs(path)
    return createSingleInputFile(path,category)

###########################################
def createSingleInputFile(path,category):
    fName = path + "\inputLUrl.csv" 
    fh = open(fName,'w')
    count,url = categoryUrlDict[category]
    fh.write(url)
    fh.close()
    return "pid7144001.py " + path + " " + pagesPerLink + " " + fName + "\n"

############################################   
inputFile = "inputLinks.csv"
batchFile = "run.bat"
fh=open(inputFile)
f_batch_h = open(batchFile,'w')
counter = 1
for line in fh:
    if not line.startswith('#'):
        url = line.strip()
        categorySoup = urlGetbs4Obj(url)
        category = getCategory(categorySoup)
        if category == 'NotValid' : category = category + str(counter)
            
        categoryUrlDict[category] = counter,url
        counter += 1
        lineToBatchFile = createCategoryDir(category)
        print lineToBatchFile
        f_batch_h.write(lineToBatchFile)  
fh.close()
f_batch_h.close()

##################### Run batch file
os.system("run.bat")