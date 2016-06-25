#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from semanticscholar import Semanticscholar
import subprocess
from record import CategoryRecord, Category
import requests
from bs4 import BeautifulSoup
from config import Config

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
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        figures = []
        links = []
        if fileName.find('papers') != -1:
            figures = self.semanticscholar.getFigures(name)
        else:
            figures, links = self.getRandomFigures(name)

        thumbs = ''
        if rID.find('arxiv') >= 0:
            thumbs = "http://www.arxiv-sanity.com/static/thumbs/" + self.getPid(form_dict['url'])
            version = self.utils.get_last_arxiv_version(rID[rID.find('arxiv-') + 6 :].replace('-', '.')) 
            jpg = '.pdf.jpg'
            thumbs = thumbs + version + jpg
            print 'thumbs ' + thumbs
        return self.getRefImage(rID, form_dict['url']) + self.genHtml(figures, form_dict['column'], links, thumbs)



    def getRefImage(self, rID, url):
        html = ''
        if rID.find('arxiv') >= 0:
            return html
        if Config.disable_reference_image == False and url.strip() != '':
            user_agent = {'User-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(r.text)
            count = 0
            for img in soup.find_all('img'):
                if img['src'].endswith('.gif'):
                    continue
                if count == 0:
                    html += '<div>'
                count += 1
                html += '<img src="' + self.utils.fixUrl(url, img['src']) + '" width="80" height="50"/>&nbsp;'
                if count > 5:
                    count = 0
                    html += '</div><div>'

            html += '</div>'
        return html


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
            width = "150"
            height = "150"
            thumb_width = '600px'
            row_count = 6
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
