# -*- coding: utf-8 -*-
import codecs
import glob
import logging
from gensim import corpora, models, similarities
from gensim.models.tfidfmodel import TfidfModel
import nt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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


stoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها']





dictionary = corpora.Dictionary(line.split() for line in codecs.open('d:\\hamshir5.txt','r','utf-8'))
for item in dictionary.values():
    if item  in stoplist:
        print item
        if item in dictionary:
           dictionary.pop(item)
#dictionary.compactify()
dictionary.save('d:\\shir.dict')
#for i in sorted(dictionary.keys()):
#
#        print i,dictionary[i]



class MyCorpus(object):
    def __iter__(self):
#        for name in filenames:
#    # print name
#
#          filename=name.split('\\')[-1]
#
#
#          file=codecs.open(filename,'r','utf-8')
#          text=file.read()
      # for line in codecs.open('d:\\hamsh.txt','r','utf-8').read().split('endofdoc'):
        for line in codecs.open('d:\\hamshir5.txt','r','utf-8'):

          pureline=correctPersianString(line)
          pureline.strip(u'.،')
        #  print pureline
          newline=[]
          for w in pureline.split():
                  w.strip(u'.،:؛!()')


                  newline.append(w)
             #print ' '.join(newline)
          yield dictionary.doc2bow(newline)
###
corpus = MyCorpus()
#corpora.MmCorpus.serialize('d:\\shir.mm', corpus)
corpora.BleiCorpus.serialize('d:\\shir.lda-c', corpus)
#for vec in  corpus:
#  print vec
