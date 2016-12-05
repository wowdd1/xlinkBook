#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
import requests
import random
import subprocess

class Track(BaseExtension):
    
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        title = form_dict['rTitle']
        name = form_dict['name']
        #print name + ' ' + title.encode('utf-8') + ' clicked'
        
        html = ''
        count = 0
        index_dict = {}
        max_index = 3
        if name.strip().find(' ') != -1:
            engins = name.split(' ')
        else:
            if self.utils.search_engin_type_engin_dict.has_key(name):
                engins = self.utils.search_engin_type_engin_dict[name]
            else:
                engins = self.utils.getEnginList('d:' + name)
        print engins
        if (len(engins) < 3):
            max_index = len(engins)
        for i in range(0, max_index):
            index = random.randint(0, len(engins) - 1)
            while index_dict.has_key(str(index)):
                index = random.randint(0, len(engins) - 1)
            index_dict[str(index)] = ''

            if engins[index].find('http') == -1:
                url = self.utils.getEnginUrl(engins[index].strip())
            else:
                url = engins[index]
            if url.find('%s') != -1:
                url = url.replace('%s', title)
            else:
                url = url + title

            engin = url[url.find('//') + 2 : url.find('/', url.find('.'))]
            engin = engin.replace('www.', '').replace('.com', '')
            div_radius = '<div style="background-color:#EEEEFF; border-radius: 5px 5px 5px 5px; width:auto; float:left;">'
            if self.utils.suportFrame(url, 2):
                html += '<br/><iframe src="' + url + '" style="border: 0; width: 100%; height: 400px;" allowfullscreen></iframe><br/>'
                html += div_radius + '<a target="_blank" href="' + url+ '">' + engin + '</a></div><br/>'
            else:
                html += '<br/>' + div_radius + '<a target="_blank" href="' + url+ '">search ' + title.replace('%20', ' ') + ' with ' +  engin +' </a></div><br/>'
            

        return html

    def check(self, form_dict):
        return False
