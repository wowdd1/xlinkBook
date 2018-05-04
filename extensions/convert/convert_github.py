#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup


token = ''

def convert(source):

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


        print ' | ----contributors----- | https://github.com/' + user + '/' + project + '/graphs/contributors | '
        getContributors(user, project)

        print ' | ----stargazers----- | https://github.com/' + user + '/' + project + '/stargazers | '
        getStargazers(user, project)

        #print ' | ----watchers----- | https://github.com/' + user + '/' + project + '/watchers | '
        #getWatchers(user, project)

        #print ' | ----forks---- | https://github.com/' + user + '/' + project + '/network/members | '

    else:

        print ' | ----repos----- | https://github.com/' + user + '?tab=repositories | '
        getRepos(user)
        print ' | ----starred----- | https://github.com/' + user + '?tab=stars | '
        getStarred(user)
        print ' | ----following----- | https://github.com/' + user + '?tab=following | '
        getFollow(user, 'following')
        #print ' | ----followers----- | https://github.com/' + user + '?tab=followers | '
        #getFollow(user, 'followers')


    return html

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
            print ' | ' + follow['login'] + ' | ' + follow['html_url'] + ' | icon:' + follow['avatar_url']


def requestWithAuth(url):
    if token != "":
        return requests.get(url, auth=(token, ''))    
    else:
        return requests.get(url)


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
    