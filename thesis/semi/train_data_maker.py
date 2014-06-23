# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import nltk
from nltk.collocations import *
from nltk.metrics.association import BigramAssocMeasures




punclist=[u'.',u',',u'،',u'؛',u':',u'؟',u'-',u'/']

def seed_maker(target,coloclist, sourcepath, outpath):



        feat_set = []
        sets = []
        allwords = []
        matchnum=0
        indexlist = []


        outfile = codecs.open(outpath, 'a', 'utf-8')
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        sourcelines = sourcefile.readlines()
        sourcefile.close()
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')

        for line in sourcelines:
               for item in coloclist:
                     if item  in  line:
                           for subline in line.split('.'):
                               if target in subline.split():
                                  #   print subline
                                     outfile.write(subline)
                                     outfile.write('\n')
                                     outfile.write('\n')

                           indexlist.append(sourcelines.index(line))
                           
#                     else:

        for num in indexlist:
            if num in range(0,len(sourcelines)-1):
                sourcelines.pop(num)
        for line in sourcelines:
                             sourcefile.write(line)
                          

        sourcefile.close()


        outfile.close()


seed_maker(u'شیر',[u'شیر مادر',u'کارخانه شیر',u'شیر پاستوریزه',u'صنایع شیر',u'قیمت شیر'],'d:\\hamshir7.txt','d:\\hammilk.txt')
seed_maker(u'شیر',[u'باغ وحش',u'شیر درنده',u'شیر آسیایی',u'چنگال شیر'],'d:\\hamshir7.txt','d:\\hamlion.txt')
seed_maker(u'شیر',[u'شیر گاز',u'شیر سیلندر',u'شیر آب'],'d:\\hamshir7.txt','d:\\hamtap.txt')