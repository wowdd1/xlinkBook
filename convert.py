#!/usr/bin/env python

import getopt
import time
import re
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from utils import Utils
utils = Utils()

source = ''
prefix = 'convert'

def printLine(line):
    line_id = random.randrange(10, 100, 2)
    print prefix + "-" + str(line_id) + " |"  + line.strip() + " | |"


def convert(source):
    f = open(source)
    lines = f.readlines()
    data = ''.join(lines)
    data = utils.clearHtmlTag(data)
    
    for line in data.split('\n'):
        printLine(line)

def main(argv):
    global source
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:', ["input"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:
        if o in ('-i', '--input'):
            source = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source)

if __name__ == '__main__':
    main(sys.argv)
    
