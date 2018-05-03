#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source):

    html = ''


    user = source[source.find('people/') + 7 :]
    if user.find('/') != -1:
        user = user[0 : user.find('/')]


    print ' | ----zhuanLan----- | ' + 'https://www.zhihu.com/people/' + user + '/following/columns |'
    getZhuanLan(user)


    print ' | ----topic----- | ' + 'https://www.zhihu.com/people/' + user + '/following/topics |'
    getTopic(user)


    print ' | ----questions----- | ' + 'https://www.zhihu.com/people/' + user + '/following/questions |'
    getQuestion(user)


    print ' | ----following----- | ' + 'https://www.zhihu.com/people/' + user + '/following |'
    getFollowing(user)

    #print ' | ----followers----- | ' + 'https://www.zhihu.com/people/' + user + '/followers |'
    #getFollower(user)

def getFollowing(user):
    for offset in range(0, 1000, 20):
        url = 'https://www.zhihu.com/api/v4/members/' + user + '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(offset) + '&limit=20'
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)

        if r.status_code == 200:

            jobj = json.loads(r.text)

            if jobj.has_key('data') and len(jobj['data']) > 0:

                for item in jobj['data']:
                    url = item['url']
                    url = 'http://www.zhihu.com/people' + url[url.rfind('/'):]
                    line = ' | ' + item['name'] + ' | ' + url + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getFollower(user):
    for offset in range(0, 1000, 20):
        url = 'https://www.zhihu.com/api/v4/members/' + user + '/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(offset) + '&limit=20'

        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:

            jobj = json.loads(r.text)
            if jobj.has_key('data') and len(jobj['data']) > 0:
                for item in jobj['data']:
                    url = item['url']
                    url = 'http://www.zhihu.com/people' + url[url.rfind('/'):]
                    line = ' | ' + item['name'] + ' | ' + url + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getZhuanLan(user):

    for offset in range(0, 1000, 20):

        url = 'https://www.zhihu.com/api/v4/members/' + user + '/following-columns?include=data%5B*%5D.intro%2Cfollowers%2Carticles_count&offset=' + str(offset) + '&limit=20'
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            jobj = json.loads(r.text)
            if jobj.has_key('data') and len(jobj['data']) > 0 and len(jobj['data']) > 0:
                for item in jobj['data']:
                    url = item['url']
                    url = 'https://zhuanlan.zhihu.com' + url[url.rfind('/'):]
                    line = ' | ' + item['title'] + ' | ' + url + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break


def getTopic(user):

    for offset in range(0, 1000, 20):

        url = "https://www.zhihu.com/api/v4/members/" + user + "/following-topic-contributions?include=data%5B*%5D.topic.introduction&offset=" + str(offset) + "&limit=20"
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:

            jobj = json.loads(r.text)
            if jobj.has_key('data') and len(jobj['data']) > 0:
                for item in jobj['data']:
                    url = item['topic']['url']
                    url = 'https://www.zhihu.com/topic' + url[url.rfind('/'):]
                    line = ' | ' + item['topic']['name'] + ' | ' + url + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getQuestion(user):
    for offset in range(0, 1000, 20):
        url = 'https://www.zhihu.com/api/v4/members/' + user + '/following-questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor&offset=' + str(offset) + '&limit=20'

        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:

            jobj = json.loads(r.text)
            if jobj.has_key('data') and len(jobj['data']) > 0:
                for item in jobj['data']:
                    url = item['url']
                    url = 'https://www.zhihu.com/question' + url[url.rfind('/'):]
                    line = ' | ' + item['title'] + ' | ' + url + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break




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
    