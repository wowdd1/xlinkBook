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

engin = ""
keyword = ""
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
def search(keyword, engin):
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
            if line.lower().startswith(keyword.lower()):
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
            if url == "":
                url = urls[0]
    elif len(urls) == 1:
        url = urls[0]
    else:
        print "no url found in " + subject +" db"
        return
    
    openBrowser(url)

def main(argv):
    global keyword
    try:
        opts, args = getopt.getopt(argv[1:], 'hs:e:u:', ["help","search","engin","use"])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-s', '--search'):
            keyword = a
        elif o in ('-e', '--engin'):
            global engin
            engin = a
        elif o in ('-u', '--use'):
            global use_subject
            use_subject = str(a)
           
    if keyword != "":
        search(keyword, engin) 
             

if __name__ == '__main__':
    main(sys.argv)
