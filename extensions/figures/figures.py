#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from semanticscholar import Semanticscholar

from record import CategoryRecord, Category
import requests
from bs4 import BeautifulSoup

class Figures(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.semanticscholar = Semanticscholar()
        self.utils = Utils()
        self.category_obj = Category()
        self.record = None
        self.category = ''

    def excute(self, form_dict):
        name = form_dict['rTitle'] 
        record = self.utils.getRecord(form_dict['rID'].encode('utf-8'))
        print record.get_id()
        print record.get_describe()
        if record != None or record.get_describe().find('category:') != -1:
    
            record = CategoryRecord(record.line)
            if record.get_category() != None:
                self.category = record.get_category().strip()
        print self.category
        figures = []
        links = []
        if self.category == self.category_obj.paper or self.category.find('cs.') != -1 or self.category.find('stat.') !=-1:
            figures = self.semanticscholar.getFigures(name)
        else:
            figures, links = self.getRandomFigures(record.get_title())

        thumbs = ''
        if record.get_id().strip().startswith('arxiv'):
            thumbs = "http://www.arxiv-sanity.com/static/thumbs/" + self.getPid(record.get_url())
            version = "v1"    
            jpg = '.pdf.jpg'
            retry = 0
            for i in range(1, 10):
                r = requests.get(thumbs + 'v' + str(i) + jpg)
                if r.status_code == 200:
                    retry = 0
                    version = 'v' + str(i)
                else:
                   retry += 1
                if retry >= 2:
                    break 
                #else:
                #    break
            thumbs = thumbs + version + jpg
            print 'thumbs ' + thumbs
        return self.genHtml(figures, form_dict['column'], links, thumbs)


    def getPid(self, url):
        return url[url.rfind('/') + 1 : ].replace('.pdf', '').strip()



    def getRandomFigures(self, title):
        r = requests.get('https://www.pinterest.com/search/pins/?q=' + title)
        soup = BeautifulSoup(r.text)
        figures = []
        links = []
        for div in soup.find_all('div', class_='pinHolder'):
            links.append('https://www.pinterest.com' + div.a['href']) 
            sp = BeautifulSoup(div.prettify())
            img = sp.find('img')
            figures.append(img['src'])
        return figures, links

    def genHtml(self, figures, column, links=[], thumb=''):
        html = '<div>'
        width = "100"
        height = "100"
        thumb_width = '570px'
        row_count = 5
        if column == '3':
            width = "80"
            height = "80"
            thumb_width = '450px'
            row_count = 5
        if column == '2':
            width = "130"
            height = "130"
            thumb_width = '570px'
            row_count = 4
        if column == '1':
            width = "230"
            height = "230"
            thumb_width = '600px'
            row_count = 5
        if thumb != '':
            html += '<a target="_blank" href="' + thumb + '"><img width="' + thumb_width + '" src="' + thumb + '"/></a><br/>'

        if figures != None: 
            count = 0
            for fig in figures:
                count += 1
                if len(links) > 0:
                    html += '<a target="_blank" href="' + links[count - 1] + '"><img class="demo-img pos-center" height="' + height + '" width="' + width + '" src="' + fig + '"/></a>&nbsp;&nbsp;'
                else:
                    html += '<a target="_blank" href="' + fig + '"><img height="' + height + '" width="' + width + '" src="' + fig + '"/></a>&nbsp;&nbsp;'
                if count % row_count == 0:
                    html += '<br/>'
 
        html += '</div>'
        return html

    def check(self, form_dict):
        rID = form_dict['rID']
        return True
        #return rID.startswith('arxiv')
