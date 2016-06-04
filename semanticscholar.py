#!/usr/bin/env python


import requests
import json
from bs4 import BeautifulSoup
import os,sys


class Semanticscholar:
    #def __init__(self):
    references = {}
    citations = {}
    figures = {}
    abstract = {}
    authors = {} 
    have_result = False
    title = ''

    def search(self, title):
        self.title = title
        print 'search ' + title
        '''
        param = {'queryString' : title,
                 'sort' : '"relevance"',
                 'autoEnableFilters' : 'true',
                 'page' : '1',
                 'pageSize' : '10'}
        user_agent = {'User-agent': 'Mozilla/5.0', 'Origin' : 'https://www.semanticscholar.org'}
        r = requests.post('https://www.semanticscholar.org/api/1/search', headers = user_agent, params=param)
        jobj = json.loads(r.text)
        print jobj.keys()

        for result in jobj['results']:
            print result
        '''
        self.requestData(title, self.getUrl(title))

    def getUrl(self, title):
        r = requests.get('https://www.semanticscholar.org/search?q=' + title)
        soup = BeautifulSoup(r.text)
        for result in soup.find_all('div', class_='search-result-title'):
            if result.text.strip() == title.replace("%20", ' ').strip():
                self.have_result = True
                return result.a['href']


    def haveResult(self):
        return self.have_result

    def requestData(self, title, url):
        print 'requestData'
        #self.requestsReferences(url)
        if url == None:
            print 'no url found for ' + title
            return

        r = requests.get('https://www.semanticscholar.org' + url)
        soup = BeautifulSoup(r.text)
        figures = []
        for div in soup.find_all('div', class_='paper-detail-figures-list-figure-image'):
            print div.img['src']
            figures.append(div.img['src'])
        self.figures[title] = figures
      
        section = soup.find('section', class_='paper-abstract')
        self.abstract[title] = section.p.text
        soup = BeautifulSoup(soup.find('ul', class_='subhead').prettify())
        authors = []
        for a in soup.find_all('a', class_='author-link'):
            authors.append({a.text.strip() : 'https://www.semanticscholar.org' + a['href']})
        self.authors[title] = authors

    def requestsReferences(self, title, url):
        id = url[url.rfind('/') + 1 : ]
        self.requestsByType(id, title, 'citedPapers', self.references)

    def requestsCitations(self, title, url):
        id = url[url.rfind('/') + 1 : ]
        self.requestsByType(id, title, 'citingPapers', self.citations)
        

    def requestsByType(self, id, title, citationType, dataDict):
        url = 'https://www.semanticscholar.org/api/1/paper/' + id + '/citations?sort=is-influential&page=1&citationType=' + citationType + '&citationsPageSize=1000'
        print 'requesting url: ' + url
        r = requests.get(url)
        jobj = json.loads(r.text)
        data = []
        for item in jobj['citations']:
            print item['title']['text'].encode('utf-8')
            url = ''
            if item.has_key('slug') and item.has_key('id'):
                url = 'https://www.semanticscholar.org/paper/' + item['slug'] + '/' + item['id'] + '/pdf'
            print url
            data.append([item['title']['text'].strip(), url])
        dataDict[title] = data


    def getFigures(self, title):
        if self.figures.has_key(title):
            print 'return cache for ' + title
            return self.figures[title]

        self.search(title)
        if self.figures.has_key(title):
            return self.figures[title]
        else:
            return ''

    def getReferences(self, title):
        print title
        print self.title
        if self.references.has_key(title):
            print 'return cache for ' + title
            return self.references[title]
        else:
            url = self.getUrl(title)
            if url != None:
                self.requestsReferences(title, self.getUrl(title)) 
                if self.references.has_key(title):
                    return self.references[title] 
                else:
                    return []
            else:
                return []

    def getCitations(self, title):
        print title
        print self.title
        if self.citations.has_key(title):
            print 'return cache for ' + title
            return self.citations[title]
        else:
            url = self.getUrl(title)
            if url != None:
                self.requestsCitations(title, self.getUrl(title))
                if self.citations.has_key(title):
                    return self.citations[title]
                else:
                    return []
            else:
                return []

    def getAbstract(self, title):
        if self.abstract.has_key(title):
            return self.abstract[title]

        self.search(title)
        if self.abstract.has_key(title):
            return self.abstract[title]
        else:
            return ''

    def getAuthors(self, title):
        if self.authors.has_key(title):
            return self.authors[title]

        self.search(title)
        if self.authors.has_key(title):
            return self.authors[title]
        else:
            return ''

