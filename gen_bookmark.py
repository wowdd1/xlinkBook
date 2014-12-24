#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import random
import time
import getopt
import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
from utils import Utils
from update.all_subject import default_subject
from record import Record

bookmark_start = '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n\
<!-- This is an automatically generated file.\n\
     It will be read and overwritten.\n\
     DO NOT EDIT! -->\n\
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n\
<TITLE>Bookmarks</TITLE>\n\
<H1>Bookmarks</H1>\n\
<DL><p>\n\
    <DT><H3 ADD_DATE="" LAST_MODIFIED="" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Bar</H3>\n\
    <DL><p>\n\
        <DT><H3 ADD_DATE="" LAST_MODIFIED="">course</H3>\n\
        <DL><p>\n'
bookmark_end = '        </DL><p>\n\
    </DL><p>\n\
</DL><p>'

gen_bookmark = False

def usage():
    print 'usage:'
    print '-h,--help: print help message.'
    print '-b,--bookmark: gen bookmark file'
    print '-f,--filter: keyword for filter course'


def write_bookmark_head(f,filter_keyword):
    print "gen bookmark head"
    head = ""
    if filter_keyword != "":
        head = bookmark_start.replace("course", filter_keyword)

    f.write(head)

def write_bookmark_body(f, link, title):
    if link == "":
        return
    f.write('            <DT><A HREF="' + link + '">' + title + "</A>\n")

def write_bookmark_footer(f):
    print "gen bookmark footer"
    f.write(bookmark_end)

def get_file_name(filter_keyword):
    file_name = filter_keyword + str(random.randint(1,1000)) + "-bookmark" + time.strftime("%Y-%m-%d") + ".html"

    return file_name

def do_gen_bookmark(filter_keyword):
    #print filter_keyword
    bookmark_file_name = get_file_name(filter_keyword)
    bookmark_f = open(bookmark_file_name, "a")
    write_bookmark_head(bookmark_f, filter_keyword)
    utils = Utils()
    for file_name in utils.find_file_by_pattern(".*", os.getcwd() + "/db/" + default_subject + "/"):
        url_f = open(file_name)
    
        for line in url_f.readlines():
            record = Record(line)
            url = record.get_url().strip()
            title = record.get_title().strip()

            if filter_keyword != "" and title.lower().find(filter_keyword.lower()) != -1:
                write_bookmark_body(bookmark_f, url, title)
            elif filter_keyword == "":
                write_bookmark_body(bookmark_f, url, title)
            

        url_f.close()

    write_bookmark_footer(bookmark_f)
    bookmark_f.close()
    print "file " + bookmark_file_name + " is ready, you can import it to browser\n"

def main(argv):
    filter_keyword = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hbf:', [])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-b', '--bookmark'):
            global gen_bookmark
            gen_bookmark = True
        elif o in ('-f', '--filter'):
            filter_keyword = str(a).strip()


    if gen_bookmark == False:
        sys.exit(1)
    else:
        do_gen_bookmark(filter_keyword)
    
if __name__ == '__main__':
    main(sys.argv)
