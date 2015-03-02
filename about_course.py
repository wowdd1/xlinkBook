#!/usr/bin/env python

import os
import sys
import getopt
from utils import Utils


def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-c,--course: the course number'

def print_course(course_num):
    util = Utils()
    record_list = util.getRecord(course_num, return_all=True)
    if record_list == None:
        return
    for record in record_list: 
        if record.get_id().strip() != '':
            os.system("./list.py -i " + record.get_path() + " -c 1 -f '^" + course_num + "' -d -r 10")

def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:', ["help", "course"])
        if len(args) == 1:
            print_course(args[0])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-c', '--course'):
            print_course(a)

if __name__ == '__main__':
    main(sys.argv)
