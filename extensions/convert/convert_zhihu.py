#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    html = ''

    user = ''
    if source.find('zhuanlan') != -1:

        if source.find('p/') != -1:
            article = source[source.find('p/') + 2 :]
            getRecommendations(article, recommendationSize=40)

            #getComments(article)
        else:
            user = source[source.find('com/') + 4 : ]
            getPosts(user, postType='columns')

    elif source.find('question') != -1:
        question = source[source.rfind('/') + 1 :]

        #getQuestionFollower(question)

        getSimilarQuestions(question)

    elif source.find('topic') != -1:
        source = source.replace('/hot', '')
        topic = source[source.rfind('/') + 1 :]

        getTopicPosts(topic)


    else:
        user = source[source.find('people/') + 7 :]
        if user.find('/') != -1:
            user = user[0 : user.find('/')]

        print ' | ----ideas----- | ' + 'https://www.zhihu.com/people/' + user + '/pins |'
        getPins(user)

        print ' | ----posts----- | ' + 'https://www.zhihu.com/people/' + user + '/posts |'
        getPosts(user)
        
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

def getTopicPosts(toipc):
    url = 'https://www.zhihu.com/api/v4/topics/' + str(toipc) + '/feeds/top_activity?before_id=0&limit=20'

    nextPage = getTopicPostsPage(toipc, url)

    pageDict = {}
    while True: 
        if nextPage != '':
            if nextPage.find('100000000000000') != -1:
                break
            nextPage = getTopicPostsPage(toipc, nextPage)
        else:
            break

def getTopicPostsPage(toipc, pageUrl):

    headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
       
    r = requests.get(pageUrl, headers=headers)

    if r.status_code == 200:
        jobj = json.loads(r.text)
        if jobj.has_key('data') and len(jobj['data']) > 0:
            for item in jobj['data']:
                line = ''
                if item['target']['type'] == 'article':

                    line = ' | ' + item['target']['title'].strip() + ' | ' + item['target']['url'] + ' | '
                elif item['target']['type'] == 'answer':
                    question = item['target']['question']['url']
                    question = question[question.find('question') :].replace('questions', 'question')
                    answer = item['target']['url']
                    answer = answer[answer.find('answer') : ].replace('answers', 'answer')
                    url = 'http://www.zhihu.com/' + question + '/' + answer
                    line = ' | ' + item['target']['question']['title'].strip() + ' | ' + url + ' | '
                print line.encode('utf-8')

        if jobj.has_key('paging') and jobj['paging']['is_end'] == False and jobj['paging'].has_key('next'):
            return jobj['paging']['next']
    return ''


def getRecommendations(article, recommendationSize=40):

    for offset in range(0, recommendationSize, 20):
        url = 'https://www.zhihu.com/api/v4/articles/' + article + '/recommendation?include=data%5B*%5D.article.column&limit=20&offset=' + str(offset)
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
       

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            jobj = json.loads(r.text)

            if jobj.has_key('data') and len(jobj['data']) > 0:

                for item in jobj['data']:

                    desc = ''
                    if item['article']['author'].has_key('headline'):
                        desc = ' description:' + item['article']['author']['headline']
                    line = ' | ' + item['article']['title'].strip() + ' | ' + item['article']['url'] + ' | zhihu:' + item['article']['author']['name'] + '(people/' + item['article']['author']['url_token'] + ') ' + desc
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getComments(article):

    for offset in range(0, 40, 20):
        url = 'https://www.zhihu.com/api/v4/articles/35851304/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=' + str(offset) + '&status=open'
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            jobj = json.loads(r.text)

            if jobj.has_key('data') and len(jobj['data']) > 0:

                for item in jobj['data']:

                    line = ' | ' + item['content'].replace("<p>", '').replace('</p>','') + ' | ' + item['url'] + ' | '

                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getPosts(user, postType='members'):
    for offset in range(0, 1000, 20):
        url = 'https://www.zhihu.com/api/v4/' + postType + '/' + user + '/articles?include=data%5B*%5D.comment_count%2Csuggest_edit%2Cis_normal%2Cthumbnail_extra_info%2Cthumbnail%2Ccan_comment%2Ccomment_permission%2Cadmin_closed_comment%2Ccontent%2Cvoteup_count%2Ccreated%2Cupdated%2Cupvoted_followees%2Cvoting%2Creview_info%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=' + str(offset) + '&limit=20&sort_by=created'
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

        #print url
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            jobj = json.loads(r.text)

            if jobj.has_key('data') and len(jobj['data']) > 0:

                for item in jobj['data']:

                    line = ' | ' + item['title'] + ' | ' + item['url'] + ' | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getPins(user):
    for offset in range(0, 1000, 20):
        url = 'https://www.zhihu.com/api/v4/members/' + user + '/pins?offset=' + str(offset) + '&limit=20&includes=data%5B*%5D.upvoted_followees%2Cadmin_closed_comment'
        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            jobj = json.loads(r.text)

            if jobj.has_key('data') and len(jobj['data']) > 0:

                for item in jobj['data']:

                    line = ' | ' + item['excerpt_title'] + ' |  | '
                    print line.encode('utf-8')
            else:
                break
        else:
            break

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

def getQuestionFollower(question):
    for offset in range(0, 200, 20):
        url = 'https://www.zhihu.com/api/v4/questions/' + question + '/followers?include=data%5B*%5D.gender%2Canswer_count%2Carticles_count%2Cfollower_count%2Cis_following%2Cis_followed&limit=20&offset=' + str(offset)

        headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:

            jobj = json.loads(r.text)
            if jobj.has_key('data') and len(jobj['data']) > 0:
                for item in jobj['data']:
                    url = item['url']
                    url = 'http://www.zhihu.com/people' + url[url.rfind('/'):]
                    line = ' | ' + item['name'] + ' | ' + url + ' | ' #'icon:' + item['avatar_url']
                    print line.encode('utf-8')
            else:
                break
        else:
            break

def getSimilarQuestions(question):
    url = 'https://www.zhihu.com/api/v4/questions/' + question + '/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5'

    headers = {'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
                'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:

        jobj = json.loads(r.text)
        if jobj.has_key('data') and len(jobj['data']) > 0:
            for item in jobj['data']:
                url = item['url']
                url = 'http://www.zhihu.com/question' + url[url.rfind('/'):]
                line = ' | ' + item['title'] + ' | ' + url + ' | ' #'icon:' + item['avatar_url']
                print line.encode('utf-8')

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
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:', ["url", "crossrefQuery"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    