import re
import requests
from bs4 import BeautifulSoup
from time import sleep

global preUrl


def getCategoryData(categoryUrl, fileName):
    global preUrl
    preUrl = categoryUrl

    page = 1
    r = requests.get(categoryUrl + '?pagina=' + str(page))
    if not r.status_code == 200:
        print "-E- problem with category url request"
    else:
        #totalNumOfRecords = getTotalNumOfRecords(r.content)  # get maximum nubmer of records for the category
        while True:
            html = r.content
            pageData = getPageData(html, page)
            if len(pageData) == 0:
                break
            writePageDataToFile(fileName, pageData)
            # first check : if there is no nextPage button ,no use for going to the next page
            if not findNextPageBtn(html):
                break
            page += 1
            if page > 50:
                break
            r = requests.get(categoryUrl + '?pagina=' + str(page))
            if not r.status_code == 200:
                print "-E- problem with category url request"
                break
        #return pageList


def getPageData(html, pageNum):
    pageData = ''
    s = BeautifulSoup(html)
    adDivs = s.find_all('div', {'class': 'x1'})
    for adDiv in adDivs:
        pageData += getAdInfo(adDiv)
    return pageData


def getAdInfo(adDiv):
    global preUrl
    adUrl = ''
    x5 = adDiv.find('div', {'class': 'x5'})
    adID = x5.text.strip()
    #if adID.find('122') == -1 and adID.find('014') == -1:
    #    return '', ('', '')
    phones = getPhonePerAd(adID)
    x7 = adDiv.find('div', {'class': 'x7'})
    if x7:
        adUrl = x7.a['href']
    else:
        x9 = adDiv.find('div', {'class': 'x9'})
        if x9:
            adUrl = x9.a['href']
        else:
            print "-E- Couldn't get ad url"

    if adUrl.find('http') == -1:
        adUrl = preUrl + adUrl

    return phones + ',' + adUrl + '\n'


def getPhonePerAd(adID):

    contactUrl = 'http://www.milanuncios.com/datos-contacto/?id='
    refUrl = contactUrl + adID
    p1, p2 = getPhoneByRequest(refUrl)
    return p1 + ',' + p2


def getPhoneByRequest(refUrl):

    phone1 = 'no phone'
    phone2 = 'no phone'
    r = requests.get(refUrl)
    if not r.status_code == 200:
        print "-E- problem with phones page"
        return phone1, phone2

    soup = BeautifulSoup(r.content)
    scr = soup.find_all('script')
    if len(scr) == 3:
        phone1 = decodeSoupAndReturnPhone(scr[2]).encode('utf-8')
    if len(scr) == 4:
        phone1 = decodeSoupAndReturnPhone(scr[2]).encode('utf-8')
        phone2 = decodeSoupAndReturnPhone(scr[3]).encode('utf-8')

    if phone1 == 'no phone' and phone2 == 'no phone': sleep(20)
    return phone1, phone2


def decodeSoupAndReturnPhone(soupElem):
    escapedStr = soupElem.text.replace('eval(unescape("document.write(\'', '').replace('\')"))','')
    unescapedStr = re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), escapedStr)
    soupAfterDecode = BeautifulSoup(unescapedStr)
    return soupAfterDecode.div.text


def findNextPageBtn(html):

    btnExist = False
    p = re.compile(r'Siguiente</a>')
    m = p.search(html)
    if m:
        btnExist = True

    return btnExist


def getTotalNumOfRecords(html):
    p = re.compile(r'Encontrados\s*<strong>.*</strong>\s*anuncios\s*en')
    m = p.search(html)
    if m:
        l = m.group()
        pNum = re.compile('\d+.*\d+')
        rawStrNum = pNum.findall(l)[0]
        return int(rawStrNum.replace('.', ''))
    else:
        return "no match"


def writePageDataToFile(fileName, pageStr):
    f = fileName + '.csv'
    fh = open(f, 'a')
    fh.write(pageStr)
    fh.close()

