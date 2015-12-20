import requests
from bs4 import NavigableString,BeautifulSoup
import re

def getPageInfo(pageUrl):
    tempList = []
    category = ''
    ref = ''
    desc = ''
    name = ''
    p1 = ''
    p2 = ''
    contactDataUrl = ''
    
    r = requests.get(pageUrl)
    if r.status_code == 200 : soup = BeautifulSoup(r.content)
    else: return []
    
    adTags = soup.find_all('div',{'class':'x1'})
    if len(adTags) > 0:
        for x1 in adTags:
            category,desc,name,phone1,phone2,contactDataUrl = getAdInfo(x1)
            #print category
            print name
    
    return tempList

def getAdInfo(x1):
    category = ''
    ref = ''
    desc = ''
    name = ''
    p1 = ''
    p2 = ''
    contactDataUrl = ''
    
    # category
    category = getCategory(x1)
    # ref
    ref = getRef(x1)
    # name/title
    name = getName(x1)
    # desc
    desc = getDescription(x1)
    # phones
    p1,p2 = getPhoneByRequest(ref)
    #contactDataUrl
    contactDataUrl = getRefUrl(ref)
    
    return category,desc,name,p1,p2,contactDataUrl
    #return ','.join([category,desc,name,p1,p2,contactDataUrl])

def getCategory(x1):
    catTag = x1.find_all('div',{'class':'x4'})
    if len(catTag) > 0:
        text = catTag[0].text
        enPlace = text.find('en')
        if enPlace > 0:
            category = text[:enPlace]
        else:
            category = text
    else:
        category = 'no category'
        
    return category
    
def getRef(x1):
    refTag = x1.find_all('div',{'class':'x5'})
    if len(refTag) > 0:
        return refTag[0].text
    else:
        return 'no ref'

def getName(x1):
    name = 'no name'
    bSub2Tags = x1.find_all('b',{'class':'sub2'})
    bSub3Tags = x1.find_all('b',{'class':'sub3'})
    if len(bSub2Tags)>0:
        name = bSub2Tags[0].text + " " +  bSub3Tags[0].text
    else:
        x7Tags = x1.find_all('div',{'class':'x7'})
        name = x7Tags[0].a.text
        
    return name
    '''
    nameTag = x1.find_all('div',{'class':'pagAnuTituloBox'})
    if len(nameTag) > 0:
        return nameTag[0].a.text.encode('utf-8')
    else:
        return 'no name'
    '''
    
def getDescription(x1):
    desc = 'no description'
    x7 = x1.find_all('div',{'class':'x7'})
    x9 = x1.find_all('div',{'class':'x9'})
    if len(x7) > 0:
        descTag = x7[0].find_all('div',{'class':'tx'})
        desc = descTag[0].text
    elif len(x9) > 0:
        descTag = x9[0].find_all('div',{'class':'tx'})
        desc = descTag[0].text
    
    return desc
    '''
    descTag = soup.find_all('div',{'class':'pagAnuCuerpoAnu'})
    if len(descTag) > 0:
        return descTag[0].text.strip().replace(',','-').encode('utf-8')
    else:
        return 'no description'
    '''
def getRefUrl(ref):
    refUrl = 'http://www.milanuncios.com/datos-contacto/?id='+ref
    return refUrl.encode('utf-8')
    
    
def getPhoneByRequest(ref):
    phone1 = 'no phone'
    phone2 = 'no phone'
    refUrl = getRefUrl(ref)
    r=requests.get(refUrl)
    
    soup = BeautifulSoup(r.content)
    scr = soup.find_all('script')
    if len(scr) == 3:
        phone1 = decodeSoupAndReturnPhone(scr[2]).encode('utf-8')
    if len(scr) == 4:
        phone1 = decodeSoupAndReturnPhone(scr[2]).encode('utf-8')
        phone2 = decodeSoupAndReturnPhone(scr[3]).encode('utf-8')
    
    return phone1,phone2

def decodeSoupAndReturnPhone(soupElem):
    escapedStr = soupElem.text.replace('eval(unescape("document.write(\'','').replace('\')"))','')
    unescapedStr = re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), escapedStr)
    soupAfterDecode = BeautifulSoup(unescapedStr)
    return soupAfterDecode.find('img').text
    