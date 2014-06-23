# -*- coding: utf-8 -*-
import os
import pickle

import nltk, nltk.corpus,codecs,re
from nltk.collocations import BigramCollocationFinder

from nltk.corpus import XMLCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import TaggedCorpusReader
from nltk.metrics.association import BigramAssocMeasures

print 'system loading !!!'
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
punclist = [u'،',u'-',u'(',u')',u'؛',u'[',u']',u'*']


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

def bigram_finder(filepath):
   file = codecs.open(filepath,'r','utf-8')
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



count=0



def hamshahri_targetword_corpus_maker(match, outpath):
        print 'loading hamshahri corpus'
        print
        corpus = LazyCorpusLoader('hamshahricorpus',XMLCorpusReader, r'(?!\.).*\.xml')
        outfile=codecs.open(outpath,'w','utf-8')
        punclist=[u'،',u'؛',u':',u'؟',u'#']

        matchnum=0
        count =0
        print 'creating target corpus'
        for file in corpus.fileids():
            #print file

            for doc in  corpus.xml(file).getchildren():

            #    print doc.getchildren()
        #          cat=doc.getchildren()[3].text#
                  text=doc.getchildren()[5].text
                  newtext=correctPersianString(text)
                  newtext= newtext.replace('\n',' ')


                  for item in punclist:
                        if item in newtext:
                            newtext=newtext.replace(item,'')
        #
        #        #  print newtext
        #
        #
                  if match in newtext.split():
        #
                        matchnum+=1
                        print newtext
                        print '#'
                        count+=1
        #
                        outfile.write(newtext)
                        outfile.write('ALI')


        outfile.close()
        print count

def seed_maker(targetword,coloclist, sourcepath,outdir, sense):
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

        sense = sense+".txt"
        seedpath = os.path.join(outdir, sense)
        seedfile = codecs.open(seedpath, 'w', 'utf-8')
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        sourcetext = sourcefile.read()
        sourcefile.close()
        sourcenews = sourcetext.split('ALI')
        for news in sourcenews:

                   lines = news.split('.')
                   noitemfound = True
                   for item in coloclist:

                         if item  in  news:
                             noitemfound = False


                   for item in coloclist:
                       if item in news:
                            for line in lines:
                                if item in line:
                                        seedfile.write(line)
                                        seedfile.write('\n')
                                        seedfile.write('\n')
                                if item not in line and targetword in line:
                                        seedfile.write(line)
                                        seedfile.write('\n')
                                        seedfile.write('\n')


                   if noitemfound:
                           unwanted.append(news)

        print str(instancenum)+" of target word found in corpus"
        print str(matchnum)+" found in corpus for "+ sense
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')
        for news in unwanted:

            sourcefile.write(news)
            sourcefile.write('ALI')

        sourcefile.close()
        seedfile.close()



def corpus_convert(match,sourcepath,outpath):
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        outfile = codecs.open(outpath, 'w', 'utf-8')
        sourcetext = sourcefile.read()
        sourcefile.close()
        sourcenews = sourcetext.split('ALI')
        for news in sourcenews:
             lines = news.split('.')
             for line in lines:
                 if match in line.split():
                         outfile.write(line)
                         outfile.write('\n')
                         outfile.write('\n')

def google_search(targetword, itemlist,targetpath):
    resultnum=0
    engine = Google(license=None)
    file = codecs.open(targetpath,'a','utf-8')
    outtext= ''
    patt = ur'\W+'
    for item in itemlist:
        for i in range(1,5):
            for result in engine.search(item, type=SEARCH, start=i):

                  url = URL(result.url)
                  text = url.download(unicode=True)

                  text = plaintext(text)
                  text = correctPersianString(text)
                  text = text.replace('\n',' ')
                  lines = text.split('.')
                  for line in lines:
                      if targetword in line:

                              match = re.findall(patt,line)
                              output =  ' '.join(match)

                              for item in punclist:
                                  if item in line:
                                      line = line.replace(item,' ')

                              print output
                              file.write(output)
                              file.write('\n')
    print str(resultnum)+" found in web"
    file.close()

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
        print "applying classifier"
        classifier = pickle.load(f)
        print "classifier labels:"
        labels = classifier.labels()

        paths = []
        files=[]
        lines=[]
        goldfeatset = []
        tapnum, lionnum,milknum=0,0,0
        print "reading from "+str(inputdir)
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
        filenames = os.listdir(inputdir)
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
                  #  for name in paths:

#                    if decision.prob('lion') >.99:
#
#                        lionnum+=1
#                        files[0].write(line)
#                        files[0].write('\n')
#
#
#                    elif decision.prob('milk') >.99:
#
#                         milknum+=1
#
#                         files[1].write(line)
#                         files[1].write('\n')
#
#                    elif decision.prob('tap') >.99:
#
#                        tapnum+=1
#                        files[2].write(line)
#                        files[2].write('\n')
#
#                    else:
#
#
#                        sourcefile.write(line)
#                        sourcefile.write('\n')
#            else:
#                pass

        sourcefile.close()

        print str(tapnum)+" instance tagged for tap"
        print str(lionnum)+" instance tagged for lion"
        print str(milknum)+" instance tagged for milk"
        f.close()


#hamshahri_targetword_corpus_maker(u'شانه','d:\\shane.txt')