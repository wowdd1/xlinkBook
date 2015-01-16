#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser
from utils import Utils
from update.all_subject import default_subject, print_all_subject
from record import Record
import prettytable
from prettytable import PrettyTable
import requests
import sys
from bs4 import BeautifulSoup;

py3k = sys.version_info[0] >= 3
if py3k:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser

class TableHandler(HTMLParser):

    def __init__(self, **kwargs):
        HTMLParser.__init__(self)
        self.kwargs = kwargs
        self.tables = []
        self.last_row = []
        self.rows = []
        self.max_row_width = 0
        self.active = None
        self.last_content = ""
        self.is_last_row_header = False

    def setMaxCellWidth(self, width):
        self.max_cell_width = width

    def handle_starttag(self,tag, attrs):
        self.active = tag
        if tag == "th":
            self.is_last_row_header = True

    def handle_endtag(self,tag):
        if tag in ["th", "td"]:
            stripped_content = self.last_content.strip()[0 : self.max_cell_width]
            self.last_row.append(stripped_content)
        if tag == "tr":
            self.rows.append(
                (self.last_row, self.is_last_row_header))
            self.max_row_width = max(self.max_row_width, len(self.last_row))
            self.last_row = []
            self.is_last_row_header = False
        if tag == "table":
            table = self.generate_table(self.rows)
            self.tables.append(table)
            self.rows = []
        if tag == "span":
            return
        self.last_content = " "
        self.active = None
    def handle_data(self, data):
        self.last_content += data

    def generate_table(self, rows):
        """
        Generates from a list of rows a PrettyTable object.
        """
        table = PrettyTable(**self.kwargs)
        for row in self.rows:
            if len(row[0]) < self.max_row_width:
                appends = self.max_row_width - len(row[0])
                for i in range(1,appends):
                    row[0].append("-")

            if row[1] == True:
                self.make_fields_unique(row[0])
                table.field_names = row[0]
            else:
                table.add_row(row[0])
        return table

    def make_fields_unique(self, fields):
        """
        iterates over the row and make each field unique
        """
        for i in range(0, len(fields)):
            for j in range(i+1, len(fields)):
                if fields[i] == fields[j]:
                    fields[j] += "'"


engin = ""
keyword = ""
print_table = False
cell_width = 100
google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
baidu = "http://www.baidu.com/s?word="
bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="

search_engin_list = [google, baidu, bing, yahoo]
use_subject = ""
def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-s, --search: the keyword for search the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print '-u, --use: seach in what subject'
    print '-p, --print: print the course table local'
    print '-w, --width: the max width of table cell'
    print "subject include:"
    print_all_subject()
    print 'ex: ' + argv0 + ' -s "cs199" -u eecs'

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)
    

def validEngin(engin):
    for item in search_engin_list:
        if item.lower().find(engin.lower()) != -1:
            return True
    print "invalided search engin: " + engin
    return False

def getUrl(keyword):
    urls = []
    url = ""
    subject = default_subject;
    if use_subject != "":
        subject = use_subject
    print 'searching %s'%keyword + " in " + subject

    utils = Utils()
    for file_name in utils.find_file_by_pattern(".*", os.getcwd() + "/db/" + subject + "/"):
        f = open(file_name)
        for line in f.readlines():
            record = Record(line)
            if record.get_id().lower().strip() == keyword.lower().strip():
                print "found " + line.replace("|","")
                record = Record(line)
                title = record.get_title().strip()
                if engin != "" and validEngin(engin) == True:
                   for item in search_engin_list:
                       if item.lower().find(engin.lower()) != -1:
                           urls.append(item + title)
                else:
                    urls.append(record.get_url().strip().lower())

        f.close()


    if len(urls) > 1:
        for u in urls:
            if u.find("google.com") == -1 and u.find("baidu.com") == -1 \
              and u.find("bing.com") == -1 and u.find("yahoo.com") == -1:
                url = u
                break
            if url == "":
                url = urls[0]
    elif len(urls) == 1:
        url = urls[0]
    else:
        print "no url found in " + subject +" db"

    return url

def printTable(keyword):
    url = getUrl(keyword)
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
        print parser.tables[0]
    else:
        print 'not suport ' + keyword 
        return
   

def search(keyword, engin):
    url = getUrl(keyword) 
    if url != '':
        openBrowser(url)

def main(argv):
    global keyword, print_table, cell_width, engin
    try:
        opts, args = getopt.getopt(argv[1:], 'hs:e:u:p:w:', ["help","search","engin","use", "print", "width"])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-s', '--search'):
            keyword = a
        elif o in ('-p', '--print'):
            keyword = a
            print_table = True
        elif o in ('-w', '--width'):
            cell_width = int(a)
        elif o in ('-e', '--engin'):
            engin = a
        elif o in ('-u', '--use'):
            global use_subject
            use_subject = str(a)
           
    if keyword != "":
        if print_table:
            printTable(keyword)    
        else:
            search(keyword, engin) 
             

if __name__ == '__main__':
    main(sys.argv)
