__author__ = 'ali'
# -*- coding: utf-8 -*-

import nltk, nltk.corpus,codecs
import pyodbc

connection = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=E:\\farsnettest.mdb")
c = connection.cursor()
file = codecs.open("d:\shir.txt","r","utf-8")
#corpus = LazyCorpusLoader('hamshahricorpus',XMLCorpusReader, r'(?!\.).*\.xml')

def correctPersianString(source):
    if source is not None:
        source = source.strip()#.replace("\\b\\s{2,}\\b", " ")

        #replace shift x with persian ye
        source = source.replace(u'\u064a', u'\u06cc' )

        #replace arabic k with persian k
        source = source.replace(u'\u0643', u'\u06a9' )

        #replace h dar shift+n
        source = source.replace(u'\u0623', u'\u0627' )

        #persian z
        source = source.strip().replace(u'\u0632\\s', u'\u0632' )

        #persian d
        source = source.strip().replace(u'\u062F\\s',u'\u062F' )

        #persian r
        source = source.strip().replace(u'\u0631\\s',   u'\u0631' )

        #persian zhe
        source = source.strip().replace(u'\u0698\\s',   u'\u0698' )

        #persian vav
        source = source.strip().replace(u'\u0648\\s',u'\u0648' )

        #persian dal zal
        source = source.strip().replace(u'\u0630\\s', u'\u0630' )

        #persian alef bi kolah
        source = source.strip().replace(u'\u0627\\s',       u'\u0627' )

        #persian alef ba kolah
        source = source.strip().replace(u'\u0622\\s',   u'\u0622' )

        return source


c.execute("select wordtext,gloss,example,senseID from wordssynsets")
#file2=codecs.open('d:\\wsdtext.txt','r','utf-8')
outfile=codecs.open('d:\\wsd\\milk.txt','w','utf-8')

stopwords=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها',
           u'بود',u'کرد',u'کردند',u'وی', u'باشد',u'باشند',u'خود',u'بود',u'شد',
           u'زیرا',u'اما',u'ولی',u'چون',u'اند',
           u'دارند',u'شوند',u'می',u'هایش',u'هایشان',u'هایت',u'هایم',u'یک',u'گفت',
           u'نیز',u'مانند',u'هایی',u'کرده',u'کردن',u'بی',u'دهد',
           u'نمی',u'ام',u'هایتان',u'نه',u'آیا',u'دیگر',u'هستند',u'بودند',u'نیست',u'نیستند',u'درباره',
           u'کنید',u'همه',u'هیچ',u'خواهد',u'همین',u'چه',u'چرا',u'کنیم',u'داد',
           u'توان',u'تواند',u'شما',u'حتی',u'مثل']
words=[u"شیر"]
count=0

wordsense={}


for item in c:
   for word in words:
      item[1]= correctPersianString(item[1])
      item[0]= correctPersianString(item[0])


      if word==item[0]:
         mixed=item[1]+' '+item[2]
         wordsense.setdefault(item[0], []).append((mixed,item[3]))


#print wordsense
anothercount=0
total=0
nooverlap=0
num=0
commonwords={}
for line in file:

              overlap={}

              bestsenses=[]

              context=line.split()
           #   print ' '.join(context)
#                  outfile.write(' '.join(context))
              purecontextwords=set(context)-set(stopwords)
              contextwords = set(context)

              for i in range(len(wordsense[word])):
                      senseid=wordsense[word][i][1]
                      glosswords=wordsense[word][i][0].split()
                    #  print senseid,' '.join(glosswords)
                      pureglosswords=set(glosswords)-set(stopwords)
                      common=set(pureglosswords)&set(purecontextwords)
                      #common= set(contextwords) & set(glosswords)
                      if word in common:
                             common.remove(word)
                      overlap[senseid]=len(common)
                      if common:
                       #commonwords[senseid]=list(common)
                       commonwords.setdefault(senseid, []).append(' '.join(common))
#                          if common:
                       print ' '.join(common)

              #print overlap
              bestoverlap=max(overlap.values())
              print bestoverlap
              if bestoverlap>0:

                  for item  in overlap.keys():
                      if overlap[item]==bestoverlap:
                          bestsenses.append(item)
              else:
                  nooverlap+=1
#              if len(bestsenses)==0:
#                  pass
#
#
#              elif 0 in bestsenses or 1 in bestsenses or 2 in bestsenses or 5 in bestsenses or 6 in bestsenses or 7 in bestsenses:
##                      if 3 in bestsenses:
##                          pass
#
#                     print ' '.join(context),'\t',bestsenses
#                     num+=1
#
#              elif len(bestsenses)==1:
#                      print ' '.join(context),'\t',bestsenses
#
#                      anothercount+=1
#                      if bestsenses[0]==4:
#                          pass
#
#                         #   print ' '.join(context)+'\n'
##                                outfile.write(' '.join(context))
##                                outfile.write('\n')
#
#              else:
#                  pass
#                  #print ' '.join(context),'\t',bestsenses

                 # print len(bestsenses)

#for item in  commonwords:
#    print item, ' '.join(set(commonwords[item]))
print 'total samples of target word',total
print 'dont have overlap:',nooverlap
print 'have one sene:',anothercount
print 'sense#0 lion', num
#file2.close()
connection.close()
outfile.close()