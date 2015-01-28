#!/usr/bin/env python

from utils import Utils, TableHandler
import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup;
import prettytable
import webbrowser

course = ''
lecture = ''
cell_width = 80

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c,--course: the course.'
    print '-l,--lecture: the lecture id of the course.'
    print '-w, --width: the max width of table cell'

def printCourseTable(course):
    if course == '':
        return
    utils = Utils()
    url = utils.getUrl(course)
    if url == '':
        return
    if url.find('ocw.mit.edu') != -1:
        r = requests.get(url + '/calendar/')
        if r.status_code == 404:
            print 'page not found'
            return
        #table = prettytable.from_html(r.text)[2]
        for table in prettytable.from_html(r.text):
            if table.field_names[0] == 'Field 1':
                continue
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
        print 'not suport ' + course
        return

def getMediaUrl(url):
    r = requests.get(url)
    #print r.text
    media_url = r.text[r.text.find('>http') + 1 : r.text.find('</', r.text.find('>http'))]
    print 'the media url is:' 
    print media_url
    return media_url

def showLecture(course, lecture):
    utils = Utils()
    url = utils.getUrl(course)
    if url == '':
        return
    if url.find('itunes.apple.com') != -1:
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all('tr', attrs={"kind": "movie"}):
            if tr.td != None and tr.td.text.strip() == lecture:
                pos = tr.prettify().find('https://itunes.apple.com')
                start = tr.prettify().find('i=', pos) + 2
                end = tr.prettify().find('&', pos)
                webbrowser.open(getMediaUrl('https://itunes.apple.com/WebObjects/DZR.woa/wa/downloadTrack/ext.mp4?id=' + tr.prettify()[start : end].strip()))
                return

        print 'not found'
        

def main(argv):
    global course, lecture, cell_width
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:l:w:', ["help","course", "lecture", "width"])
        if len(args) == 1:
            course = args[0]
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            course = str(a)
        elif o in ('-l', '--lecture'):
            lecture = str(a)            
        elif o in ('-w', '--width'):
            cell_width = int(a)

    if course != '' and lecture != '':
        showLecture(course, lecture)
    else: 
        printCourseTable(course)

if __name__ == '__main__':
    main(sys.argv)
