# -*- coding: utf-8 -*-
import collections
import os
import pickle
import random

import codecs, glob, nt
from nltk import metrics
import nltk
from nltk.classify.maxent import MaxentClassifier
from nltk.probability import FreqDist, ConditionalFreqDist

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify import DecisionTreeClassifier
from nltk.classify.util import accuracy
import sys


mystoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',
           u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',u'ما'
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها',
           u'.',u'،',u'؛',u':',u')',u'(',u'_',u'-',u'!',u'؟'
           u'کرد',u'بود',u'شد',u'برای‌این‌که',u'ـ',u'می‌شود',u'می‌کنند',u'نیز',u'ولی',u'اما',u'?',
           u'#',u'...',u'\"',u'*',u'-',u'#',u'-',u'/',
           u'باشد',u'باشند',u'خود']

classifier_save_file = open('d:\\classifier.pickle', 'wb')

def bag_of_words_feat(line):
    words=[]
    for item in line.split():
        words.append(item.split('\\')[0])
    return dict([(word, True) for word in words])

def bag_of_words(words):

    return dict([(word, True) for word in words])

def bag_of_words_in_set(words, goodwords):
    return bag_of_words(set(words) & set(goodwords))
def bag_of_Nostopword_feats(line):
    purewords=[]
    words=[]
    for item in line.split():
        words.append(item.split('\\')[0])
    for word in words:
        if word in mystoplist:
            pass
        else: purewords.append(word)
    return dict([(word, True) for word in purewords])

def bigram_feature(words):
   match =u"شیر"

   mybigrams = []
   bigram_finder = BigramCollocationFinder.from_words(words)
   score_fn=BigramAssocMeasures.raw_freq
   bigrams = bigram_finder.nbest(score_fn, 2000)

   for item in bigrams:
       if item[0] not in mystoplist and item[1] not in mystoplist:

          if item[0]==match or item[1]==match:

                mybigrams.append(item)
              #  print item[0], item[1]

   return dict([(item, True) for item in mybigrams])


def high_information_words(labelled_words, score_fn=BigramAssocMeasures.chi_sq, min_score=5):
    word_fd = FreqDist()
    label_word_fd = ConditionalFreqDist()
    for label, words in labelled_words:
         for word in words:
                word_fd.inc(word)
                label_word_fd[label].inc(word)
    n_xx = label_word_fd.N()
    high_info_words = set()
    for label in label_word_fd.conditions():
        n_xi = label_word_fd[label].N()
        word_scores = collections.defaultdict(int)
    for word, n_ii in label_word_fd[label].iteritems():
        n_ix = word_fd[word]
        score = score_fn(n_ii, (n_ix, n_xi), n_xx)
        word_scores[word] = score
    bestwords = [word for word, score in word_scores.iteritems() if score >= min_score]
    high_info_words |= set(bestwords)
    return high_info_words

def context_feature(line):
    match=u'شیر'
    features = {}
    tokens=line.split()
    words=[]
    tags=[]
    #features["word"]= match
    for item in tokens:
       if len(item.split('\\'))==2:
            word=item.split('\\')[0]
            tag= item.split('\\')[1]
            words.append(word)
            tags.append(tag)
#    for i in range(len(tags)):
#        print words[i],tags[i]
    for item in words:
        if item in mystoplist:
            words.remove(item)
    if match in words:
          ind = words.index(match)
          #features['tag']= tags[ind]
    
      
#          if ind<len(words)-1:
#                 features["next word"] = words[ind+1]
#                 features["next tag"] = tags[ind+1]
#          if ind>0:
#                features["prev word"] = words[ind-1]
#                features["prev tag"] = tags[ind-1]

#       # features["two next word"] = words[ind+2]

      #  features["two prev word"] = words[ind-2]




    return features



def classify(inputdir):
        #filenames = os.listdir('d:\\shir\\')
        filenames = os.listdir(inputdir)

        feat_set = []
        sets = []
        labeledlist = []
        for name in filenames:
        # print name
                lineno=0
                path = os.path.join(inputdir, name)
                sense = name.split('\\')[-1].split('.')[0]
                print 'training', sense

                file = codecs.open(path, 'r', 'utf-8')
                allwords = []
                for line in file:
                      if len(line.split())>2:
                             lineno+=1
                             line = line.strip()

                             words = line.split()


                             feat_set.append((bag_of_words(line),sense))
                             #feat_set.append((context_feature(line),sense))
                      else:
                          words=[]





                file.close()
        #int i[0].keys()
        random.shuffle(feat_set)
        random.shuffle(feat_set)
        #random.shuffle(feat_set)


        seed_classifier = NaiveBayesClassifier.train(feat_set)
        classifier_save_file = open('d:\\classifier.pickle', 'wb')
        pickle.dump(seed_classifier, classifier_save_file)
        classifier_save_file.close()



classify("d:\\shirseeds2\\")

  