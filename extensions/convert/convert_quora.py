#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
from quora import User



def convert(source):


    user = source[source.find('profile/') + 8:]
    if user.find('/') != -1:
        user = user[0 : user.find('/')]



    userObj = User(user)

    stats = userObj.stats

    #print stats


    print ' | -------topics----- | https://www.quora.com/profile/' + user + '/topics |' 


    r = requests.get('https://www.quora.com/profile/' + user + '/topics')
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a', class_='topic_name'):
        print ' | ' + a.text + ' | https://www.quora.com' + a['href'] + ' | ' 
    print ' | -------blogs----- | https://www.quora.com/profile/' + user + '/blogs |' 

    r = requests.get('https://www.quora.com/profile/' + user + '/blogs')
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a', class_='BoardNameLink'):
        print ' | ' + a.text + ' | ' + a['href'] + ' | '


    print ' | -------following----- | https://www.quora.com/profile/' + user + '/following |' 

    r = requests.get('https://www.quora.com/profile/' + user + '/following')
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a', class_='user'):
        print a.text

    print ' | -------followers----- | https://www.quora.com/profile/' + user + '/followers |' 



def main(argv):
    source = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:', ["url"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source)

if __name__ == '__main__':
    main(sys.argv)
    