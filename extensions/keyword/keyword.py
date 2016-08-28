#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
import requests
import json
from utils import Utils

class Keyword(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
        print url
        selection = form_dict['selection']
        print selection
        keywords = []
        keyword_dict = {}
        if selection != None:
            engins = ['google', 'bing', 'amazon', 'youtube']
            for e in engins:
                r = requests.get('http://tools.seochat.com/components/com_seotools/tools/suggest-tool/' + e + 'all.php?q=' + selection)
                jobj = json.loads(r.text)
                for item in jobj:
                   if type(item) != type([]) and item.find('fieldset>') == -1:
                        if keyword_dict.has_key(item.strip()) == False:
                            keyword_dict[item.strip()] = item.strip()
                            keywords.append(item.strip())
            html = '<div class="ref"><ol>'
            count = 0
            ref_divID = form_dict['divID']
            key = form_dict['rID']
            for k in keywords:
                count += 1
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key.replace(' ', '-') + '-' + str(appendID), k, '', '-')
                print k
                html += '<li><span>' + str(count) + '.</span>'
                html += '<p>' + self.utils.toSmartLink(k)
                if script != '':
                    html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                html +='</p></li>'
            return html + '</ol></div>'
        return 'nothing'

        

    def check(self, form_dict):
	return form_dict['rID'] != None and form_dict['rID'].startswith('loop') == False
