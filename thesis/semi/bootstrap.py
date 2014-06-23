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
           u'باشد',u'باشند',u'خود',u'دیگر',u'هستند',u'بودند',u'نیست',u'نیستند',u'درباره',
            u'کنید',u'همه',u'هیچ',u'خواهد',u'همین',u'چه',u'چرا',u'کنیم',u'داد',
            u'شده',u'می',u'ها']



def bag_of_words_feat(words):

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



def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.raw_freq,n=500):
        match =u"شیر"
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)
        mybigrams=[]
        purewords=[]
        for word in words:
              if word in mystoplist:
                pass
              else: purewords.append(word)
        for item in bigrams:
           if item[0] not in mystoplist and item[1] not in mystoplist:

                  if item[0]==match or item[1]==match:

                        mybigrams.append(item)
                       # print item[0], item[1]
        return bag_of_words(purewords + mybigrams)


def train_feats(myset):
    train_feats = []
    trainlen = int(.25 * len(myset))
    for item in myset[trainlen:]:
        train_feats.append(item)

    #        print i
    return train_feats

#
def test_feats(myset):
    test_feats = []
    trainlen = int(.25 * len(myset))
    # print trainlen
    for item in myset[:trainlen]:
        test_feats.append(item)

    return test_feats


def train_classifier(inputdir):
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
              #  print 'training', sense

                file = codecs.open(path, 'r', 'utf-8')

                for line in file:
                      if len(line.split())>2:
                           #  print line
                             lineno+=1
                             line = line.strip()

                             words = line.split()
                          
                             feat_set.append((bag_of_bigrams_words(words),sense))
                             #feat_set.append((context_feature(line),sense))
                      else:
                          words=[]
                          tags=[]


                file.close()
        
        random.shuffle(feat_set)
        random.shuffle(feat_set)
        random.shuffle(feat_set)


        seed_classifier = NaiveBayesClassifier.train(feat_set)

        classifier_save_file = open('d:\\classifier.pickle', 'wb')
        print len(feat_set)

#        for item in feat_set:
#            for word in  item[0].keys():
#                print word
        pickle.dump(seed_classifier, classifier_save_file)
        classifier_save_file.close()









def apply_classifier(sourcepath,inputdir,goldstandardpath):
        f= open('d:\\classifier.pickle', "rb")
        print "loading classifier"
        classifier = pickle.load(f)
        print "classifier labels"
        print classifier.labels()
        filenames = os.listdir(inputdir)
        paths = []
        files=[]
        lines=[]
        goldfeatset = []
        tapnum, lionnum,milknum=0,0,0
        print "reading from"+str(inputdir)
        goldfilenames = os.listdir(goldstandardpath)

        for name in goldfilenames:

                path = os.path.join(goldstandardpath, name)
                sense = name.split('\\')[-1].split('.')[0]
                print 'training', sense

                file = codecs.open(path, 'r', 'utf-8')
                allwords = []
                for line in file:
                      if len(line.split())>2:
                             words = line.split()

                             goldfeatset.append((bag_of_bigrams_words(words),sense))

        for name in filenames:

            path = os.path.join(inputdir, name)
            file= codecs.open(path, 'a', 'utf-8')
            files.append(file)
            paths.append(path)

        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        lines = sourcefile.readlines()
        sourcefile.close()
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')
        print "accuracy is "+str(accuracy(classifier, goldfeatset) * 100)
        for line in lines:

            if len(line.split())>2:
                    line = line.replace('  ',' ')
                    words= line.split()
                    feat = bag_of_bigrams_words(words)
                    #decision = classifier.classify(feat)
                    decision = classifier.prob_classify(feat)
        #            print line
        #            print decision.max()


                    if decision.prob('lion') >.99:

                        lionnum+=1
                        files[0].write(line)
                        files[0].write('\n')


                    elif decision.prob('milk') >.99:

                         milknum+=1

                         files[1].write(line)
                         files[1].write('\n')

                    elif decision.prob('tap') >.99:

                        tapnum+=1
                        files[2].write(line)
                        files[2].write('\n')

                    else:


                        sourcefile.write(line)
                        sourcefile.write('\n')
            else:
                pass

        sourcefile.close()

        print str(tapnum)+" instance tagged for tap"
        print str(lionnum)+" instance tagged for lion"
        print str(milknum)+" instance tagged for milk"
        f.close()


for i in range(0,7):
   train_classifier("d:\\hamshir\\")
   apply_classifier('d:\\shirready.txt','d:\\hamshir\\','d:\\hamshirsource' )