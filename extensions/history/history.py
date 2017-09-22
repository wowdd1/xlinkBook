#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config
import subprocess
from record import Record
from record import Tag
import re

class History(BaseExtension):

    raw_data = ''
    jobj_list = []
    tag = Tag()

    """docstring for History"""
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        #self.loadHistory()
        self.form_dict = None

    def loadHistory(self):
        self.updateHistory()
        if os.path.exists('extensions/history/data/chrome_history.json'):
            f = open('extensions/history/data/chrome_history.json', 'rU')
            self.raw_data = f.read()
            self.jobj_list = json.loads(self.raw_data)
            f.close()

    def updateHistory(self):
        if os.path.exists(Config.history_file_path):
            subprocess.check_output("mv " + Config.history_file_path + " extensions/history/data/chrome_history.json", shell=True)
            self.loadHistory()

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
        return self.form_dict['column'] != '1' and self.form_dict.has_key('extension_count') and int(self.form_dict['extension_count']) > 12
             
    def getDeleteButton(self, divID, historyFile, url):
        deleteScript = "$.post('/exec', {command : 'deleteRow', fileName : '" + historyFile + "', key : '" + url + "'}, function(data){" + "var target=document.getElementById('" + divID.replace('-history', '') + '-nav-history' + "');hidendiv_2('" + divID + "');navTopic(target,'" + divID.replace('-history', '') + "','" + divID.replace('-history', '') + '-nav-' + "',9);" + "});"
        deleteButton = '&nbsp;&nbsp;<a target="_blank" href="javascript:void(0);" onclick="' + deleteScript + '" style="color:#999966; font-size: 10pt;"><image src="http://findicons.com/files/icons/766/base_software/128/deletered.png" width="14" height="12"></image></a>'    
        return deleteButton

    def getClickCount(self, record):
        if record.line.find('clickcount:') != -1:
            return self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'clickcount'}).strip()
        else:
            return ''


    def excute(self, form_dict):
        self.form_dict = form_dict
        #print form_dict
        if form_dict.has_key('nocache'):
            nocache = form_dict['nocache'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        rID = form_dict['rID'].encode('utf8')
        divID = form_dict['divID'].encode('utf8')
        alias = self.getAlias(rID.strip(), form_dict['originFileName'], nocache)
        html = ''

        if self.existHistoryFile(form_dict['originFileName'].strip()):
            historyFilename = form_dict['originFileName'][form_dict['originFileName'].rfind('/') + 1 :].strip()
            historyFile = 'extensions/history/data/' + historyFilename + '-history'
            print historyFile
            f = open(historyFile, 'r+')
            rDict = {}
            all_lines = f.readlines()
            for line in all_lines:
                r = Record(line)
                if r.valid(line) == False:
                    #print r.line
                    continue
 
                if r.get_url().strip() != '':
                    key = r.get_url().strip()

                    if rDict.has_key(key):

                        cacheRecord = rDict[r.get_url().strip()]

                        desc = self.getClickCount(cacheRecord)

                        cacheLine = cacheRecord.line

                        #desc = str(int(newLine[newLine.rfind(':')+1 :].replace('\n', '').strip()))

                        if line.find('clickcount:') != -1:
                            desc2 = str(int(self.getClickCount(r)))
                            if int(desc2) > int(desc):
                                desc = desc2

                        desc = str(int(desc) + 1)

                        preStr = cacheLine[0: cacheLine.rfind('clickcount:')].strip()
                        preStr2 = r.line[0: r.line.rfind('clickcount:')].strip()

                        if len(preStr2) > len(preStr):
                            preStr = preStr2

                        #print newLine
                        #print desc
                        rDict[r.get_url().strip()] = Record(preStr + ' clickcount:' + desc + '\n') 
                    else:
                        if line.find('clickcount:') != -1:
                            rDict[r.get_url().strip()] = Record(line)
                        else:
                            preStr = line[0: line.rfind('clickcount:')].strip()

                            rDict[r.get_url().strip()] = Record(preStr + ' clickcount:1' + '\n' )

            rList = []
            #print rDict
            if len(rDict) != len(all_lines):
                f.truncate()
                f.close()
            else:
                f.close()

            f = None
            for k, v in rDict.items():
                #print '---' + v.line

                if v.line.strip() != '' and v.valid(v.line):
                    if len(rDict) != len(all_lines):
                        if f == None:
                            #print historyFile
                            f = open(historyFile, 'w')
                        #print v.line

                        f.write(v.line)
                    if v.get_id().strip() == form_dict['rID'].strip() or (v.get_id().strip().startswith('loop') and v.get_id().strip().find(form_dict['rID'].strip()) != -1):
                        rList.append(v)
                else:
                    print v.line

            if f != None:
                f.close()

            #print rList
            #f = open('extensions/history/data/' + historyFilename, 'r')
            if len(rList) > 0:
                if Config.hidtory_sort_type == 0:
                    rList = sorted(rList, key=lambda d: int(self.getClickCount(d)), reverse=False)
                    allSubList = []
                    clickCount = self.getClickCount(rList[0])
                    subList = []
                    for item in rList:
                        clickCount2 = self.getClickCount(item)
                        if clickCount != clickCount2:
                            clickCount = clickCount2
                            allSubList.append(subList)
                            subList = []
                        subList.append(item)
                    if len(subList) > 0:
                        allSubList.append(subList)
                    
                    rList = []
                    for subList in allSubList:
                        rList += sorted(subList, key=lambda d: d.get_url().strip()[0 : 20], reverse=True)
 
                elif Config.hidtory_sort_type == 1:
                    rList = sorted(rList, key=lambda d: d.get_url().strip()[0 : 20], reverse=True)
                elif Config.hidtory_sort_type == 2:
                    rList = sorted(rList, key=lambda d: d.get_title().strip()[0 : 20], reverse=True)
                else:
                    rList = sorted(rList, key=lambda d: d.get_id().strip(), reverse=True)



                if self.needBR():
                    html += '<br>'
                #
                count = 0
                rList.reverse()
                if form_dict['column'] == '1':
                    titleList = []
                    urlList = []
                    htmlList = []
                    for item in rList:
                        title = item.get_title().strip().replace('%20', ' ')
                        titleList.append(title)
                        #print titleList
                        urlList.append(item.get_url().strip())
                        htmlList.append(self.getDeleteButton(divID, historyFile, item.get_url().strip()))

                    return self.utils.toListHtml(titleList, urlList, htmlList, 10, False)
                else:
                    html += '<div class="ref"><ol>'
                    for item in rList:
                        title = item.get_title().strip().replace('%20', ' ')
                        count += 1
                        jobj_record = {}
                        jobj_record['id'] = rID + '-' + str(count)
                        jobj_record['title'] = title
                        jobj_record['url'] = item.get_url().strip()
                        jobj_record['count'] = self.getClickCount(item)
                        jobj_record['desc'] = item.get_describe()

                        appendHtml = self.getDeleteButton(divID, historyFile, item.get_url().strip()) + '&nbsp;'
                        #print jobj_record
                        html += self.gen_item(rID, divID, count, jobj_record, Config.more_button_for_history_module, form_dict['originFileName'], appendHtml=appendHtml)

                        '''
                        html += '<li><span>' + str(count) + '.</span>'
                        html += '<p>' + self.utils.enhancedLink(item.get_url().strip(), self.utils.formatTitle(title, Config.smart_link_br_len, []), module='history', library=form_dict['originFileName'], rid=rID) + self.utils.getIconHtml(item.get_url().strip())
                        '''

                    html += "</ol></div>"

            return html
        else:
            self.updateHistory()

            if self.needBR():
                html += '<br>'
            html += '<div class="ref"><ol>'
            count = 0
            item_dict = {}
            for jobj in self.jobj_list:
                if self.match_item(jobj, [rTitle]) or self.match_item(jobj, alias):
                    if item_dict.has_key(jobj['title'].strip()):
                        continue
                    item_dict[jobj['title'].strip()] = ''
                    count += 1
                    html += self.gen_item(rID, divID, count, jobj, Config.more_button_for_history_module, form_dict['originFileName'])

            html += "</ol></div>"

            if count == 0:
                html = ''
            return html

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, orginFilename, keywords=[], appendHtml=''):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        #if self.tag.account_tag_alias.has_key(jobj['title'].strip()):
        #    title = self.tag.account_tag_alias[jobj['title'].strip()]

        title = self.utils.getValueOrText(jobj['title'].strip(), returnType='text')

        ftitle = self.utils.formatTitle(title, Config.smart_link_br_len, keywords)

        if url != '':
            #print url + jobj['title']
            showText = ftitle
            if Config.history_show_click_count and jobj.has_key('count'):
                clickCount = jobj['count']
                if int(clickCount) > 1:
                    showText = ftitle + ' (' + clickCount + ')'

            html += '<p>' + self.utils.enhancedLink(url, ftitle, module='history', library=orginFilename, rid=rID, showText=showText) + self.utils.getIconHtml(url, title=jobj['title'])
        else:
            html += '<p>' + title + ' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if appendHtml != '':
            html += appendHtml

        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            originTitle = title

            if title.find(' - ') != -1:
                title = title[0 : title.find('-')].strip()

            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-h-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), title, url, originTitle, hidenEnginSection=Config.history_hiden_engin_section)

            descHtml = ''

            if jobj.has_key('desc') and jobj['desc'].strip() != '':
                #print jobj['desc']
                descHtml = self.utils.genDescHtml(jobj['desc'], Config.course_name_len, self.tag.tag_list)
            #if url != '':
            #    descHtml = self.utils.genDescHtml('url:' + url, Config.course_name_len, self.tag.tag_list)
            #print 'descHtml:' + descHtml
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

        html += '</p></li>'

        return html

    def match_item(self, jobj, rTitleList):
        if len(rTitleList) == 0:
            return False
        for rTitle in rTitleList:
            if rTitle.strip() == '':
                continue
            if self.containIgoncase(jobj['title'].strip(), rTitle.strip()):
                #print jobj['title'].strip() + ' ' + rTitle.strip()
                return True
        return False

    def containIgoncase(self, leftData, rightData):
        return leftData.lower().find(rightData.lower()) != -1

    def existHistoryFile(self, filename):
        return os.path.exists(self.getHistoryFileName(filename))

    def getHistoryFileName(self, filename):
        if filename.find('/') != -1:
            filename = filename[filename.rfind('/') + 1 :]
        return 'extensions/history/data/' + filename + '-history'

    def check(self, form_dict):
        self.updateHistory()
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return self.existHistoryFile(form_dict['originFileName']) and self.utils.find_file_by_pattern_path(re.compile(rID, re.I), self.getHistoryFileName(form_dict['originFileName']))

