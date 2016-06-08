#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
import requests
import random

class Track(BaseExtension):
    
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        title = form_dict['rTitle']
        name = form_dict['name']
        #print name + ' ' + title.encode('utf-8') + ' clicked'
        print self.utils.search_engin_type_engin_dict[name]
        html = ''
        count = 0
        index_dict = {}
        max_index = 3
        engins = self.utils.search_engin_type_engin_dict[name]
        if (len(engins) < 3):
            max_index = len(engins)
        for i in range(0, max_index):
            index = random.randint(0, len(engins) - 1)
            while index_dict.has_key(str(index)):
                index = random.randint(0, len(engins) - 1)
            index_dict[str(index)] = ''

            url = self.utils.search_engin_type_engin_dict[name][index]
            if url.find('%s') != -1:
                url = url.replace('%s', title)
            else:
                url = url + title
            html += '<iframe src="' + url + '" style="border: 0; width: 100%; height: 350px"></iframe>'
            if i != max_index - 1:
                html += '<br/><br/><br/>'

        return html

    def check(self, form_dict):
        return False
