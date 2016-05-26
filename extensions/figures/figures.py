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
            self.semanticscholar.search(name)
            figures = self.semanticscholar.getFigures()
        else:
            figures, links = self.getRandomFigures(record.get_title())

        return self.genHtml(figures, form_dict['column'], links)


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

    def genHtml(self, figures, column, links=[]):
        html = '<div>'
        if figures != None and len(figures) > 0:
            width = "100"
            height = "100"
            row_count = 5
            if column == '3':
                width = "100"
                height = "100"
                row_count = 5
            if column == '2':
                width = "150"
                height = "150"
                row_count = 4
            if column == '1':
                width = "250"
                height = "250"
                row_count = 6
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
        return rID.startswith('arxiv')
