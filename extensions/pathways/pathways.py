#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
from config import Config

class Pathways(BaseExtension):

    def __init__(self):
	BaseExtension.__init__(self)
	self.utils = Utils()

    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        column = form_dict['column']
        url = form_dict['url'].encode('utf8')
        #if fileName.endswith('-library') and url.find(Config.ip_adress) != -1:
        if url.find(Config.ip_adress) != -1:
            fileName = url[url.find('db=') + 3 :]
            fileName = 'db/' + fileName
            fileName = fileName.replace('&key=', '')
            if fileName.find('&') != -1:
                fileName = fileName[0 : fileName.find('&')]
            print fileName
        if fileName.find('db/') != -1:
            width = '530'
            height = '600'
            if column == '1':
                width = '1300'
                height = '600'
            elif column == '2':
                width = '700'
                height = '600'

            fileName = fileName[fileName.find('db/') + 3 :]
            db = fileName[0 : fileName.rfind('/') + 1]
            key = fileName[fileName.rfind('/') + 1 : ]
            if key == '':
                key = '?'
            src = "http://" + Config.ip_adress + '/?db=' + db + '&key=' + key + '&nosearchbox=true&column=1'
            print src
            return '<iframe width="' + width + '" height="' + height + '" frameborder="0"  src="' + src + '"></iframe>' 
        return 'nothing'

    def check(self, form_dict):
        originFileName = form_dict['originFileName'].encode('utf8')
        fileName = form_dict['fileName'].encode('utf8')
        url = form_dict['url'].encode('utf8')
        print fileName
        return (originFileName != fileName and fileName.endswith('-library') == False) or url.find(Config.ip_adress) != -1
