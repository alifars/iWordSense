# -*- coding: utf-8 -*-

import nltk, nltk.corpus, codecs
import pyodbc
from nltk.corpus import XMLCorpusReader
from nltk.corpus.util import LazyCorpusLoader

print "connecting to database"
connection = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\\farsnettest.mdb")
c = connection.cursor()
print "reading the corpus"
corpus = LazyCorpusLoader('hamshahricorpus', XMLCorpusReader, r'(?!\.).*\.xml')

def correctPersianString(source):
    if source is not None:
        source = source.strip()
        #replace("\\b\\s{2,}\\b", " ")

        #replace shift x with persian ye
        source = source.replace(u'\u064a', u'\u06cc')

        #replace arabic k with persian k
        source = source.replace(u'\u0643', u'\u06a9')

        #replace h dar shift+n
        source = source.replace(u'\u0623', u'\u0627')

        #persian z
        source = source.strip().replace(u'\u0632\\s', u'\u0632')

        #persian d
        source = source.strip().replace(u'\u062F\\s', u'\u062F')

        #persian r
        source = source.strip().replace(u'\u0631\\s', u'\u0631')

        #persian zhe
        source = source.strip().replace(u'\u0698\\s', u'\u0698')

        #persian vav
        source = source.strip().replace(u'\u0648\\s', u'\u0648')

        #persian dal zal
        source = source.strip().replace(u'\u0630\\s', u'\u0630')

        #persian alef bi kolah
        source = source.strip().replace(u'\u0627\\s', u'\u0627')

        #persian alef ba kolah
        source = source.strip().replace(u'\u0622\\s', u'\u0622')

        return source


c.execute("select wordtext,gloss,example,senseID,synsetID from wordssynsets")
#file2 = codecs.open('d:\\wsdtext.txt', 'r', 'utf-8')
outfile = codecs.open('d:\\wsd\\milk.txt', 'w', 'utf-8')

stopwords = [u'و', u'به', u'از', u'در', u'بر', u'را', u'با', u'که', u'های', u'می', u'یا', u'برای',
             u'است', u'تا', u'آن', u'دارد', u'شود', u'او', u'ها', u'هم', u'شده', u'کند', u'من', u'ای', u'هر',
             u'کنند', u'کند', 'دهند', 'اگر', u'آنها', u'دهند', u'اش', u'شد', u'اگر', u'.', u'،', u'این', u'اینها',
             u'بود', u'کرد', u'کردند', u'وی', u'باشد', u'باشند', u'خود', u'بود', u'شد',
             u'زیرا', u'اما', u'ولی', u'چون', u'اند',
             u'دارند', u'شوند', u'می', u'هایش', u'هایشان', u'هایت', u'هایم', u'یک', u'گفت',
             u'نیز', u'مانند', u'هایی', u'کرده', u'کردن', u'بی', u'دهد',
             u'نمی', u'ام', u'هایتان', u'نه', u'آیا', u'دیگر', u'هستند', u'بودند', u'نیست', u'نیستند', u'درباره',
             u'کنید', u'همه', u'هیچ', u'خواهد', u'همین', u'چه', u'چرا', u'کنیم', u'داد',
             u'توان', u'تواند', u'شما', u'حتی', u'مثل', u'می']
words = []
count = 0
#for line in file2:
#    line=line.strip()
#    tokens=line.split()
#    for token in tokens:
#        words.append(token)
wordsense = {}
#for word in  words:
#    print word

word = u'شانه'
print "target word is "+word
synidis = []
for item in c:
    item[1] = correctPersianString(item[1])
    item[0] = correctPersianString(item[0])
    #  print item[0],item[1]


    if word == item[0]:
        if item[2]:
            mixed = item[1] + ' ' + item[2]
        else:
            mixed = item[1]

        wordsense.setdefault(item[0], []).append((mixed, item[3], item[-1]))

c.execute("select synsetID1, synsetID2,relation from synrelations")
simpledic = {}
for item in wordsense.values():
    for i in range(len(item)):
        simpledic[item[i][-2]] = item[i][-1]

print simpledic
hyponyms = {}
for row in c:
    for item in wordsense.values():
        for i in range(len(item)):
        # print item[i][1],item[i][-1]
            if item[i][-1] == row[0]:
            # print item[i][-1]

                hyponyms.setdefault(item[i][1], []).append(row[1])
            else:
                pass

finaldic = {}
for item in simpledic:
    if item in hyponyms:
        list = hyponyms[item][:]
        list.append(simpledic[item])
        finaldic[item] = list
    else:
        mylist=[]
        mylist.append(simpledic[item])
        finaldic[item] = mylist
        #finaldic[item] = simpledic[item]

print "final dict"
print finaldic
c.execute("select wordtext,gloss,example,senseID,synsetID from wordssynsets")
extended = {}
for item in c:
    item[1] = correctPersianString(item[1])
    item[0] = correctPersianString(item[0])
    #  print item[0],item[1]
    for u in hyponyms.values():
      #  print u,item[-1]
        if item[-1] in u:
            for it in hyponyms:
                if hyponyms[it] == u:
                    extended.setdefault(it, []).append(item[1])


c.execute("select synsetID, gloss,example,senseid from synsets")
realfinal = {}
for row in c:
 
  for item in finaldic:

      for senseID in finaldic[item]:
           if senseID ==row[0]:
               row[1] = correctPersianString(row[1])
        
               if senseID not in realfinal:
                  realfinal[senseID] = row[1]
                   

#               print row[1]
for item in  realfinal:
    print item, ''.join(realfinal[item])
#for row in c:
#    for item in finaldic:
#
#        value = finaldic[item]
#        print value
#        row[1] = correctPersianString(row[1])
##        row[0]= correctPersianString(row[0])
#
#        if type(value) == int:
#            if value == row[0]:
#
#                realfinal.setdefault(item, []).append(row[1])
#        else:
#            for any in value:
#                if any == row[0]:
#                    realfinal.setdefault(item, []).append(row[1])
#            if any == row[0]:
#                 print item,rowfor item in  realfinal.values():
#
#    print ''.join(ite[1]
print "real final"
#m)
#

words = [u'شیر']

total = 0
nooverlap = 0
num = 0
number = 0
commonwords = {}
#for i in realfinal:
#    print i, ' '.join(set(realfinal[i]))
for file in corpus.fileids():
#
#   #if num==1000: break
    for doc in  corpus.xml(file).getchildren():
    #
        cat = doc.getchildren()[3].text#
        text = doc.getchildren()[5].text
        newtext = correctPersianString(text)
        allwords = text.split()
        sents = newtext.split('.')
        #          for word in words:
        #           # print word
        for sent in sents:
            if word in sent.split():
                total += 1
                overlap = {}
                bestsenses = []
                context = sent.split()
                purecontextwords = set(context) - set(stopwords)
                for item in realfinal:
                    list = []
                    senseid = item
                    #           print senseid
                    glosswords = realfinal[item]
                    for l in glosswords:
                        for m in l.split():
                            list.append(m)
                    pureglosswords = set(list) - set(stopwords)
                    common = set(pureglosswords) & set(purecontextwords)
                    if word in common:
                        common.remove(word)
                    overlap[senseid] = len(common)
                    if common:
                        #commonwords[senseid]=list(common)
                        commonwords.setdefault(senseid, []).append(' '.join(common))
                bestoverlap = max(overlap.values())
                if bestoverlap > 0:
                    for item  in overlap.keys():
                        if overlap[item] == bestoverlap:
                            bestsenses.append(item)

                if len(bestsenses) == 0:
                    pass
                #
                # 0,1,2,5,6,7
                elif len(bestsenses) > 0:
                    if 0 in bestsenses or 1 in bestsenses or 2 in bestsenses or 5 in bestsenses or 6 in bestsenses or 7 in bestsenses:
                    # if 1 in bestsenses:



                    #
                        number += 1
                        #print ' '.join(context), bestsenses

                        #print '\n'
                    else:
                        pass
                        #print ' '.join(context),'\t',bestsenses
                        # num+=1
                    #
                elif len(bestsenses) == 1:
                    if bestsenses[0] == 0:
                        pass

                    #
                    #    print ' '.join(context),'\t',bestsenses
##
#
#                          if bestsenses[0]==4:
#                                print ' '.join(context)
##                                outfile.write(' '.join(context))
#                                outfile.write('\n')


#                     # print len(bestsenses)
#
##for item in  commonwords:
##    print item, ' '.join(set(commonwords[item]))
#print 'total samples of target word',total
#print 'dont have overlap:',nooverlap
#print 'have one sene:',anothercount
#print 'sense#0 milk', num
file2.close()
connection.close()
outfile.close()
print "all samples:", total, number