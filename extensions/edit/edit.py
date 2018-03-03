#!/usr/bin/env python
# -*- coding: utf-8-*- 

from extensions.bas_extension import BaseExtension
from config import Config
from utils import Utils
from record import Record, Tag
import os

class Edit(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.tag = Tag()

    def excute(self, form_dict):
        rID = form_dict['rID'].strip()
        rTitle = form_dict['rTitle'].strip()
        fileName = form_dict['originFileName'].strip()
        originFileName = form_dict['originFileName'].strip()
        divID = form_dict['divID']
        if form_dict.has_key('textContent'):
            textContent = form_dict['textContent']
            library = ''
            textContent = textContent.replace(',\n  ', ', ')
            print textContent

            #return ''
            if form_dict['fileName'].strip().endswith('-library'):
                library = form_dict['fileName'][form_dict['fileName'].rfind('/') + 1 :].strip()
            return self.editRecord(rID, self.utils.removeDoubleSpace(textContent.replace('\n', ' ')), originFileName, library=library)
            
        print fileName
        r = self.utils.getRecord(rID, path=fileName, use_cache=False)
        html = 'not found'
        areaID = rID.replace(' ', '-').replace('.', '-') + '-area'
        if r != None and r.get_id().strip() != '':
            column = str(form_dict['column'])
            rows = '25'
            cols = '75'
            if column == '1':
                rows = '45'
                cols = '199' 
            elif column == '2':
                rows = '35'
                cols = '88'
            desc = r.get_describe().strip()
            html = ''
            print form_dict['extension_count']
            print desc
            if int(form_dict['extension_count']) > 12:
                html += '<br>'
            html += '<textarea rows="' + rows + '" cols="' + cols + '" id="' + areaID + '" style="font-size: 13px; border-radius:5px 5px 5px 5px; font-family:San Francisco;color:#003399;white-space:pre-wrap" '
            html += 'onfocus="setbg(' + "'" + areaID + "'," + "'#e5fff3');" + '" '
            html += 'onblur="setbg(' + "'" + areaID + "'," + "'white');" + '">'
            start = 0
            if rID.startswith('custom-'):
                html += 'id:' + r.get_id().strip() + '\n'
                html += '\ntitle:' + r.get_title().strip() + '\n'
            else:
                html += 'title:' + r.get_title().strip() + '\n'
            html += '\nurl:' + r.get_url().strip() + '\n'

            library = ''
            if form_dict['fileName'].strip().endswith('-library'):
                library = form_dict['fileName'][form_dict['fileName'].rfind('/') + 1 :].strip()
            #print 'library:----' + library
            while start < len(desc):
                end = self.utils.next_pos(desc, start, int(cols), self.tag.get_tag_list(library), library=library) 
                #print end
                line = desc[start : end].strip()
                
                print line
                if line.find(':') != -1 and line.find(':') < 15 and line[0 : 1].islower():
                    line = '\n' + line
                line = line.replace(', ', ',\n  ')
                html += line + '\n'
                

                if end < 0 or line.strip() == '':
                    break
                start = end

            html += '</textarea>'
            script = "var text = $('#" + areaID + "'); console.log('', text[0].value);"
            script += "var postArgs = {name : 'edit', rID : '" + rID + "', rTitle : '" + rTitle +"', check: 'false', fileName : '" + fileName + "', divID : '" + divID + "', originFileName : '" + originFileName+ "', textContent: text[0].value};";
            linkid = divID.replace('-edit', '').replace('div', 'a')
            script += "$.post('/extensions', postArgs, function(data) { window.location.href = window.location.href.replace('#', ''); });"
            # var a = document.getElementById('" + linkid + "'); var evnt = a['onclick']; evnt.call(a);

            html += '<br><button type="submit" id="edit_btn" hidefocus="true" onclick="' + script + '">submit</button>'
        return html

    def editRecord(self, rID, data, originFileName, library=''):
        print data
        record = Record(' | | | ' + data)
        newid = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'id'})
        if newid != None:
            newid = newid.strip()
        title = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'title', 'library' : library}).strip()
        url = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'url', 'library' : library}).strip()
        desc = data.replace('title:' + title, '').replace('url:' + url, '').strip()
        print rID
        print title 
        print url
        print desc
        newline = ''
        if rID.startswith('custom-'):
            desc = desc.replace('id:' + newid, '').strip()
            newline = newid + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        else:
            newline = rID + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        print 'newline:'
        print newline
        if os.path.exists(originFileName):
            f = open(originFileName, 'rU')
            all_lines = []
            for line in f.readlines():
                if rID != line[0 : line.find('|')].strip():
                    all_lines.append(line)
                else:
                    print 'old line:'
                    print line
                    all_lines.append(newline)

                    self.syncHistory(line, newline, originFileName)
            f.close()

            self.write2File(originFileName, all_lines)
            
            return 'refresh'
        return 'error'


    def syncHistory(self, oldLine, newLine, originFileName):
        print '--syncHistory--'
        if oldLine != newLine:

            oldRecord = Record(oldLine)
            newRecord = Record(newLine)

            oldID = oldRecord.get_id().strip()
            newID = newRecord.get_id().strip()

            oldDesc = oldRecord.get_describe()
            newDesc = newRecord.get_describe()

            historyFileName = self.getHistoryFile(originFileName)
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

                self.write2File(historyFileName, all_lines)

            elif oldDesc != newDesc:
                print 'desc chanage'
                oldDescDict = self.utils.toDescDict(oldDesc, originFileName)
                newDescDict =  self.utils.toDescDict(newDesc, originFileName)

                notMatchDict = {}

                for k, v in newDescDict.items():
                    if oldDescDict.has_key(k) == False:
                        print 'add new tag:' + k
                    elif oldDescDict[k] != newDescDict[k]:
                        print 'desc not match:' + k

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
                                    desc = self.utils.valueText2Desc(v, prefix=False).strip()

                                    print 'new desc:'
                                    print desc

                                    if line.find('clickcount:') != -1:
                                        clickcount = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'clickcount'}).strip()

                                        desc += ' clickcount:' + clickcount
                                    newline = historyRecord.get_id().strip() + ' | ' + historyRecord.get_title().strip() + ' | ' + historyRecord.get_url().strip() + ' | ' + desc.strip() + '\n'
                                    print 'new line:'
                                    print newline
                                    all_lines.append(newline)
                                    break
                            if found == False:
                                all_lines.append(line)
                    f.close()
                    print 'hislines before:' + str(count) + ' after:' + str(len(all_lines))

                    self.write2File(historyFileName, all_lines)

                    print '---syncHistory finish----'

    def getHistoryFile(self, fileName):
        if fileName.find('/') != -1:
            fileName = fileName[fileName.rfind('/') + 1 :]
        return 'extensions/history/data/'+ fileName + '-history'
       


    def write2File(self, fileName, lines):
        if os.path.exists(fileName):
            f = open(fileName, 'w')
            if len(lines) > 0:
                for line in lines:
                    f.write(line)
            else:
                f.write('')
                f.close()   

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
        rID = form_dict['rID'].strip()
        return rID.startswith('loop') == False
