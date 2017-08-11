#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from config import Config
from utils import Utils
from record import Record
from knowledgegraph import KnowledgeGraph

class Exclusive(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.kg = KnowledgeGraph()

    def excute(self, form_dict):
        rID = form_dict['rID'].strip()
        title = form_dict['rTitle'].strip()
        #fileName = form_dict['fileName']
        url = form_dict['url'].strip()
        fileName = form_dict['originFileName']
        print fileName
        r = self.utils.getRecord(rID, path=fileName)

        if r != None and r.get_id().strip() != '':
            db = fileName[fileName.find('db/') + 3 : fileName.rfind('/')] + '/'
            key = fileName[fileName.rfind('/') + 1 :]
            print db + ' ' + key
            #return 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + title.replace('...', '') + '&column=1'
            return 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + rID + '&column=1&enginType='  + Config.recommend_engin_type
        else:
            title = title.replace('%20', ' ')
            desc = 'engintype:' + title + ' '
            desc += 'localdb:' + title + ' '
            desc += self.kg.getCrossref(title, ' '.join(Config.exclusive_crossref_path))
            record = Record('custom-exclusive-' + rID + ' | '+ title + ' | ' + url + ' | ' + desc)
            return self.utils.output2Disk([record], 'exclusive', 'exclusive')
        #if fileName.find("/custom") != -1:
        #    fileName = form_dict['originFileName']
        #if form_dict.has_key('fileName') and form_dict['fileName'] != '':
        #    fileName = form_dict['fileName']



    def check(self, form_dict):
	    column = str(form_dict['column']).strip()
        #print 'exclusive check column ' + column
	    return True
