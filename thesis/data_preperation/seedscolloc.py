# -*- coding: utf-8 -*-
import codecs
import os
import nltk
from nltk.collocations import *
from nltk.metrics.association import BigramAssocMeasures

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

#
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

def seed_maker(target, sense,sourcepath, seedspath):

        seeddir = os.path.dirname(seedspath)

        
        try:
            os.makedirs(seedspath)
        except OSError:
            pass

        feat_set = []
        sets = []
        allwords = []
        outpath = os.path.join(seedspath,sense+".txt")

        outfile = codecs.open(outpath, 'w', 'utf-8')
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        sourcelines = sourcefile.readlines()
        for line in sourcelines:
              if len(line.split())!=0:
                  
                     line = line.strip()
                     words=[]
                     tags=[]
                     tokens = line.split()

                     for item in tokens:
                           if len(item.split('\\'))==2:
                                word=item.split('\\')[0]
                                tag= item.split('\\')[1]
                                words.append(word)
                                tags.append(tag)

                              #  allwords.append(word)
                    # if target.split()[0] in words and  target.split()[1] in words:
                     if target in ' '.join(words):
                         sourcelines.remove(line)
                         print ' '.join(tokens)
                         outfile.write(' '.join(tokens))
                         outfile.write('\n')
                     else:

                         
                          outfile.write('\n')



        sourcefile.close()
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')
        for line in sourcelines:
            sourcefile.write(line)
            sourcefile.write('\n')
        sourcefile.close()
        outfile.close()
       

seed_maker(u"شیر مادر","milk","d:\\shir2.txt","d:\\shirseeds2")
seed_maker(u"شیر آب","tap","d:\\shir2.txt","d:\\shirseeds2")
seed_maker(u"شیر و ببر","lion","d:\\shir2.txt","d:\\shirseeds2")