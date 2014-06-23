
# -*- coding: utf-8 -*-




import nltk, nltk.corpus,codecs,re

#from nltk.book import *
from nltk.corpus import XMLCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import TaggedCorpusReader
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

#file=codecs.open('d:\\test.txt','r','utf-8')
#tw=raw_input('enter a word')
#print type(tw)
#new=tw.encode('utf-8')




stoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها',
           u'بود']
punclist=[u'.',u',',u'،',u'؛',u':',u'؟',u'-',u'/']


def ham_corpus_maker(outpath, word):
        corpus = LazyCorpusLoader('hamshahricorpus',XMLCorpusReader, r'(?!\.).*\.xml')
        outfile=codecs.open(outpath,'w','utf-8')
        count=0
        instancenum=0
        targetwordnum=0
        for file in corpus.fileids():
            #print file

            for doc in  corpus.xml(file).getchildren():

               # print doc.getchildren()
                   cat=doc.getchildren()[3].text#
                   text=doc.getchildren()[5].text
                   newtext=correctPersianString(text)
                   newtext= newtext.replace('\n',' ')
                   textlines= newtext.split('.')
                   if word in newtext.split():
                       print newtext
                       outfile.write(newtext)
                       outfile.write('\n')
                       print
                       print







        print str(instancenum)+" seeds found "
        print str(targetwordnum)+" target word found "




        outfile.close()

ham_corpus_maker('d:\\hamshir2.txt',u'شیر')





#ham_seed_maker('d:\\hammilk.txt',[u'شیر مادر',u'شیر و پنیر',u'شیر گاو'],u'شیر')
#ham_seed_maker('d:\\hamlion.txt',[u'شیر وحشی',u'شیر و ببر',u'شیر و پلنگ'],u'شیر')
#ham_seed_maker('d:\\hamtap.txt',[u'شیر آب',u'شیر گاز',u'بستن شیر'],u'شیر')
#
#ham_seed_maker('d:\\hamshir2.txt',u'شیر')