#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import subprocess
from config import Config
import datetime
import random

class Filefinder(BaseExtension):
    form_dict = None
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()


    def excute(self, form_dict):
        self.form_dict = form_dict
        rTitle = form_dict['rTitle'] 
        if rTitle.strip() == '' or len(rTitle.strip()) < 3:
            return ''
        rID = form_dict['rID']
        fileName = form_dict['fileName'].encode('utf8')
        url = form_dict['url'].replace('#space', ' ')
        nocache = True
        if form_dict.has_key('nocache'):
            nocache = form_dict['nocache'].encode('utf8')
        use_cache = nocache == False
        html = ''
        record = self.utils.getRecord(rID.strip(), path=form_dict['originFileName'], log=True, use_cache=use_cache)
        aliasList = self.getAliasList(record)
        divID = form_dict['divID'].encode('utf8')

        if divID.find('-dbfile-') != -1:
            #keywords = aliasList + [rTitle.replace('%20', ' ')]
            keyword = rTitle.replace('%20', ' ').strip()
            dbFileList = self.genFileList(self.getMatchFiles2(keyword, [form_dict['originFileName'][form_dict['originFileName'].find('db/') :], form_dict['fileName'][form_dict['fileName'].find('db/') :]], 'db'))
            if dbFileList != '':
                html += 'matched db files(' + str(keyword) + '):<br>' + dbFileList
            return html


        if form_dict.has_key('selection') and form_dict['selection'] != '':
            rTitle = form_dict['selection'].strip()
        
        localFiles = self.genFileList(self.getMatchFiles(rTitle.strip(), url=url).split('\n'), divID=divID, rID=rID, url=url)
        if localFiles != '':
            if form_dict.has_key('extension_count') and int(form_dict['extension_count']) > 12:
                html += '<br>'
            html += localFiles

        
        count = 0
        if url != '' and self.isDir(url) == False:
            for alias in aliasList:
                count += 1
                result = self.genFileList(self.getMatchFiles(alias.strip()).split('\n'),divID=divID + '-alias-' + str(count), rID=rID)
                if result != '':
                    html += alias + ':<br>' + result

        if fileName.find('exclusive') != -1:
            keyword = rTitle.replace('%20', ' ').strip()
            dbFileList = self.genFileList(self.getMatchFiles2(keyword, [], 'db/library'))
            if dbFileList != '':
                html += 'matched library files(' + str(keyword) + '):<br>' + dbFileList

        html += '<div class="ref"><br>Search My Netdisk<br>' + self.utils.toSmartLink(rTitle, engin=Config.filefinder_netdisk_engin, showText='<font size="2">' + rTitle.replace('%20', ' ') + '</font>', rid=self.form_dict['rID'], library=self.form_dict['originFileName'], module='filefinder') + ' '
        count = 1
        for alias in aliasList:
            count += 1
            html += self.utils.toSmartLink(alias.strip(), engin=Config.filefinder_netdisk_engin, showText=str('<font size="2">' + alias + '</font>'), rid=self.form_dict['rID'], library=self.form_dict['originFileName'], module='filefinder') + ' '
            #html += '&nbsp;'
        html += '</div>'
        if rID.startswith('loop') == False:
            
            fileDivID = divID + '-dbfile-' + str(random.randint(0, 1000))
            fileLinkID = divID + '-dbfile-a-' + str(random.randint(0, 1000))

            html += '<div id="' + fileDivID + '" class="ref">'

            if len(aliasList) == 0:
                script = "var postArgs = {name : 'filefinder', rID : '" + rID + "', rTitle : '" + rTitle +"', check: 'false', fileName : '" + fileName + "', divID : '" + fileDivID + "', originFileName : '" + form_dict['originFileName'] + "'};";
                script += "$('#' + '" + fileDivID +"').load('/extensions', postArgs, function(data) { });$('#' + '" + fileDivID +"').html('Loading...');"
                html += '<a id="' + fileLinkID + '" href="javascript:void(0);" onclick="' + script + '" style="font-size:12pt;">Search Local DB</a><br> '
            else:
                html += '<br>Search Local DB<br>'
                k_list = [rTitle.replace('%20', ' ')] + aliasList
                for keyword in k_list:
                    script = "var postArgs = {name : 'filefinder', rID : '" + rID + "', rTitle : '" + keyword +"', check: 'false', fileName : '" + fileName + "', divID : '" + fileDivID + "', originFileName : '" + form_dict['originFileName'] + "'};";
                    script += "$('#' + '" + fileDivID +"').load('/extensions', postArgs, function(data) { });$('#' + '" + fileDivID +"').html('Loading...');"
                    if len(keyword) > 30:
                        keyword = keyword[0 : 30] + '..'
                    html += '<font size="2"><a id="' + fileLinkID + '" href="javascript:void(0);" onclick="' + script + '">' + keyword +'</a></font> '
            html += '</div>'

        return html

    def getAliasList(self, record):
        aliasList = []
        if record != None and record.get_id().strip() != '':
            ret = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'alias'})
            if ret != None:
                alias = ret.strip()
                print 'alias:' + alias
                if alias != '':
                    if alias.find(',') != -1:
                        aliasList = alias.split(',')
                        return aliasList
                    else:
                        aliasList = [alias.strip()]

        return aliasList

    def isDir(self, url):
        if url.startswith('/User') and url[url.rfind('/') :].find('.') == -1:
            return True
        return False

    def getMatchFiles(self, title, url='', paths=Config.filefinder_dirs):
        output = ''
        cmd = ''
        
        if url != '' and self.isDir(url):
            url = url.replace(' ', '\ ').replace('%20', '\ ')
            paths = [url]
        for path in paths:
            if path != '':
                if url != '' and self.isDir(url):
                    cmd = 'find ' + path + ' -iname "*"'
                else:
                    cmd = 'find ' + path + ' -iname "*' + title.replace('"', '').replace('%20', ' ').replace(' ', '*') + '*"'
                print 'cmd ' + cmd 
                try:
                    output += subprocess.check_output(cmd, shell=True)
                except Exception as e:
                    output += ''
            if output.find('No such file') != -1:
                continue
            if output.find('//') != -1:
                output = output.replace('//', '/')
        #print 'getMatchFiles ' + output
        return output

    dbFileArgsDict = {}

    def getMatchFiles2(self, keyword, filterList, path):
        print filterList
        cmd = 'grep -riE "' + keyword + '" ' + path
        print cmd
        output = ''
        try:
            output = subprocess.check_output(cmd, shell=True)
        except Exception as e:
            return ''
        fileList = []
        fileCountDict = {}
        titleDict = {}
        self.dbFileArgsDict = {}
        lastFileName = ''
        count = 0
        for line in output.split('\n'):
            fileName = line[0 : line.find(':')].strip().replace('//', '/')
            firstIndex = line.find('|')
            rID = line[line.find(':') + 1 : firstIndex].strip().replace(' ', '%20')
            title = line[firstIndex + 1 : line.find('|', firstIndex + 1)].strip()

            igone = False
            for f in filterList:
                if fileName == f.strip():
                    igone = True
                    continue
            if igone:
                continue
             
            if lastFileName != '' and fileName == lastFileName:
                count += 1
            else:
                count = 1
            if fileName != '':
                fileCountDict[fileName] = count 
                if title.lower().find(keyword.lower().strip()) != -1:
                    titleDict[fileName] = ''
                lastFileName = fileName

            if self.dbFileArgsDict.has_key(fileName) == False:
                print fileName
                self.dbFileArgsDict[fileName] = rID
                fileList.append(fileName)
            else:
                if self.dbFileArgsDict[fileName].find(rID) == -1:
                    self.dbFileArgsDict[fileName] = self.dbFileArgsDict[fileName] + '[or]' + rID
        fileCountDict2 = {}
        fileCountDict3 = {}
        for k, v in fileCountDict.items():
            if k == '':
                continue
            key = k + '(' + str(v) + ')'
            if titleDict.has_key(k):
                key = k + '(' + str(v) + '*)'

            if k.find('-library') != -1:
                fileCountDict3[key] = v
            else:
                if Config.filefinder_sort_by_count:
                    fileCountDict2[key] = v
                else:
                    fileCountDict2[key] = k
        
        result = []
        for k, v in sorted(fileCountDict2.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) :
            result.append(k)
        result2 = []
        for k, v in fileCountDict3.items():
            result2.append(k)
        return result2 + result




    def genFileList(self, dataList, divID='', rID='', url=''):
        if len(dataList) == 0:
            return ''
        print 'genFileList ' + ''.join(dataList)
        html = ''
        count = 0
        if len(dataList) > 0:
            html = '<div class="ref"><ol>'
            for line in dataList:

                if line != '' and (line.find('exclusive') == -1 or line.find('.') != -1):
                    if url != '' and line.strip().replace(' ', '%20') == url.strip():
                        continue
                    if line.endswith('.DS_Store'):
                        continue
                    count += 1
                    html += '<li><span>' + str(count) + '.</span>'
                    url = line
                    title = line[line.rfind('/') + 1 :]
                    
                    if line.startswith('db/') and (line[0 : len(line) - 1].endswith(str(datetime.date.today().year)[0 : 3]) or line.find('(') != -1):
                        countInfo = ''
                        if line.find('(') != -1:
                            countInfo = '(<font color="red"><b>' + line[line.find('(') + 1 : line.find(')')] + '</b></font>)'
                            line = line[0 : line.find('(')]
                            title = title[0 : title.rfind('(')].strip()
                            if title.find('-library') != -1:
                                title = '<font color="red">' + title + '</font>'

                        url = 'http://' + Config.ip_adress + '/?db=' + line[line.find('/') + 1 : line.rfind('/') + 1] + '&key=' + line[line.rfind('/') + 1 :] 
                        if line.find('paper') != -1:
                            url += '&column=1'
                        else:
                            url += '&column=' + Config.column_num + '&width=' + Config.default_width
                        if self.dbFileArgsDict.has_key(line.strip()):
                            url += '&filter=' + self.dbFileArgsDict[line.strip()]
                        
                        html += '<p>' + self.utils.enhancedLink(url, title, module='filefinder', rid=self.form_dict['rID'], library=self.form_dict['originFileName'], showText=title + countInfo)
                    else:
                        
                        html += '<p>' + self.utils.enhancedLink(line, title, module='filefinder', rid=self.form_dict['rID'], library=self.form_dict['originFileName']) + self.utils.getIconHtml(line)
                    if divID != '':
                        divID += '-' + str(count)
                        linkID = 'a-' + divID[divID.find('-') + 1 :]
                        appendID = str(count)
                        url = url.replace(' ', '#space')
                        script = self.utils.genMoreEnginScript(linkID, divID, "loop-f-" + rID.replace(' ', '-') + '-' + str(appendID) , title, url, '-', hidenEnginSection=Config.bookmark_hiden_engin_section)
                        html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', divID, '', False);


                    html += '</p></li>'
            html += "</ol></div>"
        if count == 0:
            html = ''

        return html

    def check(self, form_dict):
        return True