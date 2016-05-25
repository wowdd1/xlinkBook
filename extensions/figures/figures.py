#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from semanticscholar import Semanticscholar

class Figures(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.semanticscholar = Semanticscholar()

    def excute(self, form_dict):
        name = form_dict['rTitle'] 
        self.semanticscholar.search(name)
        return self.genHtml(self.semanticscholar.getFigures(), form_dict['column'])

    def genHtml(self, figures, column):
        html = '<div>'
        if figures != None and len(figures) > 0:
            width = "100"
            height = "100"
            if column == '3':
                width = "100"
                height = "100"
            if column == '2':
                width = "150"
                height = "150"
            if column == '1':
                width = "250"
                height = "250"
            for fig in figures:
                html += '<img height="' + height + '" width="' + width + '" src="' + fig + '"/>&nbsp;&nbsp;'
 
        html += '</div>'
        return html

   def check(self, form_dict):
        rID = form_dict['rID']
        return rID.startswith('arxiv')
