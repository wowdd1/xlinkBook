#!/usr/bin/env python


import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config
import requests
from bs4 import BeautifulSoup
import subprocess

#
# use "Export History/Bookmarks to JSON/XLS*" chrome extension export bookmark to extensions/bookmark/data/chrome_bookmarks.json
# https://chrome.google.com/webstore/detail/export-historybookmarks-t/dcoegfodcnjofhjfbhegcgjgapeichlf
#
# cat ~/Downloads/chrome_bookmarks.json  > ~/dev/python/course_env/xlinkBook/extensions/bookmark/data/chrome_bookmarks.json && rm ~/Downloads/chrome_bookmarks.json
# 

class Bookmark(BaseExtension):

    rounter = {'' : '',\
               '' : ''}
    raw_data = ''
    jobj_list = []
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.loadBookmark()

    def existChild(self, pid):
        return self.raw_data.lower().find('"parentId":"' + pid + '"') != -1

    def loadBookmark(self):
        f = open('extensions/bookmark/data/chrome_bookmarks.json', 'rU')
        self.raw_data = f.read()
        self.jobj_list = json.loads(self.raw_data)
        f.close()

    def updateBookmark(self):
        if os.path.exists(Config.bookmark_file_path):
            subprocess.check_output("mv " + Config.bookmark_file_path + " extensions/bookmark/data/chrome_bookmarks.json", shell=True)
            self.loadBookmark()

    def getAlias(self, rID, file):
        alias = ''
        record = self.utils.getRecord(rID.strip(), path=file, log=True)
        if record != None and record.get_id().strip() != '':
            ret = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'alias'})
            if ret != None:
                alias = ret.strip()
                print 'alias:' + alias

        if alias.find(',') != -1:
            return alias.split(',')
        elif alias != '':
            return [alias]
        else:
            return []

    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        alias = self.getAlias(rID.strip(), form_dict['originFileName'])
        if form_dict.has_key('selection') and form_dict['selection'].strip() != '':
            selection = form_dict['selection'].encode('utf8').strip()
            #if rTitle.find(selection) != -1:
            rTitle = selection
        divID = form_dict['divID'].encode('utf8')

        self.updateBookmark()

        html = '<br><div class="ref"><ol>'
        count = 0
        pid = ''

        if self.rounter.has_key(rID):
            pid = self.rounter[rID]
        elif rID.startswith('loop-b'):
            pid = rID[rID.rfind('-') + 1 :]
        print 'rID ' + rID + ' pid: ' + pid + ' rTitle:' + rTitle

        for jobj in self.jobj_list:
            if pid == '':
                if self.match_item(jobj, [rTitle]) or self.match_item(jobj, alias):
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])
            else :
                if jobj['parentId'] == pid:
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])

        html += "</ol></div>"

        if count == 0:
            html = ''

        if Config.bookmark_enable_cloud_bookmark:
            cloud_bookmark = self.genWebsiteHtml(form_dict['rTitle'].encode('utf8'), form_dict['originFileName'])
            if cloud_bookmark.find('<li>') != -1:
                html += 'cloud bookmark:<br>' + cloud_bookmark

        return html

    def match_item(self, jobj, rTitleList):
        if len(rTitleList) == 0:
            return False
        for rTitle in rTitleList:
            if self.containIgoncase(jobj['title'].strip(), rTitle.strip()) or (jobj.has_key('url') and (self.containIgoncase(jobj['url'].strip(), rTitle.replace(' ', '').strip()) or self.containIgoncase(jobj['url'].strip(), rTitle.replace(' ', '%20').strip()))):
                return True

        return False

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, orginFilename):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        if url != '':
            html += '<p>' + self.utils.enhancedLink(jobj['url'], self.utils.formatTitle(jobj['title'], Config.smart_link_br_len), module='bookmark', library=orginFilename, rid=rID)
        else:
            html += '<p>' + jobj['title'] + ' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-b-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), jobj['title'], url, '-', hidenEnginSection=True)
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

        html += '</p></li>'

        return html

    def genWebsiteHtml(self, key, orginFilename):
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
                html += '<li><span>' + str(count) + '.</span><p>' + self.utils.enhancedLink(div.a['href'], div.a.text, module='xmarks', library=orginFilename)
                html += "</p></li>"
            nextDiv = soup.find('div', class_='site-pagination')
            if nextDiv != None and nextpage == '':
                nextpage = 'http://www.xmarks.com' + nextDiv.a['href']
            if nextDiv == None:
                break
        html += "</ol></div>"
        return html

    def containIgoncase(self, leftData, rightData):
        return leftData.lower().find(rightData.lower()) != -1

    def containIgoncase2(self, leftData, rightDataList):
        for rightData in rightDataList:
            if leftData.lower().find(rightData.lower()) != -1:
                return True
        return False

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return self.rounter.has_key(rID) or rID.startswith('loop-b') or self.containIgoncase(self.raw_data, rTitle) or Config.bookmark_enable_cloud_bookmark or self.containIgoncase2(self.raw_data, self.getAlias(rID, form_dict['originFileName']))

