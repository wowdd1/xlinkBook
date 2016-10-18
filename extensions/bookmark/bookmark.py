#!/usr/bin/env python


import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config
import requests
from bs4 import BeautifulSoup

#
# use "Export History/Bookmarks to JSON/XLS*" chrome extension export bookmark to extensions/bookmark/data/chrome_bookmarks.json
# https://chrome.google.com/webstore/detail/export-historybookmarks-t/dcoegfodcnjofhjfbhegcgjgapeichlf
#

class Bookmark(BaseExtension):

    rounter = {'' : '',\
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
        return self.raw_data.lower().find('"parentId":"' + pid + '"') != -1

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
                if self.containIgoncase(jobj['title'], rTitle):
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, self.existChild(str(jobj['id'])))
            else :
                if jobj['parentId'] == pid:
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, self.existChild(str(jobj['id'])))

        html += "</ol></div>"

        if Config.bookmark_enable_cloud_bookmark:
            cloud_bookmark = self.genWebsiteHtml(form_dict['rTitle'].encode('utf8'))
            if cloud_bookmark.find('<li>') != -1:
                html += 'colud bookmark:<br>' + cloud_bookmark
            else:
                return ''

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

    def genWebsiteHtml(self, key):
        html = '<div class="ref"><ol>'
        count = 0
        cookies = dict(unsafe='True')
        page = ''
        page_num = 6
        page = 'http://www.xmarks.com/topic/' + key
        nextpage = ''
        page_count = 0
        for i in range(0, page_num):
            page_count += 1
            if nextpage != '':
                page = nextpage.replace('2', str(page_count))

            print 'request ' + page
            r = requests.get(page, cookies=cookies)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text)
            #print r.text
            for div in soup.find_all('div', class_='content'):
                count += 1
                html += '<li><span>' + str(count) + '.</span><p><a target="_blank" href="' + div.a['href'] + '">' + div.a.text + "</a></p></li>"
            nextDiv = soup.find('div', class_='site-pagination')
            if nextDiv != None and nextpage == '':
                nextpage = 'http://www.xmarks.com' + nextDiv.a['href']
            if nextDiv == None:
                break
        html += "</ol></div>"
        return html

    def containIgoncase(self, leftData, rightData):
        return leftData.lower().find(rightData.lower()) != -1

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return True
        return self.rounter.has_key(rID) or rID.startswith('loop-b') or self.containIgoncase(self.raw_data, rTitle)

