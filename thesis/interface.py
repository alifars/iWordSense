
# -*- coding: utf-8 -*-
import os

import nltk, nltk.corpus,codecs
import pyodbc
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import XMLCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.metrics.association import BigramAssocMeasures
import wx
import cStringIO



mystoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش',
           u'شد',
           u'اگر']

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

def bigram_finder(words, score_fn=BigramAssocMeasures.raw_freq,n=200):

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
   return mybigrams



class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour((237,237,237))
#        box = wx.BoxSizer(wx.HORIZONTAL)
#        box.Add(wx.Button(panel, -1, 'Button1'), 1, wx.ALL, 5)

        button = wx.Button(panel, label=u"خروج", pos=(400, 500))
        button2 = wx.Button(panel, label=u"نمایش همایندی ها", pos=(550, 400))


        wx.StaticText(panel, -1,u"کلمه هدف را وارد کنید",(650,60))
        self.text = wx.TextCtrl(panel, -1,pos=(530, 60),style=wx.TE_RIGHT)

        self.text2 = wx.StaticText(panel, pos=(100,40), label=u"جمله حاوی کلمه هدف را وارد کنید")
        button3 = wx.Button(panel,label=u"رفع ابهام", pos=(150, 400))
        
        self.text3 = wx.TextCtrl(panel, -1,pos=(50, 60),size=(300,20),style=wx.TE_RIGHT)

        self.printlabel = wx.StaticText(panel, pos=(220,200), label=u"شماره بهترین معانی کلمه")
        self.printarea = wx.TextCtrl(panel, -1,size=(250,100),pos=(100, 100),style=wx.TE_MULTILINE|wx.TE_RIGHT)

        self.sensearea=wx.TextCtrl(panel, -1,size=(390,270),pos=(400, 100),style=wx.TE_MULTILINE|wx.TE_RIGHT)
        self.word = self.text.GetValue()
        

        button4 = wx.Button(panel,label=u"پاک کردن", pos=(300, 500))


        self.Bind(wx.EVT_BUTTON, self.Clear, button4)
        self.Bind(wx.EVT_BUTTON, self.OnClose, button)
        self.Bind(wx.EVT_BUTTON, self.ShowSenses, button2)
        self.Bind(wx.EVT_BUTTON, self.SearchCorpus, button3)
        self.Show(True)

    def OnClose(self, event):
              self.Destroy()
    def Clear(self, event):
         self.printarea.Clear()
         self.sensearea.Clear()
         self.text.Clear()
         self.text3.Clear()


    def ShowSenses(self, event):

        filenames = os.listdir('d:\\shir\\')
        dir = 'd:\\shir'
        feat_set = []
        sets = []
        allwords = []
        for name in filenames:
        # print name
            lineno=0
            path = os.path.join(dir, name)
            sense = name.split('\\')[-1].split('.')[0]
            print 'training', sense

            file = codecs.open(path, 'r', 'utf-8')

            for line in file:
              if len(line.split())!=0:
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
        for item in  bigram_finder(allwords):
              self.sensearea.WriteText(item[0]+item[1])
              self.sensearea.WriteText("/\n")
        return bigram_finder(allwords)
           # print item[1]#,item[2]
    def SearchCorpus(self, event):
        sent = self.text3.GetValue()
        count=0
        overlap[senseid]=len(common)
                        

        




app = wx.App(False)
frame = MyFrame(None,u'اولین برچسب زن معنایی--دانشگاه صنعتی شریف-پروژه روانشناسی زبان')


app.MainLoop()

