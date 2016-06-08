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
        print name + ' ' + title + ' clicked'
        print self.utils.search_engin_type_engin_dict[name]
        html = ''
        count = 0
        index_dict = {}
        for i in range(0, 3):
            index = random.randint(0, len(self.utils.search_engin_type_engin_dict[name]) - 1)
            while index_dict.has_key(str(index)):
                index = random.randint(0, len(self.utils.search_engin_type_engin_dict[name]) - 1)
            index_dict[str(index)] = ''

            url = self.utils.search_engin_type_engin_dict[name][index]
            if url.find('%s') != -1:
                url = url.replace('%s', title)
            else:
                url = url + title
            html += '<iframe src="' + url + '" style="border: 0; width: 100%; height: 350px"></iframe>'
            if i != 2:
                html += '<br/><br/><br/>'

        return html

    def check(self, form_dict):
        return False
