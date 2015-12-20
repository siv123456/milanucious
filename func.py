# -*- coding: iso-8859-1 -*-
###########################################
## variable definitions and imports
###########################################
import sys
import time
import requests
import os
from bs4 import BeautifulSoup
from ghost import Ghost
import datetime

if len(sys.argv) < 3:
    sys.stderr.write("Usage:" + sys.argv[0] + " outputPath pagesToScrape inputFile" )
    sys.exit(1)
else:
    outputPath = sys.argv[1]
    pagesToScrapePerCategory = sys.argv[2]
    inputFile = sys.argv[3]
    

baseUrl = 'http://www.milanuncios.com'
#now = datetime.datetime.now()
#dateTimeStr = now.strftime("%Y-%m-%d %H-%M")
#currentDir = os.getcwd()
#outputPath = currentDir+"\output_"+dateTimeStr
if not os.path.exists(outputPath): os.makedirs(outputPath)
log = outputPath+"\log.txt"
f_log_h = open(log,'w')

print "Input file with links: "+inputFile
print "Number of pages to scrape per link: "+pagesToScrapePerCategory



######## FUNCTIONS #######################
def getCategoryData(categoryUrl,categorySoup,outputPath):
    
    onePageTempList = []
    page = 1
    # get category name
    category = getCategory(categorySoup)
    print "CATEGORY: ", category
    # create output file
    outputFile = outputPath+"/"+category+".csv"
    f_out_h = open(outputFile,'w')
    f_out_h.write('Category,Description,Url,Name,Phone1,Phone2,contactDataUrl\n')
    #f_out_h.write('PageURL\n')
    f_out_h.close()
    ###############################
    ### get 1 page data:
    # get X4 - description1 data
    # get X7 - url + description2
    # get X5 - url for phones data
    # get phones
    # append 1 page data to file
    ################################
    while True:
        print "PAGE: ",page
        pageUrl = categoryUrl+"&pagina="+str(page)
        pageSoup = urlGetbs4Obj(pageUrl)
        #######################################
        ### code for getting data from one page
        #######################################
        onePageTempList = getOnePageData(categoryUrl,category,pageSoup)
        if len(onePageTempList):
            print "Append data from page #",page, " to output file"
            #append page data to output file
            f_out_h = open(outputFile,'a')
            for item in onePageTempList:
                f_out_h.write(item)
            f_out_h.close()
        else:
            return
        ##########################################################################
        ### checking if there is another page to scrape (i.e is there a nextPage)
        ##########################################################################
        if nextsPage(pageSoup) and page < int(pagesToScrapePerCategory) :
            page +=1
        else: # there is no next page or we already got 25 pages
            return
            

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
def getOnePageData(categoryUrl,category,onePageSoup):
    onePageList = []
    x1Divs = onePageSoup.findAll("div",{"class":"x1"})
    # this check makes sure we still have data on the page we're scraping
    if not len(x1Divs) :
        return onePageList
    for eachX1Div in x1Divs :
        x4Div = eachX1Div.find('div',{'class':'x4'})
        x5Div = eachX1Div.find('div',{'class':'x5'})
        x7Div = eachX1Div.find('div',{'class':'x7'})
        # X4 data
        desc1 = getX4divData(x4Div)
        # X5 data
        PhonesUrl = getX5divData(x5Div)
        phones = getPhones(PhonesUrl)
        # X9 data
        desc2Href,desc2Data = getX7divData(categoryUrl,x7Div)
        oneAdDataStr = category+','+desc1+','+desc2Href+','+desc2Data + ',' + phones + ',' + PhonesUrl + "\n"
        onePageList.append(oneAdDataStr)
        
    return onePageList
#####################################
def getX4divData(div):
    st= div.contents
    return st[0].encode('utf-8').replace(',',' ')
    
####################################
def getX5divData(div):
    wantedId = div.string
    wantedId =  str(wantedId).replace("r","")
    newUrl = baseUrl + '/datos-contacto/?id=' + wantedId
    newUrl = newUrl.strip()
    return newUrl

####################################
def getPhones(url):
        
    gh=Ghost()

    page, page_name = gh.create_page(download_images=False,prevent_download=["css",'js'] )
    try:
        page_resource = page.open(url, wait_onload_event=True)
    except:
        plog(f_log_h,"E","Failed waiting to onload event - " + url)
        return "no phone,no phone"
    try:
        page.wait_for_selector("div.telefonos")
    except:
        errorString = "No telefonos DIV encountered - "+ url 
        plog(f_log_h,"E",errorString)
        return "no phone,no phone"
    p = page.evaluate('''
            phones = []
            var p = document.getElementsByClassName('telefonos');
            for (i = 0; i<p.length ; i++) {
            phones[i] = p[i].outerText
            }
            phones;
        ''')
    s = ','.join(element.encode('utf-8').strip() for element in p)
    if len(p) == 1 :
        s = s+','+" "
    gh.remove_page(page)
    return s        
    
    
####################################
def getX7divData(urlPre,div):
    try:
        relevantAtag = div.find('a',{'class':'cti'})
        try:
            href = relevantAtag['href'].encode('utf-8').strip()
            url = urlPre+href
        except:
            
            href = 'no url'
            url = href
            print "href problem: " ,relevantAtag
            exit(1)
        try:
            descPre = relevantAtag.contents
            descPost = descPre[-1].encode('utf-8').strip().replace(',',' ')
        except:
            descPost = 'no description'
            print descPost," " ,relevantAtag
            exit(2)
    except:
        #print urlPre
        href="no url"
        url = href
        descPost = "no description"
    
    return url,descPost

#####################################
def nextsPage(pageSoup):
    # look for "Siguiente" in teh bottome of teh page
    atags = pageSoup.findAll('a')
    for a in atags:
        string  = a.string
        if string=='Siguiente':
            return True
    
    return False

#####################################

def obtainUrlsToScrape(fh):
    # parsing the inputLinks file to get all
    # category links to scrape
    # if there is a "#" at the beggining of the line
    # the link will be ignored
    tempList = []
    for line in fh:
        if not line.startswith("#"):
            url = line.strip()
            tempList.append(url)
        
    return tempList
##########################################

def urlGetbs4Obj (url):
    # get a url and return a beautiful soup object
    #html = urllib2.urlopen(url).read()
    try:
        r = requests.get(url)
    except ConnectionError:
        plog( f_log_h, 'E', "Network problem")
    except HTTPError:
        plog(f_log_h,'E',"An HTTP error occurred")
    except Timeout:
        plog(f_log_h,'E',"The request timed out")
    else:
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        return soup

###########################################
def plog(fh,commentType,string):
    # fh : file handler of teh log file 
    # commentType: E or W or I
    # string : what to print to log file

    lineToPrint = "-"+commentType+"- "+string+"\n"
    try:
        fh.write(lineToPrint)
    except:
        print "-E- Can't write to log file"
    
##############################################
