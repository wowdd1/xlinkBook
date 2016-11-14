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
        self.img_style = "-webkit-border-radius: 8px; -moz-border-radius: 8px; border-radius: 8px; background: #f8f8f8; border-top:1px solid #ccc; border-right:1px solid #666; border-bottom:2px solid #999; border-left:1px solid #ccc; padding: 0px;"
        self.img_style_2 = 'border-radius:50%;'
        self.img_style_3 = '-webkit-filter: blur(1px); -moz-filter: blur(30px); -ms-filter: blur(30px); filter: blur(1px); filter:progid:DXImageTransform.Microsoft.Blur(PixelRadius=30, MakeShadow=false);'

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
        if rID.find('arxiv') >= 0 or form_dict['url'].find('arxiv') != -1:
            thumbs = "http://www.arxiv-sanity.com/static/thumbs/" + self.getPid(form_dict['url'])
            version = self.utils.get_last_arxiv_version(rID[rID.find('arxiv-') + 6 :].replace('-', '.')) 
            jpg = '.pdf.jpg'
            thumbs = thumbs + version + jpg
            print 'thumbs ' + thumbs
            return self.genHtml(figures, form_dict['column'], links, thumbs)
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
                html += '<img src="' + self.utils.fixUrl(url, img['src']) + '" width="50" height="50" style="' + self.img_style_2+ '"/>&nbsp;'
                if count > 5:
                    count = 0
                    html += '</div><div>'

            html += '</div>'
        return html


    def getPid(self, url):
        return url[url.rfind('/') + 1 : ].replace('.pdf', '').strip()



    def getRandomFigures(self, title):
        return self.getPinterestImg(title)
        #return self.getGoogleImage(title)

    def getGoogleImage(self, title):
        r = requests.get('https://www.google.com/search?q=%s&newwindow=1&biw=1435&bih=481&source=lnms&tbm=isch&sa=X'.replace('%s', title.replace(' ', '%20')))
        soup = BeautifulSoup(r.text)
        figures = []
        links = []
        for div in soup.find_all('div', class_='rg_di rg_bx rg_el ivg-i'):
            links.append('http://www.google.com' + div.a['href'])
            figures.append('http://www.google.com' + div.a['href'])
        return figures, links

    def getPinterestImg(self, title):
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
        space = ''
        if column == '3':
            width = "100"
            height = "100"
            thumb_width = '450px'
            row_count = 4
            space = ''
        if column == '2':
            width = "130"
            height = "130"
            thumb_width = '563px'
            row_count = 4
            space = 3 * '&nbsp;'
        if column == '1':
            width = "150"
            height = "150"
            thumb_width = '600px'
            row_count = 7
            space = 2 * '&nbsp;'
       
        if thumb != '':
            html += self.utils.enhancedLink(thumb, '', img='<img width="' + thumb_width + '" src="' + thumb + '" style="' + self.img_style + '"/>', module='figures') + '<br/>'
        if figures != None: 
            count = 0
            for fig in figures:
                count += 1
                if len(links) > 0:
                    html += self.utils.enhancedLink(links[count - 1], '', img='<img class="demo-img pos-center" height="' + height + '" width="' + width + '" src="' + fig + '" style="' + self.img_style + '"/>', module='figures') + space
                else:
                    html += self.utils.enhancedLink(fig, '', img='<img height="' + height + '" width="' + width + '" src="' + fig + '" style="' + self.img_style + '"/>', module='figures') + space
                if count % row_count == 0:
                    html += '<br/>'
 
        html += '</div>'
        return html

    def check(self, form_dict):
        return True
