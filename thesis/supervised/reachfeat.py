# -*- coding: utf-8 -*-
from _collections import defaultdict
import os
import random

import codecs, glob, nt
import nltk

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify import NaiveBayesClassifier
from nltk.classify import DecisionTreeClassifier
from nltk.classify.util import accuracy
import sys


def bag_of_words(line):
    words=[]
    for item in line.split():
        words.append(item.split('\\')[0])
    return dict([(word, True) for word in words])


def get_feature(word):
    return dict([(word, True)])


def extract_words(text):
    match = u'شیر'

    tokens = text.split()
    nudetokens = []
    for token in tokens:
         word=token.split('\\')[0]

         nudetokens.append(word)

    result = [x for x in nudetokens]
    for i in  result:
            print i
    return result


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

filenames = os.listdir('d:\\shir\\')
dir = 'd:\\shir'
feat_set = []
sets = []
for name in filenames:
# print name

    path = os.path.join(dir, name)
    sense = name.split('\\')[-1].split('.')[0]
    print 'training', sense
    file = codecs.open(path, 'r', 'utf-8')
    #text = file.read()
    for line in file:
      if len(line.split())!=0:
             line = line.strip()
            # feat_set.append((get_feature2(line), sense))
             feat_set.append((bag_of_words(line), sense))

for item in feat_set:
    print item
random.shuffle(feat_set)
random.shuffle(feat_set)
##print feat_set
#for item in feat_set:
#    print item
def train_feats(feat_set):
    train_feats = []
    trainlen = int(.25 * len(feat_set))
    for item in feat_set[trainlen:]:
        train_feats.append(item)

    #        print i
    return train_feats


def test_feats(feat_set):
    test_feats = []
    trainlen = int(0.25 * len(feat_set))
    # print trainlen
    for item in feat_set[:trainlen]:
        test_feats.append(item)

    return test_feats

train = train_feats(feat_set)
test = test_feats(feat_set)
classifier = NaiveBayesClassifier.train(train)
#classifier = DecisionTreeClassifier.train(train)
#classifier = nltk.classify.WekaClassifier.train(train,classifier='naivebayes',quiet=False)

print accuracy(classifier, test) * 100
#classifier.show_most_informative_features()
#for i in  classifier.most_informative_features():
 #   print i[0],i[1]
match = u'شیر'
#file = codecs.open('d:\\other.txt', 'r', 'utf-8')
#for line in file:
#
#    if match  in line.split():
#       # print line
#
#        tokens = bag_of_words(extract_words(line))
#        decision = classifier.prob_classify(tokens)
#        #decision = classifier.classify(tokens)
#
#        #result = "%s - %s" % (decision, line )
#        print line,decision.max()
##        #if decision=='lion':
##        #         milkfile.write(line)
##        #         milkfile.write('\n')
#        if decision.prob('tap') > .9:
#            print line

file.close()