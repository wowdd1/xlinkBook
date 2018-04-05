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
        self.divID = ''

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
                #print 'alias:' + alias

        if alias.find(',') != -1:
            return record, alias.split(',')
        elif alias != '':
            return record, [alias]
        else:
            return record, []

    def needBR(self):
        return self.form_dict['column'] != '1' and self.form_dict.has_key('extension_count') and int(self.form_dict['extension_count']) > 12
             
    def getDeleteButton(self, divID, historyFile, url):
        deleteScript = "$.post('/exec', {command : 'deleteRow', fileName : '" + historyFile + "', key : '" + url + "'}, function(data){" + "var target=document.getElementById('" + divID.replace('-history', '') + '-nav-history' + "');hidendiv_2('" + divID + "');navTopic(target,'" + divID.replace('-history', '') + "','" + divID.replace('-history', '') + '-nav-' + "',9);" + "});"
        deleteButton = '&nbsp;<a target="_blank" href="javascript:void(0);" onclick="' + deleteScript + '" style="color:#999966; font-size: 10pt;"><image src="' + Config.website_icons['delete'] + '" width="14" height="12"></image></a>'    
        return deleteButton

    def getClickCount(self, record):
        if record.line.find('clickcount:') != -1:
            return self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'clickcount'}).strip()
        else:
            return '1'




    def genQuickAccessSyncButton(self, rid, quickAccessHistoryFile, divID, objID):

        script = "$.post('/syncQuickAccess', {rid : '" + rid + "', fileName : '" + quickAccessHistoryFile + "'},function(data) { "

        script += "refreshTab2('" + divID + "', '" + objID + "', 'history');"

        script += "});"

        html = '<a target="_blank" href="javascript:void(0);" onclick="' + script + '">' + self.utils.getIconHtml('', 'sync') + '</a>'

        return html

    def getRefreshID(self, divID, text):
        if text == Config.history_quick_access_name:
            return 'td-' + divID.replace('history', 'a-qa-')

        else:
            return 'td-' + divID.replace('history', 'a-')

    def excute(self, form_dict):
        self.form_dict = form_dict
        

        if form_dict.has_key('command'):
            return self.excuteCommand(form_dict);
        else:
            #print '---excute---'
            print form_dict
            if form_dict.has_key('nocache'):
                nocache = form_dict['nocache'].encode('utf8')
            rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ').strip()
            rID = form_dict['rID'].encode('utf8')
            divID = form_dict['divID'].encode('utf8')
            self.divID = divID
            objID = form_dict['objID'].encode('utf8')
            libraryRecord, alias = self.getAlias(rID.strip(), form_dict['fileName'], nocache)
            html = ''
            quickAccessHistoryFile = ''

            if self.existHistoryFile(form_dict['fileName'].strip()):
                historyFile = self.getHistoryFileName(form_dict['fileName'])
                quickAccessHistoryFile = self.utils.getQuickAccessHistoryFileName()
                print historyFile
                f = open(historyFile, 'r+')
                rDict = {}
                all_lines = f.readlines()
                if Config.history_enable_quick_access:
                    quickAccess = self.utils.queryQuickAccess(rID)
                    if quickAccess != None:
                        print 'quickAccess:' + quickAccess.line
                        all_lines.append(quickAccess.line)
                        #print all_lines
                for line in all_lines:
                    r = Record(line)
                    if r.valid(line) == False:
                        #print r.line
                        continue
     
                    if r.get_url().strip() != '':
                        #key = r.get_url().strip()
                        key = r.get_id().strip() + '-' +r.get_title().strip()
                        if key.find(' - ') != -1:
                            key = key[0 : key.find(' - ')].strip()

                        if rDict.has_key(key):

                            cacheRecord = rDict[key]

                            desc = self.getClickCount(cacheRecord)

                            cacheLine = cacheRecord.line

                            #desc = str(int(newLine[newLine.rfind(':')+1 :].replace('\n', '').strip()))

                            if line.find('clickcount:') != -1:
                                desc2 = str(int(self.getClickCount(r)))
                                #if int(desc2) > int(desc):
                                #    desc = desc2
                                desc = str(int(desc2) + int(desc))
                            else:
                                desc = str(int(desc) + 1)

                            preStr = cacheLine[0: cacheLine.rfind('clickcount:')].strip()
                            preStr2 = r.line[0: r.line.rfind('clickcount:')].strip()



                            newRecord = Record(preStr2)
                            if newRecord.get_describe().strip() != '':
                                preStr = preStr2
                            #print newLine
                            #print desc
                            rDict[key] = Record(preStr + ' clickcount:' + desc + '\n') 
                        else:
                            if line.find('clickcount:') != -1:
                                rDict[key] = Record(line)
                            else:
                                preStr = line[0: line.rfind('clickcount:')].strip()

                                rDict[key] = Record(preStr + ' clickcount:1' + '\n' )

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
                    #if k.lower().endswith(Config.history_quick_access_name.lower()):
                    #    print ')))))))((((' + v

                    if v.line.strip() != '' and v.valid(v.line):
                        if len(rDict) != len(all_lines):
                            if f == None:
                                #print historyFile
                                f = open(historyFile, 'w')
                            #print v.line
                            if k.lower().endswith(Config.history_quick_access_name.lower()) == False and v.get_title().lower().strip() != Config.history_quick_access_name.lower():
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
                    parentDesc = ''
                    if libraryRecord != None:
                        parentDesc = libraryRecord.get_describe()

                    if form_dict['column'] == '1':
                        titleList = []
                        urlList = []
                        htmlList = []
                        descHtmlList = []
                        aidList = []
                        refreshIDList = []

                        count = 0
                        for item in rList:
                            title = item.get_title().strip().replace('%20', ' ')
                            titleList.append(title)
                            #print titleList
                            urlList.append(item.get_url().strip())

                            appendFrontHtml = ''
                            if title.lower() != Config.history_quick_access_name.lower():
                                appendFrontHtml = self.utils.genQuickAcessButton(item, 'history', iconType='remark')
                            else:
                                appendFrontHtml = self.utils.genQuickAcessButton(item, 'history')


                            if title.lower() != Config.history_quick_access_name.lower():
                                htmlList.append(appendFrontHtml + self.getDeleteButton(divID, historyFile, item.get_url().strip()))
                            else:
                                #html = self.utils.getIconHtml('', 'quickaccess')
                                html += appendFrontHtml + self.genQuickAccessSyncButton(rID, quickAccessHistoryFile, divID, objID) + '&nbsp;'

                                htmlList.append(html)
                            count += 1
                            refreshID = self.getRefreshID(self.divID, title)
                            aid = self.getAID(self.divID, count)
                            aidList.append(aid)
                            refreshIDList.append(refreshID)
                            descHtmlList.append(self.utils.genDescHtml(item.get_describe().strip(), Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, aid=aid, refreshID=refreshID))

                        #splitNumber = len(rList) / 3
                        splitNumber = len(rList)
                        return self.utils.toListHtml(titleList, urlList, htmlList, descHtmlList=descHtmlList, splitNumber=splitNumber, moreHtml=True, aidList=aidList, refreshIDList=refreshIDList, orginFilename=form_dict['originFileName'])
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
                            jobj_record['parentDesc'] = parentDesc
                            print jobj_record['desc']
                            appendHtml = ''
                            appendFrontHtml = ''
                            if title.lower() != Config.history_quick_access_name.lower():
                                appendFrontHtml = self.utils.genQuickAcessButton(item, 'history', iconType='remark')

                                appendHtml += self.getDeleteButton(divID, historyFile, item.get_url().strip()) + '&nbsp;'
                            else:
                                #appendHtml = self.utils.getIconHtml('', 'quickaccess')
                                appendFrontHtml = self.utils.genQuickAcessButton(item, 'history')

                                appendHtml += self.genQuickAccessSyncButton(rID, quickAccessHistoryFile, divID, objID) + '&nbsp;'
                            #print jobj_record
                            html += self.gen_item(rID, divID, count, jobj_record, Config.more_button_for_history_module, form_dict['fileName'], form_dict['originFileName'], appendFrontHtml='', appendAfterHtml=appendFrontHtml+appendHtml)

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
                        html += self.gen_item(rID, divID, count, jobj, Config.more_button_for_history_module, form_dict['fileName'], form_dict['originFileName'])

                html += "</ol></div>"

                if count == 0:
                    html = ''
                return html

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, fileName, orginFilename, keywords=[], appendFrontHtml='', appendAfterHtml='', parentDesc=''):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        resType = ''
        if jobj.has_key('url'):
            url = jobj['url']

        title = self.utils.getValueOrText(jobj['title'].strip(), returnType='text')

        if title.find(' - ') != -1:
            resType = title[title.rfind('-') + 1 :].strip()
            if Config.website_icons.has_key(resType):
                title = title[0 : title.find(' - ')]

        if title.find('/') != -1:
            title = title[title.rfind('/') + 1 : ]

        ftitle = self.utils.formatTitle(title, Config.smart_link_br_len, keywords)

        urlIcon = ''
        if url != '':
            if title.lower() != Config.history_quick_access_name.lower():
                urlIcon = self.utils.getIconHtml(url, title=jobj['title'])
            #print url + jobj['title']
            showText = ftitle
            #if Config.history_show_click_count and jobj.has_key('count'):
            #    clickCount = jobj['count']
            #    if int(clickCount) > 1:
            #        showText = ftitle + ' (' + clickCount + ')'
            aid = self.getAID(ref_divID, count)
            refreshID = self.getRefreshID(self.divID, text=title)
            desc = jobj['desc'].strip()
            if desc.find('clickcount') != -1:
                desc = desc[0 : desc.find('clickcount')].strip()

            haveDesc = True
            if len(desc) == 0 and url.find(Config.ip_adress) == -1: #and url.startswith('/') == False:
                haveDesc = False


            pid = aid.replace('a-', 'p-')
            pscript = "switchLinkBGColor('" + pid + "', 'rgb(248, 248, 255)', 'rgb(255, 255, 255)');"

            html += '<p id="' + pid + '" onmouseover="' + pscript + '" style="border-radius: 5px 5px 5px 5px;">'

            html += self.utils.enhancedLink(url, ftitle, module='history', library=fileName, rid=rID, haveDesc=haveDesc, aid=aid, refreshID=refreshID, showText=showText)

            if appendFrontHtml != '':
                html += appendFrontHtml

            html += urlIcon

            #if jobj['desc'].strip().startswith('clickcount') == False and title.lower() != Config.history_quick_access_name.lower():
            #        html += self.utils.getIconHtml('', title='remark')
            

        else:
            html += '<p>' + title 
            if appendFrontHtml != '':
                html += appendFrontHtml
            html += ' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if urlIcon == '' and resType != '' and Config.website_icons.has_key(resType):

            html += self.utils.getIconHtml('', title=resType)

        if appendAfterHtml != '':
            html += appendAfterHtml

        if moreOption:
            linkID = self.getAID(ref_divID, count) + '-more'
            ref_divID += '-' + str(count)
            appendID = str(count)
            originTitle = title

            #if title.find(' - ') != -1:
            #    title = title[0 : title.find('-')].strip()

            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-h-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), title, url, originTitle, hidenEnginSection=Config.history_hiden_engin_section)

            descHtml = ''

            if jobj.has_key('desc') and jobj['desc'].strip() != '':
                #print jobj['desc']
                #refreshID = self.getRefreshID(self.divID, text=title)
                refreshID = ''
                aid = self.getAID(self.divID, count)
                #print 'parentDesc--->'  + jobj['parentDesc']
                if Config.history_enable_subitem_log:
                    descHtml = self.utils.genDescHtml(jobj['desc'], Config.course_name_len, self.tag.tag_list, library=fileName, rid=rID, aid=aid, refreshID=refreshID, iconKeyword=True, fontScala=1, parentDesc=jobj['parentDesc'])
                else:
                    descHtml = self.utils.genDescHtml(jobj['desc'], Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, rid=rID, aid=aid, refreshID=refreshID, parentDesc=jobj['parentDesc'])
            
            #if url != '':
            #    descHtml = self.utils.genDescHtml('url:' + url, Config.course_name_len, self.tag.tag_list)
            #print 'descHtml:' + descHtml
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml).strip();

        html += '</p></li>'

        return html

    def getAID(self, ref_divID, count):
        ref_divID += '-' + str(count)
        linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]

        return linkID

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



    def excuteCommand(self, form):
        if form['command'] == 'sync':
            print 'sync'
            self.syncHistory(form)

        return ''

    def syncHistory(self, form):
        print '--syncHistory--'
        oldLine = form['oldLine']
        newLine = form['newLine']
        originFileName = form['fileName']
        category = form['resourceType']
        utils = self.utils
        if oldLine != newLine:

            oldRecord = Record(oldLine)
            newRecord = Record(newLine)

            oldID = oldRecord.get_id().strip()
            newID = newRecord.get_id().strip()

            oldDesc = oldRecord.get_describe()
            newDesc = newRecord.get_describe()

            historyFileName = self.getHistoryFileName(originFileName)
            print historyFileName

            all_lines = []
            historyRecord = None
            count = 0

            if oldID != newID and os.path.exists(historyFileName):
                print 'id chanage'
                f = open(historyFileName, 'rU')

                for line in f.readlines():
                    count += 1
                    historyRecord = Record(line)

                    if historyRecord.get_id().strip() == oldID:
                        print 'match line:' + line
                        newline = newID + ' | ' + historyRecord.get_title().strip() + ' | ' + historyRecord.get_url().strip() + ' | ' + historyRecord.get_describe().strip() + '\n'
                        print 'newline:' + newline
                        all_lines.append(newline)
                    else:
                        all_lines.append(line)
                f.close()
                print 'hislines before:' + str(count) + ' after:' + str(len(all_lines))

                utils.write2File(historyFileName, all_lines)

            elif oldDesc != newDesc:
                print 'desc chanage'
                oldDescDict = utils.toDescDict(oldDesc, originFileName)
                newDescDict =  utils.toDescDict(newDesc, originFileName)

                print oldDescDict
                print newDescDict

                notMatchDict = {}

                for k, v in newDescDict.items():
                    if oldDescDict.has_key(k) == False:
                        print 'add new tag:' + k
                    elif oldDescDict[k] != newDescDict[k]:
                        print 'desc not match:' + k

                        #print oldDescDict[k]
                        #print newDescDict[k]
                        notMatchDict = self.whatNotMacth(oldDescDict[k], newDescDict[k])

                for k, v in oldDescDict.items():
                    if newDescDict.has_key(k) == False:
                        print 'delete tag:' + k

                if os.path.exists(historyFileName):
                    print 'foud history file:' + historyFileName
                    f = open(historyFileName, 'rU')

                    for line in f.readlines():
                        #print line[0 : line.find('|')].strip()
                        #print newID
                        count += 1
                        historyRecord = Record(line)
                        if newID != historyRecord.get_id().strip():
                            all_lines.append(line)
                        else:
                            found = False
                            for k, v in notMatchDict.items():
                                #print historyRecord.get_title()
                                #print k
                                if historyRecord.get_title().find(k) != -1:

                                    print 'matched line:'
                                    print line
                                    found = True
                                    desc = utils.valueText2Desc(v, prefix=False).strip()

                                    print 'new desc:'
                                    print desc

                                    if category != None and category != '' and desc.find('category:') == -1:
                                        desc += ' category:' + category

                                    if line.find('clickcount:') != -1:
                                        clickcount = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'clickcount'}).strip()
                                        desc += ' clickcount:' + str(clickcount) 
                                                  

                                    newline = historyRecord.get_id().strip() + ' | ' + historyRecord.get_title().strip() + ' | ' + historyRecord.get_url().strip() + ' | ' + desc.strip() + '\n'
                                    print 'new line:'
                                    print newline
                                    all_lines.append(newline)
                                    break
                            if found == False:
                                all_lines.append(line)
                    f.close()
                    print 'hislines before:' + str(count) + ' after:' + str(len(all_lines))

                    utils.write2File(historyFileName, all_lines)

                    print '---syncHistory finish----'



    def whatNotMacth(self, oldValue, newValue):
        result = {}

        oldValueDict = self.toNotMatchDict(oldValue)
        newValueDict = self.toNotMatchDict(newValue)

        #print oldValueDict
        #print newValueDict

        for k, v in newValueDict.items():
            if oldValueDict.has_key(k) and oldValueDict[k] != newValueDict[k]:
                print 'whatChanage:' + k 

                result[k] = newValueDict[k]

        return result

    def toNotMatchDict(self, value):
        valueDict = {}
        if value.find(',') != -1:
            values = value.split(',')
        else:
            values = [value]

        for item in values:
            item = item.strip().encode('utf-8')
            #print '===' + item
            if self.utils.getValueOrTextCheck(item):
                #print item[0 : item.find('(')]
                valueDict[self.utils.getValueOrText(item, 'text')] = item
            else:
                valueDict[item] = item
      
        return valueDict

 

    def check(self, form_dict):
        self.updateHistory()
        rID = form_dict['rID'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return self.existHistoryFile(form_dict['fileName']) and self.utils.find_file_by_pattern_path(re.compile(rID, re.I), self.getHistoryFileName(form_dict['fileName']))

