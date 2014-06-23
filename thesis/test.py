# -*- coding: utf-8 -*-
import codecs
from nltk.collocations import BigramCollocationFinder
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
punclist = [u'?',u'-',u'(',u')',u'?',u'[',u']',u'*']

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
def bigram_finder(match,filepath):
   print '*********************'
   file = codecs.open(filepath,'r','utf-8')
   allwords = []
   mybigrams = []
   for line in file:
       print line
       words= line.split()
#       allwords.extend(words)
#
#
#   bigram_finder = BigramCollocationFinder.from_words(allwords)
#   score_fn=BigramAssocMeasures.raw_freq
#   bigrams = bigram_finder.nbest(score_fn, 2000)
#
#   for item in bigrams:
#       if item[0] not in mystoplist and item[1] not in mystoplist:
#
#          if item[0]==match or item[1]==match:
#
#                mybigrams.append(item)
#                print item[0],item[1]


bigram_finder(u'شانه','d:\\shane.txt')