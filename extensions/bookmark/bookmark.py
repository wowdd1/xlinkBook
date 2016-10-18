#!/usr/bin/env python


import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config

#
# use "Export History/Bookmarks to JSON/XLS*" chrome extension export bookmark to extensions/bookmark/data/chrome_bookmarks.json
#

class Bookmark(BaseExtension):

    rounter = {'6.034' : '5582',\
               '' : ''}
    raw_data = ''
    jobj_list = []
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

        f = open('extensions/bookmark/data/chrome_bookmarks.json', 'rU')
        self.raw_data = f.read()
        self.jobj_list = json.loads(self.raw_data)
        f.close()

    def existChild(self, pid):
        return self.raw_data.find('"parentId":"' + pid + '"') != -1

    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        divID = form_dict['divID'].encode('utf8')

        html = '<br><div class="ref"><ol>'
        count = 0
        pid = ''

        if self.rounter.has_key(rID):
            pid = self.rounter[rID]
        elif rID.startswith('loop-b'):
            pid = rID[rID.rfind('-') + 1 :]
        print 'rID ' + rID + ' pid: ' + pid

        for jobj in self.jobj_list:
            if pid == '':
                if jobj['title'].find(rTitle) != -1:
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, self.existChild(str(jobj['id'])))
            else :
                if jobj['parentId'] == pid:
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, self.existChild(str(jobj['id'])))

        html += "</ol></div>"

        return html

    def gen_item(self, rID, ref_divID, count, jobj, moreOption):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        if url != '':
            html += '<p><a target="_blank" href="' + jobj['url'] + '"> '+ self.utils.formatTitle(jobj['title'], Config.smart_link_br_len) + '</a>'
        else:
            html += '<p>' + jobj['title']
        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-b-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), jobj['title'], url, '-')
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            html += '</p></li>'

        return html

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return self.rounter.has_key(rID) or rID.startswith('loop-b') or self.raw_data.find(rTitle) != -1

