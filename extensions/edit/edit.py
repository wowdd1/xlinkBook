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
        print form_dict
        rID = form_dict['rID'].strip()
        rTitle = form_dict['rTitle'].replace('%20', ' ').strip()
        fileName = form_dict['fileName'].strip()
        originFileName = form_dict['originFileName'].strip()
        divID = form_dict['divID']

        library = form_dict['fileName']

        if form_dict.has_key('textContent'):
            textContent = form_dict['textContent']

            if rID.startswith('loop-h'):
                editedData = ''
                textContent = textContent.replace(',\n', '+')
                textContent = self.utils.removeDoubleSpace(textContent)
                textContent = textContent.replace(', ', '+')
                textContent = textContent.replace(',', '+')
                textContent = textContent.replace('\n', '')
                editedData = rTitle + '(' + textContent + ')'
                print 'editedData--->' + editedData
                r, historyRecord = self.getRecordByHistory(rID, rTitle, fileName)

                if r != None:
                    editRID = r.get_id().strip()
                    resourceType = ''
                    if historyRecord != None and editedData.find('category(') == -1:
                        resourceType = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', historyRecord.line, {'tag' : 'category'})
                        if resourceType != None:
                            resourceType = resourceType.strip()

                    print 'editRID-->' + editRID
                    if rID.find(editRID) != -1:
                        newData = r.edit_desc_field2(self.utils, r, resourceType, rTitle, editedData, self.tag.get_tag_list(library), library=library)

                        if newData != '':

                            #print '--->' + newData
                            result = self.editRecord(editRID, self.utils.removeDoubleSpace(newData), originFileName, library=library, resourceType=resourceType)

                            if divID.find('-history-') != -1:
                                aid = divID[0 : divID.find('-history-')].strip() + '-a-'
                                result =result + '#history#' + aid

                            print 'result--->' + result
                            return result

                return 'error'
            
            else:
                textContent = textContent.replace(',\n  ', ', ')
                print textContent

                return self.editRecord(rID, self.utils.removeDoubleSpace(textContent.replace('\n', ' ')), originFileName, library=library)
            

            return 'error'


        column = str(form_dict['column'])
        print fileName
        r = self.utils.getRecord(rID, path=fileName, use_cache=False)
        html = 'not found'


        areaID = rID.replace(' ', '-').replace('.', '-') + '-area'

        if rID.startswith('loop-h'):
            r, historyRecord = self.getRecordByHistory(rID, rTitle, fileName)

            if r != None:
                #print r.line
                item = r.get_desc_field2(self.utils, rTitle, self.tag.get_tag_list(library), library=library)
                if item != '':
                    print '---->' + item

                    text = value = self.utils.getValueOrText(item, returnType='text')
                    value = self.utils.getValueOrText(item, returnType='value')

                    rows, cols = self.getRowsCols(column)
                    html = self.genTextareaHtml(rows, cols, areaID, value.replace('+', ',\n'))
                    html += '<br>'
                    html += self.genEditButton(areaID, rID, text, fileName, divID, originFileName)
                    return html

            return r.line

        if r != None and r.get_id().strip() != '':

            desc = r.get_describe().strip()
            html = ''
            print form_dict['extension_count']
            print desc
            if int(form_dict['extension_count']) > 12:
                html += '<br>'

            start = 0
            text = ''
            rows, cols = self.getRowsCols(column)
            if rID.startswith('custom-'):
                text += 'id:' + r.get_id().strip() + '\n'
                text += '\ntitle:' + r.get_title().strip() + '\n'
            else:
                text += 'title:' + r.get_title().strip() + '\n'
            text += '\nurl:' + r.get_url().strip() + '\n'


            #print 'library:----' + library
            while start < len(desc):
                end = self.utils.next_pos(desc, start, int(cols), self.tag.get_tag_list(library), library=library) 
                #print end
                line = desc[start : end].strip()
                
                print line
                if line.find(':') != -1 and line.find(':') < 15 and line[0 : 1].islower():
                    line = '\n' + line
                line = line.replace(', ', ',\n  ')
                text += line + '\n'
                

                if end < 0 or line.strip() == '':
                    break
                start = end

            html += self.genTextareaHtml(rows, cols, areaID, text)
            html += '<br>'
            html += self.genEditButton(areaID, rID, rTitle, fileName, divID, originFileName)
        return html

    def getRecordByHistory(self, rid, title, fileName):
        path = fileName[0 : fileName.find('db/')] + 'extensions/history/data/' + fileName[fileName.rfind('/') + 1:] + '-history'
        print path
        print title
        rList = self.utils.getRecord(title, path=path, use_cache=False, accurate=False, matchType=2, return_all=True, log=True)

        for historyRecord in rList:
            historyRID = historyRecord.get_id().strip()
            print 'historyRID:' + historyRID + ' rid:' + rid
            if historyRID != '' and rid.find(historyRID) != -1:
                record = self.utils.getRecord(historyRID, path=fileName, use_cache=False)

                return record, historyRecord

        return None

    def genEditButton(self, areaID, rID, rTitle, fileName, divID, originFileName):
        script = "var text = $('#" + areaID + "'); console.log('', text[0].value);"
        script += "var postArgs = {name : 'edit', rID : '" + rID + "', rTitle : '" + rTitle +"', check: 'false', fileName : '" + fileName + "', divID : '" + divID + "', originFileName : '" + originFileName+ "', textContent: text[0].value};";
        linkid = divID.replace('-edit', '').replace('div', 'a')
        script += "$.post('/extensions', postArgs, function(data) { \
                        console.log('refresh:' + data);\
                        if (data.indexOf('#') != -1) {\
                            dataList = data.split('#');\
                            if (dataList.length == 3) {\
                                if (dataList[1] == 'history') {\
                                    refreshTab(dataList[2], 'history');\
                                    return;\
                                }\
                            }\
                            window.location.href = window.location.href.replace('#', '');\
                        } else {\
                            window.location.href = window.location.href.replace('#', ''); \
                        }});"
        # var a = document.getElementById('" + linkid + "'); var evnt = a['onclick']; evnt.call(a);

        html = '<button type="submit" id="edit_btn" hidefocus="true" onclick="' + script + '">submit</button>'

        return html


    def getRowsCols(self, column):
        rows = '25'
        cols = '75'
        if column == '1':
            rows = '45'
            cols = '199' 
        elif column == '2':
            rows = '35'
            cols = '88'
        return rows, cols

    def genTextareaHtml(self, rows, cols, areaID, text):
        html = ''
        html += '<textarea rows="' + rows + '" cols="' + cols + '" id="' + areaID + '" style="font-size: 13px; border-radius:5px 5px 5px 5px; font-family:San Francisco;color:#003399;white-space:pre-wrap" '
        html += 'onfocus="setbg(' + "'" + areaID + "'," + "'#e5fff3');" + '" '
        html += 'onblur="setbg(' + "'" + areaID + "'," + "'white');" + '">'
        html += text
        html += '</textarea>'

        return html

    def editRecord(self, rID, data, originFileName, library='', resourceType=''):
        print data
        record = Record(' | | | ' + data)
        newid = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'id'})
        if newid != None:
            newid = newid.strip()
        else:
            newid = rID
        title = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'title', 'library' : library}).strip()
        url = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'url', 'library' : library}).strip()
        desc = data.replace('id:' + newid, '').replace('title:' + title, '').replace('url:' + url, '').strip()
        if url == None:
            url = ''

        newRecord = Record(newid + ' | ' + title + ' | ' + url + ' | ' + desc)
        result = newRecord.editRecord(self.utils, rID, newRecord, originFileName, library, resourceType=resourceType)  

        if result:
            return 'refresh'
        return 'error'   


    def check(self, form_dict):
        rID = form_dict['rID'].strip()
        return rID.startswith('loop') == False or rID.startswith('loop-h')
