# -*- coding: utf-8 -*-
import codecs
import logging
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

file=codecs.open('d:\\hamshir5.txt','r','utf-8')
texts=[line.split() for line in file.readlines()]


dictionary = corpora.Dictionary.load('d:\\shir.dict')
corpus = corpora.BleiCorpus('d:\\shir.lda-c')
#
#for text in texts:
#    for vec in corpus:
#        print  ' '.join(text)
#        print vec


#for i in  dictionary:
#    c+=1
#    print i, dictionary[i]
#print c
#for vec in corpus:
#    print vec
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#model =models.LsiModel(corpus=corpus_tfidf, id2word=dictionary ,  num_topics=5)
#ldamodel = models.LdaModel(corpus=corpus , num_topics=10)
#model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
model = models.LdaModel(corpus, id2word=dictionary, passes=4, num_topics=5)
#corpus_lsi = model[corpus]
#index = similarities.MatrixSimilarity(model[corpus])
print model.show_topics()

#for num in xrange(model.num_topics):
i=0
#for doc in corpus_lsi:
#    i+=1
#    print doc
#    print ' '.join(texts[i])

#for i in  model.show_topics(topn=20):
#    print i
#    print '............................................'


#doc=u'من این داستان'
#vec_bow = dictionary.doc2bow(doc.split())
#vec_lsi = model[vec_bow] # convert the query to LSI space
#sims = index[vec_lsi] # perform a similarity query against the corpus
#sims = sorted(enumerate(sims), key = lambda item: -item[1])
#print sims
#index = similarities.MatrixSimilarity(lsi[corpus])
##index.save('d:\\example.index')
#index = similarities.MatrixSimilarity.load('d:\\example.index')
#sims = index[vec_lsi] # perform a similarity query against the corpus
#print list(enumerate(sims))