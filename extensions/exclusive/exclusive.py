#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from config import Config

class Exclusive(BaseExtension):

    def excute(self, form_dict):
	filter = form_dict['rTitle']
	fileName = form_dict['originFileName']
        #if form_dict.has_key('fileName') and form_dict['fileName'] != '':
        #    fileName = form_dict['fileName']
	db = fileName[fileName.find('db/') + 3 : fileName.rfind('/')] + '/'
	key = fileName[fileName.rfind('/') + 1 :]
	return 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + filter.replace('...', '') + '&column=1'


    def check(self, form_dict):
	column = str(form_dict['column']).strip()
        #print 'exclusive check column ' + column
	return column != '1' and form_dict['rID'].startswith('loop') == False
