# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import nltk
from nltk.collocations import *
from nltk.metrics.association import BigramAssocMeasures

from pattern.web import Google, SEARCH, plaintext, Wikipedia, Newsfeed, Yahoo, Bing, Twitter, URL, Result

mystoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها',
           u'بود',u'کرد',u'کردند',u'وی', u'باشد',u'باشند',u'خود',u'بود',u'شد',
           u'زیرا',u'اما',u'ولی',u'چون',u'اند',
           u'دارند',u'شوند',u'می',u'هایش',u'هایشان',u'هایت',u'هایم',u'یک',u'گفت',
           u'نیز',u'مانند',u'هایی',u'کرده',u'کردن',u'بی',u'دهد',
           u'نمی',u'ام',u'هایتان',u'نه',u'آیا',u'دیگر',u'هستند',u'بودند',u'نیست',u'نیستند',u'درباره',
           u'کنید',u'همه',u'هیچ',u'خواهد',u'همین',u'چه',u'چرا',u'کنیم',u'داد',
           u'توان',u'تواند',u'شما',u'حتی',u'مثل']
punclist = [u'،',u'-',u'(',u')',u'؛',u'[',u']',u'*']

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


def bigram_finder(words, score_fn=BigramAssocMeasures.raw_freq,n=200):

   mybigrams = []
   bigram_finder = BigramCollocationFinder.from_words(words)

   bigrams = bigram_finder.nbest(score_fn, n)

   for item in bigrams:
       if item[0] not in mystoplist and item[1] not in mystoplist:
         #   print item [0], item[1]
            mybigrams.append(item)

   for item in mybigrams:
       print item[0],item[1]
  # print bag_of_words(bigrams)
   return mybigrams

def seed_maker(targetword,coloclist, sourcepath, sense):
        print "#######################################################"
        print "# collecting seeds                                     #"
        print "#######################################################"

        feat_set = []
        sets = []
        allwords = []
        matchnum=0
        indexlist = []
        unwanted = []
        instancenum=0
        outdir='d:\\hamshir'


        sense = sense+".txt"
        seedpath = os.path.join(outdir, sense)
        seedfile = codecs.open(seedpath, 'w', 'utf-8')
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        sourcetext = sourcefile.read()
        sourcefile.close()
        sourcenews = sourcetext.split('ALI')
        for news in sourcenews:

                   lines = news.split('.')
                   noitemfound = True
                   for item in coloclist:

                         if item  in  news:
                             noitemfound = False


                   for item in coloclist:
                       if item in news:
                            for line in lines:
                                if item in line:
                                        seedfile.write(line)
                                        seedfile.write('\n')
                                        seedfile.write('\n')
                                if item not in line and targetword in line:
                                        seedfile.write(line)
                                        seedfile.write('\n')
                                        seedfile.write('\n')


                   if noitemfound:
                           unwanted.append(news)

        print str(instancenum)+" of target word found in corpus"
        print str(matchnum)+" found in corpus for "+ sense
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')
        for news in unwanted:

            sourcefile.write(news)
            sourcefile.write('ALI')

        sourcefile.close()
        seedfile.close()
        


def corpus_convert(match,sourcepath,outpath):
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        outfile = codecs.open(outpath, 'w', 'utf-8')
        sourcetext = sourcefile.read()
        sourcefile.close()
        sourcenews = sourcetext.split('ALI')
        for news in sourcenews:
             lines = news.split('.')
             for line in lines:
                 if match in line.split():
                         outfile.write(line)
                         outfile.write('\n')
                         outfile.write('\n')

def google_search(targetword, itemlist,targetpath):
    resultnum=0
    engine = Google(license=None)
    file = codecs.open(targetpath,'a','utf-8')
    outtext= ''
    patt = ur'\W+'
    for item in itemlist:
        for i in range(1,5):
            for result in engine.search(item, type=SEARCH, start=i):

                  url = URL(result.url)
                  text = url.download(unicode=True)

                  text = plaintext(text)
                  text = correctPersianString(text)
                  text = text.replace('\n',' ')
                  lines = text.split('.')
                  for line in lines:
                      if targetword in line:

                              match = re.findall(patt,line)
                              output =  ' '.join(match)

                              for item in punclist:
                                  if item in line:
                                      line = line.replace(item,' ')

                              print output
                              file.write(output)
                              file.write('\n')
    print str(resultnum)+" found in web"
    file.close()


#
#seed_maker(u'شیر',[u'باغ وحش',u'شیر درنده',u'شیر آسیایی',u'چنگال شیر',u'شیر طلایی'],'d:\\hamshir.txt','lion')
#seed_maker(u'شیر',[u'شیر مادر',u'کارخانه شیر',u'شیر پاستوریزه',u'قیمت شیر',u'مصرف شیر'],'d:\\hamshir.txt','milk')
#seed_maker(u'شیر',[u'شیر گاز',u'شیر سیلندر',u'شیر آب',u'شیر فلکه',u'شیر صنعتی'],'d:\\hamshir.txt','tap')

#seed_maker(u'شیر',[u'باغ وحش',u'شیر درنده',u'شیر آسیایی',u'چنگال شیر',u'شیر طلایی',u'شیر سنگی'],'d:\\hamshir.txt','lion')
#seed_maker(u'شیر',[u'شیر مادر',u'کارخانه شیر',u'شیر پاستوریزه',u'قیمت شیر',u'مصرف شیر',u'شیر دادن',u'لبنیات',u'شیر گاو',u'شیر گوسفند',u'شیر خشک'],'d:\\hamshir.txt','milk')
#seed_maker(u'شیر',[u'شیر گاز',u'شیر سیلندر',u'شیر آب',u'شیر فلکه',u'شیر صنعتی'],'d:\\hamshir.txt','tap')
#
##corpus_convert(u'شیر',  'd:\\hamshir.txt','d:\\shirready.txt')
###    ('lion',[u'باغ وحش',u'شیر درنده',u'شیر آسیایی',u'چنگال شیر']),
###    ('',[u'شیر مادر',u'کارخانه شیر',u'شیر پاستوریزه',u'صنایع شیر',u'قیمت شیر'])]
###
###    ,'d:\\hamshir.txt')
#google_search(u'شیر',[u'شیر وحشی',u'شیر و ببر',u'شیر و پلنگ'], "d:\\hamshir\\lion.txt")

#google_search(u'شیر',[u'شیر آب',u'شیر گاز',u'بستن شیر'], "d:\\hamshir\\tap.txt")

#seed_remove_from_corpus('d:\\hamshir','d:\\hamshir.txt','d:\\remain.txt')
seed_maker(u'سیر',[u'حبه سیر',u'سیر ترشی',u'سیر و پیاز'],'d:\\sir.txt','garlic')
seed_maker(u'سیر',[u'سیر شدن',u'سیر شد',u'گرسنه'],'d:\\sir.txt','full')