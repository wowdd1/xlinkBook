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
import random

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
        self.form_dict = None

    def existChild(self, pid):
        return self.raw_data.lower().find('"parentId":"' + pid + '"') != -1

    def loadBookmark(self):
        if os.path.exists('extensions/bookmark/data/chrome_bookmarks.json'):
            f = open('extensions/bookmark/data/chrome_bookmarks.json', 'rU')
            self.raw_data = f.read()
            self.jobj_list = json.loads(self.raw_data)
            f.close()

    def updateBookmark(self):
        if os.path.exists(Config.bookmark_file_path):
            subprocess.check_output("mv " + Config.bookmark_file_path + " extensions/bookmark/data/chrome_bookmarks.json", shell=True)
            self.loadBookmark()

    def getAlias(self, rID, file, nocache):
        alias = ''
        use_cache = nocache == False
        record = self.utils.getRecord(rID.strip(), path=file, log=True, use_cache=use_cache)
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

    def needBR(self):
        if self.form_dict['column'] != '1' and self.form_dict.has_key('extension_count') and int(self.form_dict['extension_count']) > 12:
            return True
        if self.form_dict['column'] == '3' and int(self.form_dict['extension_count']) > 10:
            return True
        return False

    def excute(self, form_dict):
        self.form_dict = form_dict
        divID = form_dict['divID'].encode('utf8')
        nocache = False
        if form_dict.has_key('nocache'):
            nocache = form_dict['nocache'].encode('utf8')

        print divID
        if divID.find('-cloud-') != -1:
            html = ''
            cloud_bookmark = self.genWebsiteHtml(form_dict['rTitle'].encode('utf8'), form_dict['originFileName'])
            if cloud_bookmark.find('<li>') != -1:
                html += 'cloud bookmark(' + form_dict['rTitle'].encode('utf8') + '):<br>' + cloud_bookmark
            else:
                html = ''
            return html
        
        html = ''
        if self.needBR():
            html += '<br>'
        html += '<div class="ref"><ol>'

        rID = form_dict['rID'].encode('utf8')

        fileName = form_dict['fileName'].encode('utf8')
        
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        alias = self.getAlias(rID.strip(), form_dict['originFileName'], nocache)
        print alias
        #if form_dict.has_key('selection') and form_dict['selection'].strip() != '':
        #    selection = form_dict['selection'].encode('utf8').strip()
            #if rTitle.find(selection) != -1:
        #    rTitle = selection
        

        self.updateBookmark()
        
        count = 0
        pid = ''
        records = []
        currentPage = form_dict['page']

        if self.rounter.has_key(rID):
            pid = self.rounter[rID]
        elif rID.startswith('loop-b'):
            pid = rID[rID.rfind('-') + 1 :]
        print 'rID ' + rID + ' pid: ' + pid + ' rTitle:' + rTitle

        notList = []
        aliasList = []
        for item in alias:
            item = item.strip()
            if item.startswith('!') == True:
                notList.append(item.replace('!', '').strip())
            else:
                aliasList.append(item)
        print notList
        print aliasList
        page_item_count = Config.bookmark_page_item_count[int(form_dict['column']) - 1]
        if form_dict.has_key('nopage'):
            page_item_count = 1000

        for jobj in self.jobj_list:
            if pid == '':
                if self.match_item(jobj, [rTitle]) or self.match_item(jobj, aliasList, notList):
                    count += 1
                    if rID.startswith('loop-b'):
                        html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])
                    else:
                        if count <= int(form_dict['page']) * page_item_count and count > (int(form_dict['page']) - 1) * page_item_count:
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
        
        total_page = 0;
        if Config.bookmark_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'bookmark', rTitle, Config.bookmark_output_data_format)
        else:
            if len(records) < page_item_count:
                total_page = 1
            elif len(records) % page_item_count == 0:
                total_page = len(records) / page_item_count
            else:
                total_page = len(records) / page_item_count + 1
            print 'currentPage ' + str(currentPage)

            if total_page > 1 and rID.startswith('loop-b') == False:
                if int(currentPage) == 1:
                    html += '<div style="margin-left:auto; text-align:right;margin-top:2px; margin-right:55px;">'

                    html += self.utils.enhancedLink('', '<font size="1">expand</font>', module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, 1, nopage=True), ignoreUrl=True)
                    html += '</div>'

                html += '<div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto;">'
                for page in range(0, total_page):
                    print (page + 1)

                    if page == 0 and int(currentPage) > 1:
                        html += self.utils.enhancedLink('', '<font size="5">< </font>', module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, int(currentPage) - 1), ignoreUrl=True)
                        html += '&nbsp;&nbsp;&nbsp;&nbsp;'

                    if ((page + 1) == int(currentPage)):
                        html += '<font size="5">' + self.utils.enhancedLink('', str(page + 1), module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, page + 1), style="color:#00BFFF;", ignoreUrl=True) + '</font> '
                    else:
                        html += self.utils.enhancedLink('', str(page + 1), module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, page + 1), ignoreUrl=True) + ' '
                    
                        
                    if page == total_page - 1 and int(currentPage) < total_page:
                        html += '&nbsp;&nbsp;&nbsp;&nbsp;'
                        html += self.utils.enhancedLink('', '<font size="5"> ></font>', module='bookmark', library=form_dict['originFileName'], rid=form_dict['rID'], script=self.getPageScript(form_dict, int(currentPage) + 1), ignoreUrl=True)
            
                html += '</div>'

        if rID.startswith('loop') == False:
            cloudDivID = divID + '-cloud-' + str(random.randint(0, 1000))
            cloudLinkID = divID + '-cloud-a-' + str(random.randint(0, 1000))

            if total_page > 1 and form_dict['column'] != '1':
                html += '<br>'
            html += '<div id="' + cloudDivID + '" class="ref">'
            aCount = 0
            alias = [rTitle] + alias
     
            html += 'Load Cloud Bookmark'
            
            for a in alias:
                aCount += 1
                if aCount == 1:
                    html += '<br>'

                script = "var postArgs = {name : 'bookmark', rID : '" + rID + "', rTitle : '" + a +"', check: 'false', fileName : '" + fileName + "', divID : '" + cloudDivID + "', originFileName : '" + form_dict['originFileName'] + "'};";
                script += "$('#' + '" + cloudDivID +"').load('/extensions', postArgs, function(data) { });$('#' + '" + cloudDivID +"').html('Loading...');"
                html += '<a id="' + cloudLinkID+ '-' + str(aCount) + '" href="javascript:void(0);" onclick="' + script + '" style="font-size:10pt;">' + str(a) + '</a> '
            html += '</div>'
        return html

    def getBookmarkItemCount(self, column):
        return Config.bookmark_page_item_count[int(column) - 1]

    def getPageScript(self, form_dict, page, nopage=False):
        script = 'var postArgs = {};';
        #print form_dict
        for k, v in form_dict.items():
            if k == 'defaultLinks' or k == 'screenWidth' or k =='screenHeight':
                script += 'postArgs["' + k + '"] = ' + str(form_dict[k]) + ';'
            else: 
                script += 'postArgs["' + k + '"] = "' + form_dict[k] + '";'
        script += 'postArgs["page"] = ' + str(page) + ';'
        if nopage:
            script += 'postArgs["nopage"] = true;'
        script += 'requestExtension(postArgs, false);';
        return script


    def match_item(self, jobj, rTitleList, notList=[]):
        if len(rTitleList) == 0:
            return False
        if len(notList) > 0 and self.do_match_item(jobj, notList):
            return False

        return self.do_match_item(jobj, rTitleList)

    def do_match_item(self, jobj, items):
        for rTitle in items:
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

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, orginFilename, keywords=[]):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        if url != '':
            html += '<p>' + self.utils.enhancedLink(url, self.utils.formatTitle(jobj['title'], Config.smart_link_br_len, keywords), module='bookmark', library=orginFilename, rid=rID) + self.utils.getIconHtml(url)
        else:
            html += '<p>' + jobj['title'] +  self.utils.getIconHtml(".dir", radius=False) #' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-b-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), jobj['title'], url, '-', hidenEnginSection=Config.bookmark_hiden_engin_section)

            descHtml = ''
            if url != '':
                descHtml = self.utils.genDescHtml('url:' + url, Config.course_name_len, self.tag.tag_list)
            #print 'descHtml:' + descHtml
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

        html += '</p></li>'

        return html


    def genWebsiteHtml(self, key, orginFilename):
        html = '<ol>'
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
                title = self.colorkeyword(div.a.text, key)
                html += '<li><span>' + str(count) + '.</span><p>' + self.utils.enhancedLink(div.a['href'], title, module='xmarks', library=orginFilename) + self.utils.getIconHtml(div.a['href'])
                html += "</p></li>"
            nextDiv = soup.find('div', class_='site-pagination')
            if nextDiv != None and nextpage == '':
                nextpage = 'http://www.xmarks.com' + nextDiv.a['href']
            if nextDiv == None:
                break
        html += "</ol>"
        return html

    def colorkeyword(self, text, keyword):
        text = text.replace(keyword.replace('%20', ' '), '<font style="color:red;">' + keyword + '</font>')
        text = text.replace(keyword.replace('%20', ' ').lower(), '<font style="color:red;">' + keyword.lower() + '</font>')
        return text

    def containIgoncase(self, leftData, rightData):
        if leftData.lower().find(rightData.lower()) != -1:
            return True
        elif rightData.endswith('s') and leftData.lower().find(rightData[0 : len(rightData) - 1].lower()) != -1:
            return True
        else:
            #if leftData.find('2017') != -1:
            #    print leftData + ' - ' + rightData
            return False

    def containIgoncase2(self, leftData, rightDataList):
        for rightData in rightDataList:
            if leftData.lower().find(rightData.lower()) != -1:
                return True
        return False

    def check(self, form_dict):
        if os.path.exists('extensions/bookmark/data/chrome_bookmarks.json') == False:
            return False
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        nocache = False
        if form_dict.has_key('nocache'):
            nocache = form_dict['nocache'].encode('utf8')
        print 'rTitle:' + rTitle
        return fileName.find('exclusive') != -1 or self.rounter.has_key(rID) or rID.startswith('loop-b') or self.containIgoncase(self.raw_data, rTitle) or self.containIgoncase2(self.raw_data, self.getAlias(rID, form_dict['originFileName'], nocache)) or rTitle.find('.') != -1

