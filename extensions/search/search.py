#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
from config import Config

class Search(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        selection = form_dict['selection']
        display = form_dict['display']
        print 'Search....'
        #print selection.strip()
        #print form_dict
        if display == 'none' or form_dict['rID'].find('loop') != -1:
            return '<div></div>'
        if selection.strip() == form_dict['rTitle']:
            result = '<div><br>'
            url = self.toUrl(form_dict['originFileName'], form_dict['rTitle'])
            count = 0
            for enginTpye in self.utils.getEnginTypes():
                count += 1
                result += '<font size="2"><a target="_blank" font color="#999966" href="' + url + '&enginType=' + enginTpye + '">' + enginTpye + '</a></font> '
                if count %10 == 0:
                    result += '<br>'
            result += '<br></div>'
            return result
        elif selection.strip() != '':
            return self.utils.gen_plugin_content(selection, False) 
        else:
            return 'select some text'

    def toUrl(self, fullFileName, title):
        if fullFileName.find('db/') != -1:
            fullFileName = fullFileName[fullFileName.find('db/') + 3 :]
            db = fullFileName[0 : fullFileName.rfind('/') + 1]
            key = fullFileName[fullFileName.rfind('/') + 1 :]
            return 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + title
        return ''
    def check(self, form_dict):
        return True
