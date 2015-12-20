import requests
from bs4 import NavigableString,BeautifulSoup
from general import *

def getAllPages(srchUrl):
    pagina = 0
    links = []
    while pagina < maxPagesPerSearchUrl:
        pagina+=1
        nextUrl = srchUrl+"&pagina="+str(pagina)
        links.append(nextUrl)
    
    return links
    
    
def getLinksFromSearchUrl(srchUrl):
    
    #baseUrl = urlGetBaseUrl(srchUrl)
    pagina = 1
    links = []
    nextUrl = srchUrl+"&pagina="+str(pagina)
    r= requests.get(nextUrl)
    soup = BeautifulSoup(r.content)
    while checkNextPageExists(soup):
        print "Page #: ",pagina
        if pagina > 1 :break
        links = links + getAllLinksFromPage(soup,baseUrl)
        pagina+=1
        nextUrl = srchUrl+"&pagina="+str(pagina)
        r= requests.get(nextUrl)
        soup = BeautifulSoup(r.content)
        
    return links
        
def checkNextPageExists(soup):
    tableTag = soup.find_all('table')
    if len(tableTag) > 0 :
        tdTags = tableTag[0].find_all('td')
        lastTd = tdTags[-1]
        if lastTd.div.a.text == 'Siguiente':
            return 1
    else:
        return 0
    
def getAllLinksFromPage(soup,baseUrl):
    links = []
    x1Tags = soup.find_all('div',{'class':'x1'})
    for x1 in x1Tags:
        aTag = x1.find_all('a',{'class':'cti'})
        links.append(baseUrl+aTag[0]['href'])
    
    return links

    
