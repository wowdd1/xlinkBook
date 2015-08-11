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


path = "/Users/zd/dev/python/course_env/random_walk/analysis/sentence2vec"
input_file = path + '/course.txt'
sent_file = path + '/course.txt'

data = { 'course.txt'} #, 'paper.txt'}

for txt in data:

    sent_file = path + "/" + txt
    tmp_file = path + "/" + txt + ".tmp"
    mod_file = path + "/" + txt + ".model"
    if course != "":
        f = open(tmp_file, "a")
        f.write(course + "\n")

        f1 = open(sent_file,'rU')
        f.write("".join(line for line in f1.readlines()))

    model = Sent2Vec(LineSentence(tmp_file), model_file=mod_file)

    if course != "":
        os.remove(tmp_file)

    result = {}
    for i in range(0, len(model.sents)):
        result[str(model.similarity(0, i))] = model.sentences[str(i)]


    logging.info("similarity data:")
    for k, v in [(k,result[k]) for k in sorted(result.keys(), reverse = True)]:
        if (float(k) > 0.8 and float(k) < 1):
            logging.info("      " + v)
