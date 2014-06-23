# -*- coding: utf-8 -*-
import collections
import os
import pickle
import random

import codecs, glob, nt
from nltk import metrics
import nltk
from nltk.classify.maxent import MaxentClassifier
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
           u'.',u'،',u'؛',u':',u')',u'(',u'_',u'-',u'!',u'؟'
           u'کرد',u'بود',u'شد',u'برای‌این‌که',u'ـ',u'می‌شود',u'می‌کنند',u'نیز',u'ولی',u'اما',u'?',
           u'#',u'...',u'\"',u'*',u'-',
           u'باشد',u'باشند',u'خود']

classifier_save_file = open('d:\\classifier.pickle', 'wb')

def bag_of_words(line):
    words=[]
    for item in line.split():
        words.append(item.split('\\')[0])
    return dict([(word, True) for word in words])

def bag_of_Nostopword(words):
    purewords=[]
    for word in words:
        if word in mystoplist:
           # print word
            pass
        else:
            purewords.append(word)

    return dict([(word, True) for word in purewords])

def bigram_finder(words, score_fn=BigramAssocMeasures.raw_freq,n=200):
   match = "شیر"
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
   return bag_of_words(mybigrams)

def get_feature2(line):
    match=u'شیر'
    features = {}
    tokens=line.split()
    words=[]
    tags=[]

    for item in tokens:
       if len(item.split('\\'))==2:
            word=item.split('\\')[0]
            tag= item.split('\\')[1]
            words.append(word)
            tags.append(tag)
#    for i in range(len(tags)):
#        print words[i],tags[i]

    if match in words:
        ind = words.index(match)

        features["next word"] = words[ind+1]
       # features["two next word"] = words[ind+2]
        features["prev word"] = words[ind-1]
      #  features["two prev word"] = words[ind-2]
        features["prev tag"] = tags[ind-1]
        features["next tag"] = tags[ind+1]

##    for letter in 'abcdefghijklmnopqrstuvwxyz':
##        features["count(%s)" % letter] = name.lower().count(letter)
##        features["has(%s)" % letter] = (letter in name.lower())
    return features

def train_feats(myset):
    train_feats = []
    trainlen = int(.15 * len(myset))
    for item in myset[trainlen:]:
        train_feats.append(item)

    #        print i
    return train_feats

#
def test_feats(myset):
    test_feats = []
    trainlen = int(.15 * len(myset))
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
                     feat_set.append((bag_of_words(line),sense))
                     #feat_set.append((get_feature2(line),sense))
              else:
                  words=[]
                  tags=[]
            file.close()

        random.shuffle(feat_set)
        random.shuffle(feat_set)
        #random.shuffle(feat_set)



        train_data = train_feats(feat_set)
        test_data  = test_feats(feat_set)
        #classifier=  MaxentClassifier.train(train_data)
        nb_classifier = NaiveBayesClassifier.train(train_data)
        dt_classifier = DecisionTreeClassifier.train(train_data, entropy_cutoff=0.8, depth_cutoff=5, support_cutoff=30)
       # pickle.dump(classifier, classifier_save_file)
        entropy_classifier = MaxentClassifier.train(train_data,algorithm='iis', trace=0, max_iter=1, min_lldelta=0.5)
        print "nb accuracy "+ str(accuracy(nb_classifier, test_data) * 100)
        print "dt accuracy "+ str(accuracy(dt_classifier, test_data) * 100)
        print "entropy accuracy "+ str(accuracy(entropy_classifier, test_data) * 100)
        mv_classifier = MaxVoteClassifier(nb_classifier, dt_classifier, entropy_classifier)
        print "max vote accuracy "+ str(accuracy(mv_classifier, test_data) * 100)


classify("d:\\shir\\")

classifier_save_file.close()
##classifier = MaxentClassifier.train(train)
###classifier = DecisionTreeClassifier.train(train_feats,binary=True, entropy_cutoff=0.8, depth_cutoff=5, support_cutoff=30)
##classifier = DecisionTreeClassifier.train(train_data)
#print classifier.labels()
      #def precision_recall(classifier, testfeats):
        #    refsets = collections.defaultdict(set)
        #    testsets = collections.defaultdict(set)
        #    for i, (feats, label) in enumerate(testfeats):
        #          refsets[label].add(i)
        #          observed = classifier.classify(feats)
        #          testsets[observed].add(i)
        #    precisions = {}
        #    recalls = {}
        #    for label in classifier.labels():
        #        precisions[label] = metrics.precision(refsets[label],testsets[label])
        #        recalls[label] = metrics.recall(refsets[label], testsets[label])
        #    return precisions, recalls

##print "precisions "
#print precision_recall(classifier,test)[0]
#print "recalls "
#print precision_recall(classifier,test)[1]
#for item in  classifier.most_informative_features(n=10):
#    print item[0]
##classifier.show_most_informative_features()
#    print i
match = u'شانه'
#file = codecs.open('d:\\hamshane.txt', 'r', 'utf-8')
#for line in file:
#    set =[]
#    if match  in line.split():
#        print line
##
#        tokens = extract_vocab(line)
#        set = set + [get_feature(word) for word in line.split()]
#        decision = classifier.prob_classify(set)
##
##        result = "%s - %s" % (decision, line )
#        print decision
###        #if decision=='lion':
###        #         milkfile.write(line)
###        #         milkfile.write('\n')
##        if decision.prob('milk') > .9:
##            print line

