#!/usr/bin/env python

import os
import sys
import getopt
from utils import Utils


def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-c,--course: the course number'
    print '-u, --use: seach in what subject'   

def print_course(course_num, subject):
    util = Utils()
    record_list = util.getRecord(course_num, use_subject=subject, return_all=True)
    if record_list == None:
        return
    for record in record_list: 
        if record.get_id().strip() != '':
            os.system("./list.py -i " + record.get_path() + " -c 1 -f '^" + course_num + "' -d -r 10")

def main(argv):
    use_subject = ''
    course = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:u:', ["help", "course", "use"])
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
            course = str(a)
        elif o in ('-u', '--use'):
            use_subject = str(a)

        print_course(course, use_subject)
if __name__ == '__main__':
    main(sys.argv)
