# -*- coding: utf-8 -*-
import xml.dom.minidom
import xml.etree.ElementTree as xml
import os, codecs

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



xmlfile = open("d:/test.xml", 'w')

root = xml.Element('corpus')
#root = xml.Element('word2')
count=0
match=u'شیر'
sent=[]
tagseq=[]
wordsent=[]
results=[]
alltags={}


stoplist=[u'و',u'به',u'از',u'در',u'بر',u'را',u'با',u'که',u'های',u'می',u'یا',u'برای',
           u'است',u'تا',u'آن',u'دارد',u'شود',u'او',u'ها',u'هم',u'شده',u'کند',u'من',u'ای',u'هر',
           u'کنند',u'کند','دهند','اگر',u'آنها',u'دهند',u'اش', u'شد', u'اگر',u'.',u'،',u'این',u'اینها',
           u'.',u'،',u'؛',u':',u')',u'(',u'_',u'-',u'!',u'؟'
           u'کرد',u'بود',u'شد',u'برای‌این‌که',u'ـ',u'می‌شود',u'می‌کنند',u'نیز',u'ولی',u'اما',u'?',
           u'#',u'...',u'\"',u'*',u'-',
           u'باشد',u'باشند',u'خود']



punclist=['.','،','؛',':',',']
linecount=0

dir = 'd:\\bijcorpus'
#outdir = 'd:\\bijfile'
names = os.listdir(dir)
c =0
linec=0
fileno=0
for name in names:
#    c+=1
    path = os.path.join(dir,name)
    print path
#
#
    file = codecs.open(path,'r','utf-8')
    fileno+=1
    while fileno<2:
      for line in file:
         linec+=1
        # print line
         word=''
         tag=''
         pureline=correctPersianString(line)
         items = pureline.split()
         leng = len(pureline.split())
         if leng == 5:
             word = items[-1]
             tag =  items[2]
             shorttag = items[-3]
             #print shorttag
         elif leng>5:
             newitems= items[4:]
             word = u'\u200c'.join(newitems)
             tag = items[2]

         wordtag=word+"\\"+tag
         #if word not in stoplist:
             #print word
         wordsent.append(word)
         tagseq.append(tag)
         sent.append((word,tag))
    #
    #
         if word=='.':

               # print ' '.join(wordsent)
                #print
                instance = xml.Element('instance')
                root.append(instance)
                instance.attrib['POS'] = ' '.join(wordsent)
                sent=[]
                tagseq=[]
                wordsent=[]

    file.close()
#for num in range(10) :
##Create a child element
#  instance = xml.Element('instance')
#  root.append(instance)
xml.ElementTree(root).write(file)

#This is how you set an attribute on an element
#pos.attrib['POS'] = u"شیر"

#Now lets write it to an .xml file on the hard drive

#Open a file


#Create an ElementTree object from the root element


#Close the file like a good programmer
xmlfile.close()