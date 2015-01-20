#!/usr/bin/env python

from utils import Utils, TableHandler
import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup;

keyword = ''
cell_width = 80

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-w, --width: the max width of table cell'

def printTable(keyword):
    if keyword == '':
        return
    utils = Utils()
    url = utils.getUrl(keyword)
    if url == '':
        return
    if url.find('ocw.mit.edu') != -1:
        r = requests.get(url + '/calendar/')
        if r.status_code == 404:
            print 'page not found'
            return
        table = prettytable.from_html(r.text)[2]
        table.align['TOPICS'] = 'l'
        print table
    elif url.find('itunes.apple.com') != -1:
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        table = soup.find('table', class_='tracklist-table content sortable total-flexible-columns-2 total-columns-6')
        parser = TableHandler()
        parser.setMaxCellWidth(cell_width)
        parser.feed(table.prettify().replace('Video', ''))
        parser.tables[0].align["Name"] = "l"
        parser.tables[0].align["Description"] = "l"
        #print parser.tables[0].field_names
        #parser.tables[0].sortby = parser.tables[0].field_names[3]
        #parser.tables[0].reversesort = True
        print parser.tables[0]
    else:
        print 'not suport ' + keyword
        return

def main(argv):
    global keyword, cell_width
    try:
        opts, cmd_args = getopt.getopt(argv[1:], 'hc:w:', ["help","course", "width"])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            keyword = a
        elif o in ('-w', '--width'):
            cell_width = int(a)

    
    printTable(keyword)

if __name__ == '__main__':
    main(sys.argv)
