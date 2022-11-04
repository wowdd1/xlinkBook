#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
import twitter
import os

def convert(source, crossrefQuery='', proxy=None):
    
    api = twitter.Api(consumer_key='eBC035F5rtFzaTXUfc4X7OpbZ', 
        consumer_secret='Pu2MIeNqgtP5ArQGJx5YkQzY1e2WFmLa3Z7s5CWvWHBB7GGksf', 
        access_token_key='348373764-00MtmSVHbbzcGWlomOhcRn0STmHXMJJT9tBKweWc', 
        access_token_secret='3OjwMbJEkj9Zj7bD2UGcyAwLkvQlLop3JJSudcyBZ7fii',
        sleep_on_rate_limit=True,
        proxies=proxy)
        #proxies=Config.proxies)
    '''
    api = twitter.Api(consumer_key='', 
        consumer_secret='', 
        access_token_key='', 
        access_token_secret='',
        sleep_on_rate_limit=False,
        proxies=None)
    '''

    if source.find('lists/') != -1:
        source = source.replace('/members/', '').replace('/members', '')
        user = source[source.find('com/') + 4 :]
        user = user[0 : user.find('/lists')]

        l = source[source.find('lists/') + 6 :].replace('/', '')
        members = api.GetListMembers(owner_screen_name=user, slug=l)
        for friend in members:

            homepage = ''
            if friend.url != None:
                homepage += ' website:homepage(' + friend.url + ') '

            name = friend.name.replace('"', '').replace("'", '')

            line = ' | ' + name + ' | http://twitter.com/' + friend.screen_name + ' | ' + homepage + ' description:' + friend.description.replace('\n', '<br>').strip().replace('"', '').replace("'", '') + ' alias:' + name + ' icon:' + friend.profile_image_url
            
            print line.encode('utf-8')

    elif source.find('status/') != -1:

        messageID = source[source.rfind('/') + 1:]

        #status = api.GetStatus(messageID)

        #retweeters = api.GetRetweeters(messageID)

        #for uid in retweeters:
        #    user = api.GetUser(user_id=uid)

        #    print user

        #retweets = api.GetRetweets(messageID)

        #jobj = json.loads(status)

        #print retweets

        #print jobj['text']
        retweetedUser = getUserByMessageID(api, messageID, mtype='retweeted')

        for k, v in retweetedUser.items():
            print v


        favoritedUser = getUserByMessageID(api, messageID, mtype='favorited')
        for k, v in favoritedUser.items():
            if retweetedUser.has_key(k):
                continue
            print v

    else:

        user = source[source.find('com/') + 4 :]
        if user.find('/') != -1:
            user = user[0 : user.find('/')]

        #print user
        #print '----friends----'

        friendDict = {}

        #print crossrefQuery
        friendDict = getFriendDict(api, user)

        if crossrefQuery != '':

            if crossrefQuery == ':homepage':
                #print user
                user = api.GetUser(screen_name=user)
                print user.url
                return

            if crossrefQuery.startswith('--join'):
                joinUser = crossrefQuery[crossrefQuery.find('join') + 4 :].strip().replace('"', '').replace("'", '')
                joinUserFriendDict = getUserDict(api, joinUser)


                for k, v in friendDict.items():

                    if joinUserFriendDict.has_key(k):
                        print v
                return
            
            if crossrefQuery.startswith('--merger'):
                mergerUser = crossrefQuery[crossrefQuery.find('merger') + 6 :].strip().replace('"', '').replace("'", '')
                mergerUserFriendDict = getUserDict(api, mergerUser)
                for k, v in friendDict.items():
                    print v
                    if mergerUserFriendDict.has_key(k):
                        mergerUserFriendDict[k] = ''
                for k, v in mergerUserFriendDict.items():
                    if mergerUserFriendDict[k] != '':
                        print v
                return

        else:

            for k, v in friendDict.items():
                print v




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

def getUserByMessageID(api, messageID, mtype='retweeted'):
    url = 'https://twitter.com/i/activity/retweeted_popup?id=' + messageID
    if mtype == 'favorited':
        url = 'https://twitter.com/i/activity/favorited_popup?id=' + messageID
    userDict = {}
    r = requests.get(url)
    jobj = json.loads(r.text)
    soup = BeautifulSoup(jobj['htmlUsers'])
    for div in soup.find_all('div', class_='activity-user-profile-content'):
        screen_name = div.a['href'].replace('/', '')
        line = ' | ' + div.a.strong.text.strip() + ' | http://twitter.com' + div.a['href'] + ' | icon:' + div.img['src'] + ' description:' + div.p.text.strip().replace('\n', '')
        userDict[screen_name] = line.encode('utf-8')   
    return userDict


def getUserDict(api, user):
    userDict = {}
    if os.path.exists(user):
        #print user
        f = open(user)
        for line in f.readlines():
            if line.strip() == '':
                continue
            url = line[line.find('http') : line.find('|', line.find('http'))].strip()
            screen_name = url[url.find('com/') + 4 :]
            userDict[screen_name] = line.strip()
        f.close()
        return userDict

    else:
        return getFriendDict(api, user)

def getFriendDict(api, user):
    friendDict = {}
    friends = api.GetFriends(screen_name=user)
    for friend in friends:
        homepage = ''
        if friend.url != None:
            homepage += ' website:homepage(' + friend.url + ') '
        name = friend.name.replace('"', '').replace("'", '')    
        line = ' | ' + name + ' | http://twitter.com/' + friend.screen_name + ' | ' + homepage + ' description:' + friend.description.replace('\n', '<br>').strip().replace('"', '').replace("'", '') + ' alias:' + name + ' icon:' + friend.profile_image_url

        friendDict[friend.screen_name] = line.encode('utf-8')

    return friendDict

def main(argv):
    source = ''
    crossrefQuery = ''
    proxy={}
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:p:', ["url", "crossrefQuery", "proxy"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a
        if o in ('-p', '--proxy'):
            proxy = {'http' : 'http://' + a,
                          'https' : 'https://' + a}

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery, proxy=proxy)

if __name__ == '__main__':
    main(sys.argv)
