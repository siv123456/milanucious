# -*- coding: utf-8 -*-
from getPageInfo import getPageInfo
from getPageUrlList import getAllPages
from general import *

searchUrlList = [
    'http://www.milanuncios.com/anuncios/clases-particulares.htm?demanda=s',
    'http://www.milanuncios.com/informaticos/?demanda=s'
]
pageLinks = []
extractedInfo = [] # list of tuples (category,desc,name,phone1.phone2,contactDataUrl)
strToFile = ''


for srchUrl in searchUrlList:
    print srchUrl
    category = getCategory(srchUrl)
    pageLinks = getAllPages(srchUrl) # now i have all pages i need 
    for eachPage in pageLinks:
        extractedInfo = getPageInfo(eachPage)
    
    
    
    
    
    '''
    for eachLink in urlList:
        #eachLink = eachLink.replace('com//','com/')
        print eachLink
        #strToFile = strToFile + getAdInfo(eachLink) + "\n"
    
    print strToFile
    '''