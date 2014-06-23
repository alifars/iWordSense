# -*- coding: utf-8 -*-
import collections
import os
import pickle
import random
from random import choice
import codecs, glob, nt
from nltk import metrics
import nltk



filenames = os.listdir('d:\\hamshirsource\\')
       # filenames = os.listdir(inputdir)

inputdir = 'd:\\hamshirsource\\'
senseslist = []
for name in filenames:
# print name
        lineno=0
        path = os.path.join(inputdir, name)
        sense = name.split('\\')[-1].split('.')[0]
        print 'training', sense
        senseslist.append(sense)

print senseslist
for name in filenames:
# print name
        lineno=0
        sensematchno = 0
        path = os.path.join(inputdir, name)
        sense = name.split('\\')[-1].split('.')[0]
        print 'training', sense
        file = codecs.open(path, 'r', 'utf-8')
#        allwords = []
        for line in file:
              lineno+=1
              random_sense = choice(senseslist)
              if  sense == random_sense:
                    sensematchno+=1

        print sensematchno,lineno
        print sensematchno*100/lineno