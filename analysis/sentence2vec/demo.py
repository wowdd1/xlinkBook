#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


"""

"""

import logging
import sys
import os
from word2vec import Word2Vec, Sent2Vec, LineSentence

import getopt

logging.basicConfig(format='%(message)s', level=logging.INFO)
course = " ".join(sys.argv)
if (course.find("-c") != -1):
    course = course[course.find("-c") + 2 :].strip()
else:
    course = ""

#logging.info(course)

#logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
#logging.info("running %s" % " ".join(sys.argv))

path = "/Users/zd/dev/python/course_env/random_walk/analysis/sentence2vec"
input_file = path + '/test.txt'
'''
model = Word2Vec(LineSentence(input_file), size=100, window=5, sg=0, min_count=5, workers=8)
model.save(input_file + '.model')
model.save_word2vec_format(input_file + '.vec')
'''

sent_file = path + '/sent.txt'

if course != "":
    f = open(sent_file + ".tmp", "a")
    f.write(course + "\n")

    f1 = open(sent_file,'rU')
    f.write("".join(line for line in f1.readlines()))
    sent_file = sent_file + ".tmp"

model = Sent2Vec(LineSentence(sent_file), model_file=input_file + '.model')

if course != "":
    os.remove(sent_file)
#model.save_sent2vec_format(sent_file + '.vec')
#model.save(sent_file + '.model')

#program = os.path.basename(sys.argv[0])
#logging.info("finished running %s" % program)


#model = Sent2Vec.load(sent_file + '.model')
#print len(model.sents)
result = {}
for i in range(0, len(model.sents)):
    #logging.info((str(model.similarity(0, i)) + "  " + model.sentences[str(i)]))
    result[str(model.similarity(0, i))] = model.sentences[str(i)]


#print len(result.keys())
logging.info("similarity data:")
for k, v in [(k,result[k]) for k in sorted(result.keys(), reverse = True)]:
    #print float(k)
    if (float(k) > 0.8 and float(k) < 1):
        #print k + " " + v
        logging.info("      " + v)
