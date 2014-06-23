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
from classification import MaxVoteClassifier
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
           u'.',u'،',u'؛',u':',u')',u'(',u'_',u'-',u'!',u'؟',u'!!!',u'#',
           u'کرد',u'بود',u'شد',u'برای‌این‌که',u'ـ',u'می‌شود',u'می‌کنند',u'نیز',u'ولی',u'اما',u'?',
           u'#',u'...',u'\"',u'*',u'-',u'#',u'-',u'/',
           u'باشد',u'باشند',u'خود']

#classifier_save_file = open('d:\\classifier.pickle', 'wb')

def precision_recall(classifier, testfeats):
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)

        for i, (feats, label) in enumerate(testfeats):
                refsets[label].add(i)
                observed = classifier.classify(feats)
                testsets[observed].add(i)

        precisions = {}
        recalls = {}
        F_measure = {}

        for label in classifier.labels():
                precisions[label] = metrics.precision(refsets[label], testsets[label])
                recalls[label] = metrics.recall(refsets[label], testsets[label])
                F_measure[label] = metrics.f_measure(refsets[label], testsets[label])

        return precisions, recalls, F_measure

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



def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.raw_freq,n=200):
        match =u"شیر"
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)
        mybigrams=[]

        for item in bigrams:
           if item[0] not in mystoplist and item[1] not in mystoplist:

                  if item[0]==match or item[1]==match:
        
                        mybigrams.append(item)
                    #    print item[0], item[1]
        return bag_of_words(words + mybigrams)

def high_information_words(labelled_words, score_fn=BigramAssocMeasures.raw_freq, min_score=5):
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
          features['tag']= tags[ind]
          for i in range(max(0, ind-5), ind):
                j = ind-i
                features['left-context-word-%s' % j]= words[i][0]

          for i in range(ind+1, min(ind+6, len(words))):
                j = i-ind
                features['right-context-word-%s' % j]= words[i][0]
#                features['right-context-word-%s(%s)' % (j, words[i])] = True
          for i in range(max(0, ind-5), ind):
                        j = ind-i
                        features['left-context-tag-%s' % j]= tags[i][0]

          for i in range(ind+1, min(ind+6, len(words))):
                j = i-ind
                features['right-context-tag-%s' % j]= tags[i][0]
#          if ind<len(words)-1:
#                 features["next word"] = words[ind+1]
#                 features["next tag"] = tags[ind+1]
#          if ind>0:
#                features["prev word"] = words[ind-1]
#                features["prev tag"] = tags[ind-1]
#

       #   print features
    return features

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


def classify(inputdir):
        #filenames = os.listdir('d:\\shir\\')
        filenames = os.listdir(inputdir)

        feat_set = []
        sets = []

        for name in filenames:
        # print name
                labeledlist = []
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
                             words=[]
                             tags=[]
                             tokens = line.split()

                             for item in tokens:
                                   if len(item.split('\\'))==2:
                                        word=item.split('\\')[0]
                                        tag= item.split('\\')[1]
                                        words.append(word)
                                        tags.append(tag)
                                        allwords.append(word)
                             feat_set.append((bag_of_bigrams_words(words),sense))
                            # feat_set.append((context_feature(line),sense))
                      else:
                          words=[]
                          tags=[]
                print lineno
                labeledlist.append((sense,allwords))


#                feat_set.append((bigram_feature(allwords),sense))
                file.close()
        high_info_words = set(high_information_words(labeledlist))
        for item in  high_info_words:
                      print item

        random.shuffle(feat_set)
        random.shuffle(feat_set)
        random.shuffle(feat_set)

        

        train_data = train_feats(feat_set)
        test_data  = test_feats(feat_set)
        print "training on "+str(len(train_data))+" instances"
        print "testting on "+str(len(test_data))+" instances"
        #classifier=  MaxentClassifier.train(train_data)
       # nb_classifier = NaiveBayesClassifier.train(train_data)
        dt_classifier = DecisionTreeClassifier.train(train_data, entropy_cutoff=0.8, depth_cutoff=7, support_cutoff=10)
       # print dt_classifier.pp()
       # pickle.dump(classifier, classifier_save_file)
        entropy_classifier = MaxentClassifier.train(train_data,algorithm='iis', trace=0, max_iter=2, min_lldelta=0.5)
        print "nb accuracy "
       # print accuracy(nb_classifier, test_data) * 100
       # print "nb precision and recall"
#        print precision_recall(nb_classifier,test_data)

    #    print   nb_classifier.show_most_informative_features()
#        for item in  nb_classifier.most_informative_features():
#            print item
     #   print "dt accuracy "+ str(accuracy(dt_classifier, test_data) * 100)
        print "entropy accuracy "+ str(accuracy(entropy_classifier, test_data) * 100)
#        mv_classifier = MaxVoteClassifier(nb_classifier, dt_classifier, entropy_classifier)
#        print "max vote accuracy "+ str(accuracy(mv_classifier, test_data) * 100)


classify("d:\\shir\\")

  