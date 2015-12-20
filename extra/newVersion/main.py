# -*- coding: utf-8 -*-
from category import getCategoryData
import datetime


categoryUrlList = [('denstistas', 'http://www.milanuncios.com/dentistas/'),
                   ('fotografos', 'http://www.milanuncios.com/fotografos/')]

for srchInfo in categoryUrlList:
    catStr = ''
    fileName, srchUrl = srchInfo
    print srchUrl
    print datetime.datetime.now().time().isoformat()
    fileName += " " + datetime.datetime.now().date().isoformat() + " " + \
                datetime.datetime.now().hour + datetime.datetime.now().minute
    getCategoryData(srchUrl, fileName)
    #allInfo = getCategoryData(srchUrl, fileName)
    #for each in allInfo:
    #    l, phones = each
    #    p1, p2 = phones
    #    catStr = catStr + p1 + ',' + p2 + ',' + l + "\n"
    print datetime.datetime.now().time().isoformat()
