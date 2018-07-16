#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup


token = ''

def convert(source, crossrefQuery=''):

    html = ''


    #print 'source'

    user = ''
    project = ''

    args = source[source.find('com/') + 4 : ]
    if args.find('/') != -1:
        user = args[0 : args.find('/')]
        project = args[args.find('/') + 1 :].replace('/', '')
    else:
        user = args


    #print user

    if project != '':

        if user == 'topics':

            getTopicRepos(project, topRepos=120, sortBy='stars')

        else:

            if project == 'awesome-deep-learning-papers':

                r = requests.get(source)
                soup = BeautifulSoup(r.text)

                for li in soup.find_all('li'):

                    line = li.text
                    url = ''
                    if li.a != None:
                        url = li.a['href']
                    if line.find('[pdf]') != -1:
                        if li.strong != None:
                            line = ' | ' + li.strong.text + ' | ' + url + ' | '
                        else:

                            line = ' | ' + line[0 : line.find('(')] + ' | ' + url + ' | '

                        print line.encode('utf-8')
            else:

                print ' | -----topic tag---- | | '
                getRepoTags(user, project)


                #print ' | ----commits----- | https://github.com/' + user + '/' + project + '/commits | '
                #getCommits(user, project)

                #print ' | ----issues----- | https://github.com/' + user + '/' + project + '/issues | '
                #getIssues(user, project)

                #print ' | ----pulls----- | https://github.com/' + user + '/' + project + '/pulls | '
                #getPulls(user, project)

                print ' | ----contributors----- | https://github.com/' + user + '/' + project + '/graphs/contributors | '
                getContributors(user, project)

                #print ' | ----stargazers----- | https://github.com/' + user + '/' + project + '/stargazers | '
                #getStargazers(user, project)

                #print ' | ----watchers----- | https://github.com/' + user + '/' + project + '/watchers | '
                #getWatchers(user, project)

                #print ' | ----forks---- | https://github.com/' + user + '/' + project + '/network/members | '

    else:

        print ' | ----repos----- | https://github.com/' + user + '?tab=repositories | '
        getRepos(user)
        print ' | ----starred----- | https://github.com/' + user + '?tab=stars | '
        getStarred(user)
        print ' | ----gist----- | https://gist.github.com/' + user + ' | '

        print ' | ----following----- | https://github.com/' + user + '?tab=following | '
        getFollow(user, 'following')
        #print ' | ----followers----- | https://github.com/' + user + '?tab=followers | '
        #getFollow(user, 'followers')



    return html

#sortBy 1.'' 2.'stars' 3. 'forks'

def getTopicRepos(topic, topRepos=0, sortBy='stars', topicBRNumber=8):

    url = 'https://github.com/topics/' + topic + '?o=desc&s=' + sortBy

    args = ["", "Y3Vyc29yOjMw", "Y3Vyc29yOjYw", "Y3Vyc29yOjkw", "Y3Vyc29yOjEyMA%3D%3D", "Y3Vyc29yOjE1MA%3D%3D", "Y3Vyc29yOjE4MA%3D%3D", "Y3Vyc29yOjIxMA%3D%3D", "Y3Vyc29yOjI0MA%3D%3D", "Y3Vyc29yOjI3MA%3D%3D", "Y3Vyc29yOjMwMA%3D%3D", "Y3Vyc29yOjMzMA%3D%3D", "Y3Vyc29yOjM2MA%3D%3D", "Y3Vyc29yOjM5MA%3D%3D", "Y3Vyc29yOjQyMA%3D%3D", "Y3Vyc29yOjQ1MA%3D%3D", "Y3Vyc29yOjQ4MA%3D%3D", "Y3Vyc29yOjUxMA%3D%3D", "Y3Vyc29yOjU0MA%3D%3D", "Y3Vyc29yOjU3MA%3D%3D", "Y3Vyc29yOjYwMA%3D%3D", "Y3Vyc29yOjYzMA%3D%3D", "Y3Vyc29yOjY2MA%3D%3D", "Y3Vyc29yOjY5MA%3D%3D", "Y3Vyc29yOjcyMA%3D%3D", "Y3Vyc29yOjc1MA%3D%3D", "Y3Vyc29yOjc4MA%3D%3D", "Y3Vyc29yOjgxMA%3D%3D", "Y3Vyc29yOjg0MA%3D%3D", "Y3Vyc29yOjg3MA%3D%3D", "Y3Vyc29yOjkwMA%3D%3D", "Y3Vyc29yOjkzMA%3D%3D", "Y3Vyc29yOjk2MA%3D%3D"]

    #args = ["", "Y3Vyc29yOjMw"]

    repoCount = topRepos
    count = 0

    for arg in args:
        if arg != '':
            if url.find(topic + '?') == -1:
                url += '?utf8=%E2%9C%93&after=' + arg
            else:    
                url += '&utf8=%E2%9C%93&after=' + arg

        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        count += 1

        if repoCount == 0:
            span = soup.find('span', class_='Counter')

            repoCount = int(span.text.replace(',', '').strip())
        else:
            if 30 * count > repoCount:
                break

        line = ''
        for article in soup.find_all('article'):

            h3 = article.div.h3

            title = h3.text.replace('\n', '').strip()

            user = title[0 : title.find('/')].strip()

            sp = BeautifulSoup(article.prettify())

            desc = 'github:' + user
            topicCount = 0
            for a in sp.find_all('a'):
                if a['href'].startswith('/topics'):
                    desc += ', topics/' + a.text.replace('\n', '').strip()
                    topicCount += 1
                    if topicCount >= topicBRNumber:
                        desc += '<br>'
                        topicCount = 0

            desc += ' insight:' + title.replace(' ', '')

            line = ' | ' + title + ' | ' + 'https://github.com' + h3.a['href'] + ' | ' + desc

            print line.encode('utf-8')
        if line == '':
            break

def getRepoTags(user, project):
    url = 'https://github.com/' + user + '/' + project
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a', class_='topic-tag'):
        print ' | ' + a.text.replace('\n', '').strip() + ' | https://github.com' + a['href'] + ' | ' 



def getCommits(user, project):
    url = 'https://github.com/' + user + '/' + project + '/commits'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for div in soup.find_all('div', class_='table-list-cell'):
        if div.p != None:
            line = ' | ' + div.p.a.text.replace('->', ' ').replace('\n', ' ').strip() + ' | https://github.com' + div.p.a['href'] + ' | '
            print line.encode('utf-8')


def getIssues(user, project):
    url = 'https://github.com/' + user + '/' + project + '/issues'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for div in soup.find_all('div', class_='col-9'):
        line = ' | ' + div.a.text.strip() + ' | https://github.com' + div.a['href'] + ' | '
        print line.encode('utf-8')

def getPulls(user, project):
    url = 'https://github.com/' + user + '/' + project + '/pulls'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for div in soup.find_all('div', class_='col-9'):
        line = ' | ' + div.a.text.strip() + ' | https://github.com' + div.a['href'] + ' | '
        print line.encode('utf-8')



def getContributors(user, project):
    url = 'https://github.com/' + user + '/' + project + '/graphs/contributors-data'
    headers = {'accept' : 'application/json' }
    r = requests.get(url, headers=headers)
    jobj = json.loads(r.text)

    for i in range(len(jobj) -1, -1, -1):
        obj = jobj[i]
        line = '| ' + obj['author']['login'] + ' | https://github.com/' + obj['author']['login'] + ' | icon:' + obj['author']['avatar']
        print line.encode('utf-8')


def getStargazers(user, project, pageSize=50):
    return getUsers(user, project, 'stargazers', pageSize=pageSize)

def getWatchers(user, project, pageSize=50):
    return getUsers(user, project, 'watchers', pageSize=pageSize)

def getUsers(user, project, userType, pageSize=50):

    for page in range(1, pageSize):
        url = 'https://github.com/' + user + '/' + project + '/' + userType + '?page=' + str(page)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        li = soup.find('li', class_='follow-list-item')
        if li == None:
            break

        for li in soup.find_all('li', class_='follow-list-item'):
            line = ' | ' + li.h3.text.replace('"', '').replace("'", '') + ' | https://github.com' + li.h3.a['href'] + ' | icon:' + li.div.a.img['src']
            print line.encode('utf-8')


def getRepos(user, returnAll=True):

    if returnAll:
        repos_dict = getReposV2(user, 'repositories', pageSize=50)
        for k, line in [(k,repos_dict[k]) for k in sorted(repos_dict.keys(), reverse=True)]:
            print line.encode('utf-8')
    else:
        repos_url = "https://api.github.com/users/" + user + "/repos"
        repos_data = requestWithAuth(repos_url)
        repos_jobj = json.loads(repos_data.text)

        repo_dict = {}


        for repo in repos_jobj:
            #print repo['name']
            desc = ''
            if repo.has_key('description') and repo['description'] != None:
                desc = 'description:' 
                desc += 'star(' + str(repo['stargazers_count']) + ') '
                desc += 'forks(' + str(repo['forks']) + ') '
                #desc += 'watchers(' + str(repo['watchers']) + ') '
                desc += repo['description'].replace('\n', '<br>')
            line =  ' | ' + repo['full_name'] + ' | ' + repo['html_url'] + ' | ' + desc


            key = repo.get("stargazers_count", 0)

            repo_dict[getKey(repo_dict, key)] = line

        for k, line in [(k,repo_dict[k]) for k in sorted(repo_dict.keys(), reverse=True)]:
            print line.encode('utf-8')

def getKey(dictData, key):
    if dictData.has_key(key):
        count = 0
        while dictData.has_key(key):
            count += 1
            key = key - count 

        return key
    else:
        return key


def getReposV2(user, repoType, pageSize=50):
    repos_dict = {}
    repos_url_dict = {}
    if repoType == 'stars':
        htmlTag = 'div'
    else:
        htmlTag = 'li'
    for page in range(1, pageSize):
        repo_url = "https://github.com/" + user + "?page=" + str(page) + "&tab=" + repoType

        r = requests.get(repo_url)
        soup = BeautifulSoup(r.text)
        div = soup.find(htmlTag, class_='col-12')
        if div == None:
            break
        for div in soup.find_all(htmlTag, class_='col-12'):
            if div.h3 != None:

                if repos_url_dict.has_key(div.h3.a['href']):
                    return repos_dict
                else:
                    repos_url_dict[div.h3.a['href']] = div.h3.a['href']
                soup2 = BeautifulSoup(div.prettify())
                desc = 'description:'
                links = soup2.find_all('a', class_='muted-link')
                star = 0
                for a in links:
                    if a['href'].endswith('stargazers'):
                        star = int(a.text.strip().replace(',', ''))
                        desc += 'star(' + a.text.strip() + ') '
                        break
                if htmlTag == 'div':
                    divDesc = soup2.find('div', class_='py-1')
                    desc += divDesc.text.replace('\n', '').strip()

                else:
                    desc += div.text.replace('\n', '').strip()




                line = ' | ' + div.h3.text.strip() + ' | http://github.com' + div.h3.a['href']+ ' | ' + desc 

                repos_dict[getKey(repos_dict, star)] = line

    return  repos_dict


def getStarred(user, returnAll=True, pageSize=50):
    starred_dict = {}

    if returnAll:
        starred_dict = getReposV2(user, 'stars', pageSize=pageSize)
    else:
        starred_url = "https://api.github.com/users/" + user + "/starred"

        starred_data = requestWithAuth(starred_url)
        starred_jobj = json.loads(starred_data.text)

        for starred in starred_jobj:

            desc = ''
            if starred.has_key('description') and starred['description'] != None:
                desc = 'description:'
                desc += 'star(' + str(starred['stargazers_count']) + ') '
                desc += 'forks(' + str(starred['forks']) + ') '
                #desc += 'watchers(' + str(starred['watchers']) + ') '
                desc += starred['description'].replace('\n', '<br>')

            line = ' | ' + starred['full_name'] + ' | ' + starred['html_url'] + ' | ' + desc

            key = starred.get("stargazers_count", 0)

            starred_dict[getKey(starred_dict, key)] = line


    for k, line in [(k,starred_dict[k]) for k in sorted(starred_dict.keys(), reverse=True)]:
        print line.encode('utf-8')


def getFollow(user, followType, returnAll=True, pageSize=50):

    if returnAll:

        for page in range(1, pageSize):
            url = 'https://github.com/' + user + '?page=' + str(page) + '&tab=' + followType

            r = requests.get(url)
            soup = BeautifulSoup(r.text)

            div = soup.find('div', class_='col-12')
            if div == None:
                break
            for div in  soup.find_all('div', class_='col-12'):
                desc = ' description:' + div.text.replace('\n', '')
                line = ' | ' + div.span.text + ' | https://github.com' + div.a['href'] + ' | ' + desc +' icon:' + div.a.img['src']
                print line.encode('utf-8')
    else:

        follow_url = "https://api.github.com/users/" + user + "/" + followType
        follow_data = requestWithAuth(follow_url)
        follow_jobj = json.loads(follow_data.text)

        for follow in follow_jobj:
            #print starred
            homepage = ''
            if follow['blog'] != '':
                homepage = 'website:homepage(' + follow['blog'] + ') '
            print ' | ' + follow['login'] + ' | ' + follow['html_url'] + ' | ' + homepage + ' icon:' + follow['avatar_url']


def requestWithAuth(url):
    if token != "":
        return requests.get(url, auth=(token, ''))    
    else:
        return requests.get(url)


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
    