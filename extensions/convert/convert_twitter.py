#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
import twitter

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}


def convert(source):
    

    api = twitter.Api(consumer_key='', 
        consumer_secret='', 
        access_token_key='', 
        access_token_secret='',
        sleep_on_rate_limit=False,
        proxies=None)

    if source.find('lists/') != -1:
        user = source[source.find('com/') + 4 :]
        user = user[0 : user.find('/lists')]
        l = source[source.find('lists/') + 6 :].replace('/', '')
        members = api.GetListMembers(owner_screen_name=user, slug=l)
        for friend in members:
            line = ' | ' + friend.name.replace('"', '').replace("'", '') + ' | http://twitter.com/' + friend.name + ' | description:' + friend.description.replace('\n', '<br>').strip().replace('"', '').replace("'", '') + ' icon:' + friend.profile_image_url
            print line.encode('utf-8')
    else:

        user = source[source.find('com/') + 4 :]
        if user.find('/') != -1:
            user = user[0 : user.find('/')]

        #print user
        #print '----friends----'

        friends = api.GetFriends(screen_name=user)
        for friend in friends:
            line = ' | ' + friend.name.replace('"', '').replace("'", '') + ' | http://twitter.com/' + friend.screen_name + ' | description:' + friend.description.replace('\n', '<br>').strip().replace('"', '').replace("'", '') + ' icon:' + friend.profile_image_url
            print line.encode('utf-8')

        print '----lists----'
        lists = api.GetListsList(screen_name=user)
        #print lists
        for l in lists:
            print ' | ' + l.slug + ' | http://twitter.com' + l.uri + ' |'

        print '----memberships----'
        memberships = api.GetMemberships(screen_name=user)
        for m in memberships:
               line = ' | ' + m.slug + ' | http://twitter.com' + m.uri + ' |'
               print line.encode('utf-8')

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