# -*- coding: utf-8 -*-

import codecs
import urllib2
import nltk
from nltk.collocations import *
from pattern.web import Google, SEARCH, plaintext, Wikipedia, Newsfeed, Yahoo, Bing, Twitter, URL, Result

#count=0
milkfile=codecs.open('d:\\webseeds\\webmilk.txt','w','utf-8')
lionfile=codecs.open('d:\\webseeds\\weblion.txt','w','utf-8')
tapfile = codecs.open('d:\\webseeds\\webtap.txt','w','utf-8')
#

#engine = Wikipedia(language="fa")
#engine = Bing(license=None)
#engine = Twitter(license=None, throttle=0.5, language=None)
#       print result.download()
#



def google_search(match,targetfile):
    engine = Google(license=None)
    for i in range(1,10):
        for result in engine.search(match, type=SEARCH, start=i):
              print plaintext(result.description)
              targetfile.write(plaintext(result.description))
              targetfile.write('\n')

def bing_search(match):
    engine = Bing
    for i in range(1,10):
        for result in engine.search(match, type=SEARCH, start=i):
              print plaintext(result.description)

engine = Bing() # Enter your license key.
for i in range(1,15):
    for result in engine.search('holy', type=SEARCH, start=i):
        print plaintext(result.description)
        print
#google_search(u'شیر مادر', milkfile)
#google_search(u'شیر وحشی', lionfile)
#google_search(u'شیر آب', tapfile)
##article =  engine.search(match)
#print article.title
#for link in  article.links:
#    print link
#    #subarticle = engine.search(link)
#    url = URL(link)
#    result = Result(url)
#    print result.download()

#    print item
#for item in  engine.search(match,count=10):
#    print item.description
#    #print item

#
#       url = URL(result.url)
#       result = Result(url)
#       print result.download()
milkfile.close()
lionfile.close()
tapfile.close()