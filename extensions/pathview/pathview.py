#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
from config import Config

class Pathview(BaseExtension):

    def __init__(self):
	BaseExtension.__init__(self)
	self.utils = Utils()

    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        column = form_dict['column']
        if fileName.find('db/') != -1:
            width = '525'
            height = '300'
            if column == '1':
                width = '1300'
                height = '600'
            elif column == '2':
                width = '700'
                height = '400'

            fileName = fileName[fileName.find('db/') + 3 :]
            db = fileName[0 : fileName.rfind('/') + 1]
            key = fileName[fileName.rfind('/') + 1 : ]
            src = "http://" + Config.ip_adress + '/?db=' + db + '&key=' + key + '&nosearchbox=true&column=1'
            print src
            return '<iframe width="' + width + '" height="' + height + '" frameborder="0"  src="' + src + '"></iframe>' 
        return 'nothing'

    def check(self, form_dict):
        originFileName = form_dict['originFileName'].encode('utf8')
        fileName = form_dict['fileName'].encode('utf8')
        return originFileName != fileName and fileName.endswith('-library') == False
