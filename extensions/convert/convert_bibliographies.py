#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
import bibtexparser



def convert(source, crossrefQuery=''):

    r = requests.get(source)

    bibText = r.text.encode('utf-8')


    if True:

        author = ''
        title = ''
        year = ''
        for line in bibText.split('\n'):
            if line.strip() == '':
                continue

            if line.find(' author =') != -1:
                author = line.strip()
                author = author[author.find('{') + 1 : author.rfind('}')].strip().replace(' and ', ', ')

            if line.find(' year =') != -1:
                year = line.strip()
                year = year[year.find('{') + 1 : year.rfind('}')].strip()
                year = 'description:' + year


            if line.find(' title =') != -1:
                title = line.strip()
                title = title[title.find('{') + 1 : title.rfind('}')].strip()

                print ' | ' + title + ' | | ' + ' author:'+ author + ' ' + year

                title = ''
                author = ''
                year = ''

    else:

        f = open('web_content/bib', 'w+')

        f.write(bibText)

        f.close()

        f = open('web_content/bib', 'r')

        bib_database = bibtexparser.load(f)

        for entry in bib_database.entries:
            desc = ''
            if entry.has_key('year'):
                desc = 'description:' + entry['year']
            line = ' | ' + entry['title'] + ' |  | author:' + entry['author'] + ' ' + desc 
            print line.encode('utf-8')

    
def main(argv):
    source = ''
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:', ["url", "crossrefQuery"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    