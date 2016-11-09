#!/usr/bin/env python


import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config
import requests
from bs4 import BeautifulSoup
import subprocess
from record import Record
from record import Tag

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
    tag = Tag()
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
        #if form_dict.has_key('selection') and form_dict['selection'].strip() != '':
        #    selection = form_dict['selection'].encode('utf8').strip()
            #if rTitle.find(selection) != -1:
        #    rTitle = selection
        divID = form_dict['divID'].encode('utf8')

        self.updateBookmark()

        html = '<br><div class="ref"><ol>'
        count = 0
        pid = ''
        records = []
        currentPage = form_dict['page']

        if self.rounter.has_key(rID):
            pid = self.rounter[rID]
        elif rID.startswith('loop-b'):
            pid = rID[rID.rfind('-') + 1 :]
        print 'rID ' + rID + ' pid: ' + pid + ' rTitle:' + rTitle

        for jobj in self.jobj_list:
            if pid == '':
                if self.match_item(jobj, [rTitle]) or self.match_item(jobj, alias):
                    count += 1
                    if rID.startswith('loop-b'):
                        html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])
                    else:
                        if count < int(form_dict['page']) * Config.bookmark_page_item_count and count >= (int(form_dict['page']) - 1) * Config.bookmark_page_item_count:
                            currentPage = form_dict['page']
                            html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])
                    url = ''
                    if jobj.has_key('url'):
                        url = jobj['url']
                    records.append(Record('bookmark-' + str(count) + ' | ' + jobj['title'] + ' | ' + url + ' | '))
            else :
                if jobj['parentId'] == pid:
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])
                    url = ''
                    if jobj.has_key('url'):
                        url = jobj['url']
                    records.append(Record('bookmark-' + str(count) + ' | ' + jobj['title'] + ' | ' + url + ' | '))

        html += "</ol></div>"

        if count == 0:
            html = ''

        if Config.bookmark_enable_cloud_bookmark:
            cloud_bookmark = self.genWebsiteHtml(form_dict['rTitle'].encode('utf8'), form_dict['originFileName'])
            if cloud_bookmark.find('<li>') != -1:
                html += 'cloud bookmark:<br>' + cloud_bookmark

        if Config.bookmark_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'bookmark', rTitle, Config.bookmark_output_data_format)
        else:
            total_page = 0;
            if len(records) < Config.bookmark_page_item_count:
                total_page = 1
            elif len(records) % Config.bookmark_page_item_count == 0:
                total_page = len(records) / Config.bookmark_page_item_count
            else:
                total_page = len(records) / Config.bookmark_page_item_count + 1
            print 'currentPage ' + str(currentPage)
            if total_page > 1 and rID.startswith('loop-b') == False:
                html += '<div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto;">'
                for page in range(0, total_page):
                    print (page + 1)
                    if page == 0 and int(currentPage) > 1:
                        html += self.utils.enhancedLink('', '<font size="5"><</font>', module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, int(currentPage) - 1))
                        html += '&nbsp;&nbsp;&nbsp;&nbsp;'

                    if ((page + 1) == int(currentPage)):
                        html += '<font size="5">' + self.utils.enhancedLink('', str(page + 1), module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, page + 1), style="color:#00BFFF;") + '</font> '
                    else:
                        html += self.utils.enhancedLink('', str(page + 1), module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, page + 1)) + ' '
                    
                        
                    if page == total_page - 1 and int(currentPage) < total_page:
                        html += '&nbsp;&nbsp;&nbsp;&nbsp;'
                        html += self.utils.enhancedLink('', '<font size="5">></font>', module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, int(currentPage) + 1))
            
                html += '</div>'
            return html

    def getPageScript(self, form_dict, page):
        script = 'var postArgs = {};';
        script += 'postArgs["objID"] = "' + form_dict['objID'] + '";'
        script += 'postArgs["targetid"] = "' + form_dict['targetid'] + '";'
        script += 'postArgs["targetDataId"] = "' + form_dict['targetDataId'] + '";'
        script += 'postArgs["name"] = "' + form_dict['name'] + '";'
        script += 'postArgs["rID"] = "' + form_dict['rID'] + '";'
        script += 'postArgs["rTitle"] = "' + form_dict['rTitle'] + '";'
        script += 'postArgs["url"] = "' + form_dict['url'] + '";'
        script += 'postArgs["fileName"] = "' + form_dict['fileName'] + '";'
        script += 'postArgs["check"] = "' + form_dict['check'] + '";'
        script += 'postArgs["column"] = "' + form_dict['column'] + '";'
        script += 'postArgs["divID"] = "' + form_dict['divID'] + '";'
        script += 'postArgs["defaultLinks"] = ' + str(form_dict['defaultLinks']) + ';'
        script += 'postArgs["user_name"] = "' + form_dict['user_name'] + '";'
        script += 'postArgs["originFileName"] = "' + form_dict['originFileName'] + '";'
        script += 'postArgs["selection"] = "' + form_dict['selection'] + '";'
        script += 'postArgs["screenWidth"] = ' + str(form_dict['screenWidth']) + ';'
        script += 'postArgs["screenHeight"] = ' + str(form_dict['screenHeight']) + ';'

        script += 'postArgs["page"] = ' + str(page) + ';'

        script += 'requestExtension(postArgs, false);';
        return script


    def match_item(self, jobj, rTitleList):
        if len(rTitleList) == 0:
            return False
        for rTitle in rTitleList:
            if rTitle.strip() == '':
                continue
            if self.containIgoncase(jobj['title'].strip(), rTitle.strip()):
                #print jobj['title'].strip() + ' ' + rTitle.strip()
                return True
            if jobj.has_key('url') and len(rTitle) > 8:
                if self.containIgoncase(jobj['url'].strip(), rTitle.replace(' ', '').strip()):
                    return True
                if self.containIgoncase(jobj['url'].strip(), rTitle.replace(' ', '%20').strip()):
                    return True
                if self.containIgoncase(jobj['url'].strip(), rTitle.strip().replace(' ', '-')):
                    return True
            if self.containIgoncase(jobj['title'].strip(), rTitle.strip().replace(' ', '-')):
                return True

        return False

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, orginFilename):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        if url != '':
            html += '<p>' + self.utils.enhancedLink(url, self.utils.formatTitle(jobj['title'], Config.smart_link_br_len), module='bookmark', library=orginFilename, rid=rID)
        else:
            html += '<p>' + jobj['title'] + ' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-b-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), jobj['title'], url, '-', hidenEnginSection=Config.bookmark_hiden_engin_section)

            descHtml = self.utils.genDescHtml('url:' + url, Config.course_name_len, self.tag.tag_list)
            print 'descHtml:' + descHtml
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

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

