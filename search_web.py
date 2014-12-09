#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser
import utils

engin = ""
keyword = ""
google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
baidu = "http://www.baidu.com/s?word="
bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="

search_engin_list = [google, baidu, bing, yahoo]

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-s, --search: the keyword for search the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print 'ex: ' + argv0 + ' -s "cs199"'

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
    print 'searching , %s'%keyword
    urls = []
    url = ""
    for url_file in utils.find_file_by_pattern(".urls", os.getcwd() + "/db/"):
        f = open(url_file)
        for line in f.readlines():
            if line.startswith(keyword):
                print "found " + line
                pos = line.find("http")
                title = line[line.find("|", pos) + 1 :].strip()
                if engin != "" and validEngin(engin) == True:
                   for item in search_engin_list:
                       if item.lower().find(engin.lower()) != -1:
                           urls.append(item + title)
                else:
                    urls.append(line[pos:line.find("|",pos)].strip().lower())
                
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
        print "no url found in db"
        return
    
    openBrowser(url)

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hs:e:', [])
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

    if keyword != "":
        search(keyword, engin) 
             

if __name__ == '__main__':
    main(sys.argv)
