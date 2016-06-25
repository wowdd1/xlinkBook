#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils

class Search(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        selection = form_dict['selection']
        if selection.strip() != '':
            return self.utils.gen_plugin_content(selection, False) 
        else:
            return 'please select some text for search'


    def check(self, form_dict):
        return True
