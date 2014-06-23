# -*- coding: utf-8 -*-
import codecs
import xml.etree.ElementTree as xml
#file=codecs.open('d:\\shirpos.txt','r','utf-8')
#outfile = open("d:/test.xml", 'w')
#root_element = xml.Element("sentences")
#for line in file:
#
#
#  child = xml.SubElement(root_element, "sentence")
#  child.text = line
##child = xml.SubElement(root_element, "instance2")
##child.text = "asasasasass"
#xml.ElementTree(root_element).write(outfile,encoding='utf-8',)
#
##Close the file like a good programmer
#file.close()
#outfile.close()

#Parse XML directly from the file path
tree = xml.parse("d:/test.xml")
#
##Get the root node
#rootElement = tree.getroot()
#
##Get a list of children elements with tag == "Books"
#bookList = rootElem.findall("Books")
#
##Check if any "Books" were found
#if bookList != None:
#    for book in bookList:
#        #Do something with your book!