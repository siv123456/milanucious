from urlparse import urlparse
import requests
from bs4 import NavigableString,BeautifulSoup

maxPagesPerSearchUrl = 1


def getCategory(srchUrl):
    
    r = requests.get(srchUrl)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.content)
    else:
        return "problem with categoty"
    if getUrlType(srchUrl) == 'type2':
        bSub2Tag = soup.find_all('b',{'class':'sub2'})
        text1 = bSub2Tag[0].text
        bSub3Tag = soup.find_all('b',{'class':'sub3'})
        text2 = bSub3Tag[0].text
        
        category = text1 + " " + text2
        
    else:
        pass
    
    return category

def getUrlType(srchUrl):
    o = urlparse(srchUrl)
    if o.path.find('.htm')>0:
        return 'type2'
    else:
        return 'type1'

def urlGetBaseUrl(srchUrl):
    # there are two types of search url:
    # 1. 'http://www.milanuncios.com/informaticos/?demanda=s&pagina=2'
    # 2. 'http://www.milanuncios.com/anuncios/clases-particulares.htm?demanda=s'
    # for the first type relative urls from each page should concat with the beggining of teh url till the "?"
    # for the ssecond type basic url would be the name of the site http://www.milanuncios.com
    # from urlParser : scheme://netloc/path;parameters?query#fragment
    o = urlparse(srchUrl)
    #print o.scheme
    #print o.netloc
    #print o.path
    #print o.parameters
    #print o.query
    #print o.fragment
    if o.path.find('.htm')>0:
        print 'type2'
        baseUrl = o.scheme + '://' + o.netloc + o.path[:o.path.find('/',1)]
        return baseUrl
    else:
        print 'type1'
        baseUrl = o.scheme + '://' + o.netloc + o.path
        return baseUrl

       