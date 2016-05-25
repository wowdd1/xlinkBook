#!/usr/bin/env python


import requests
import json
from bs4 import BeautifulSoup
import os,sys


class Semanticscholar:
    #def __init__(self):
    references = []
    figures = []
    abstract = ''
    authors = []  
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
        self.requestData(self.getUrl(title))

    def getUrl(self, title):
        r = requests.get('https://www.semanticscholar.org/search?q=' + title)
        soup = BeautifulSoup(r.text)
        for result in soup.find_all('div', class_='search-result-title'):
            if result.text.strip() == title.replace("%20", ' ').strip():
                self.have_result = True
                return result.a['href']


    def haveResult(self):
        return self.have_result

    def requestData(self, url):
        print 'requestData'
        #self.requestsReferences(url)
        if url == None:
            return

        r = requests.get('https://www.semanticscholar.org' + url)
        soup = BeautifulSoup(r.text)
        for div in soup.find_all('div', class_='paper-detail-figures-list-figure-image'):
            print div.img['src']
            self.figures.append(div.img['src'])
      
        section = soup.find('section', class_='paper-abstract')
        self.abstract = section.p.text
        soup = BeautifulSoup(soup.find('ul', class_='subhead').prettify())
        for a in soup.find_all('a', class_='author-link'):
            self.authors.append({a.text.strip() : 'https://www.semanticscholar.org' + a['href']})

    def requestsReferences(self, url):
        id = url[url.rfind('/') + 1 : ]
        r = requests.get('https://www.semanticscholar.org/api/1/paper/' + id + '/citations?sort=is-influential&page=1&citationType=citedPapers&citationsPageSize=1000')
        jobj = json.loads(r.text)
        for item in jobj['citations']:
            print item['title']['text']
            url = ''
            if item.has_key('slug') and item.has_key('id'):
                url = 'https://www.semanticscholar.org/paper/' + item['slug'] + '/' + item['id'] + '/pdf'
            print url
            self.references.append([item['title']['text'].strip(), url])

    def getFigures(self):
        return self.figures

    def getReferences(self, title):
        if len(self.references) > 0 and title != self.title:
            return self.references
        else:
            url = self.getUrl(title)
            if url != None:
                self.requestsReferences(self.getUrl(title)) 
                return self.references           
            else:
                return []

    def getAbstract(self):
        return self.abstract

    def getAuthors(self):
        return self.authors

