# -*- coding: iso-8859-1 -*-
from bs4 import BeautifulSoup
import requests
import time
import os
import datetime
import sys
'''
##### EMAIL Stuff
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
myAddress = 'sivbfreelancer@gmail.com'
toAddress = 'jorgemartinezfdez@outlook.es'
msg = MIMEText("New run has ended")
msg['Subject'] = 'Run details'
msg['From'] = myAddress
msg['To'] = toAddress
s = smtplib.SMTP('localhost')
s.sendmail(myAddress, [toAddress], msg.as_string())
s.quit()
'''
############
now = datetime.datetime.now()
dateTimeStr = now.strftime("%Y-%m-%d_%H-%M")
currentDir = os.getcwd()
#outputPath = currentDir+"\output_"+dateTimeStr
outputPath = "output_"+dateTimeStr
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

### get variables from CFG file
cfgFile = os.path.dirname(os.path.abspath(__file__))+"/"+'pid7144001.cfg.txt'
f_cfg_h = open(cfgFile)
for line in f_cfg_h:
    if line.startswith('pagesPerLink='):
        pagesPerLink = line[line.index('=')+1:]
        pagesPerLink = pagesPerLink.strip()
    elif line.startswith('inputFile='):
        inputFile = line[line.index('=')+1:]
        inputFile = inputFile.strip()
    elif line.startswith('batchFile='):
        batchFile = line[line.index('=')+1:]
        batchFile = batchFile.strip()
    else:
        print "Cfg Variable unknown - exiting.."
        time.sleep(5)
        exit(1)
          
f_cfg_h.close()

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
        soup = BeautifulSoup(html, "html.parser")
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
    return sys.executable + " pid7144001.py " + path + " " + pagesPerLink + " " + fName + "\n"

############################################   
fh=open(os.path.dirname(os.path.abspath(__file__))+"/"+inputFile)
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
os.system(batchFile)

