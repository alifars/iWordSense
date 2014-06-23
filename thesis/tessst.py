# -*- coding: utf-8 -*-

import codecs

file = codecs.open("d:\\hamshir\\lion.txt","r","utf-8")
#outfile = codecs.open("d:\\hamshircopy.txt","w","utf-8")
match =u'شیر'
matchnum=0
for line in file:

             if match in line.split():
                 matchnum+=1

#    outfile.write(line)
#    outfile.write('\n')
  
print matchnum
file.close()
#outfile.close()