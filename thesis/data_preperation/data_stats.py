# -*- coding: utf-8 -*-
import codecs
import os
import re
import urllib2
import nltk
from nltk.collocations import *
from nltk.metrics.association import BigramAssocMeasures


def data_stats(targetword, sourcepath):
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
        lineno=0
        newsnum=0






        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        sourcetext = sourcefile.read()
        sourcefile.close()
        sourcenews = sourcetext.split('ALI')

        for news in sourcenews:
                   newsnum+=1

                   lines = news.split('.')
                   for line in lines:
                       lineno+=1
                       if targetword in line:
                                       instancenum+=1
                                        #lines.remove(line)
#                                    if targetword in line and item not in line:
#
#                               print line


        print str(instancenum)+" target word found in corpus"
        print str(lineno)+" lines are  in corpus"
        print str(newsnum)+" lines are  in corpus"

data_stats(u'شیر','d:\\hamshir.txt')