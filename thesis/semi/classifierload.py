import codecs
import os
import pickle

def bag_of_words(line):
    words=[]
    for item in line.split():
        words.append(item.split('\\')[0])
    return dict([(word, True) for word in words])


f= open('d:\\seed_classifier.pickle')
classifier = pickle.load(f)
print "classifier labels"
print classifier.labels()



def apply_classifier(sourcepath,inputdir):
        filenames = os.listdir(inputdir)
        paths = []
        files=[]
        print
        for name in filenames:

            path = os.path.join(inputdir, name)
            file= codecs.open(path, 'a', 'utf-8')
            files.append(file)
            paths.append(path)
        print files
        sourcefile = codecs.open(sourcepath, 'r', 'utf-8')
        lines = sourcefile.readlines()
        for line in lines:

            if len(line.split())>2:
                    feat = bag_of_words(line)
                    #decision = classifier.classify(feat)
                    decision = classifier.prob_classify(feat)
        #            print line
        #            print decision.max()


                    if decision.prob('lion') >.99:

                        files[0].write(line)
                        lines.remove(line)
                    if decision.prob('milk') >.99:

                         files[1].write(line)
                         lines.remove(line)
                    if decision.prob('tap') >.99:


                        files[2].write(line)
                        lines.remove(line)

            else:
                pass
             #   lines.remove(line)
        sourcefile.close()
        sourcefile = codecs.open(sourcepath, 'w', 'utf-8')
        for line in lines:
            sourcefile.write(line)
            sourcefile.write('\n')


        f.close()
        sourcefile.close()

