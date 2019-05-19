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

    def textFormatConvert(self, textContent):

        newTextContent = textContent.strip()

        textContentList = newTextContent.split('\n')

        if textContentList[0].endswith(':'):

            print textContentList
            group = ''
            convertText = ''
            accountTag = False
            accountType = ''
            accountValue = ''
            for item in textContentList:
                if item == '':
                    continue
                if item.strip().endswith(':'):
                    if self.utils.isAccountTag(item, self.tag.tag_list_account):
                        accountTag = True

                        if accountValue != '' and item != accountType + ':':
                            convertText += accountType + '(' + accountValue[0 : len(accountValue) - 1] + '),\n'
                            accountValue = ''
                            accountType = ''
                        accountType = item.replace(':', '')


                    else:
                        accountTag = False
                        if accountValue != '':
                            convertText += accountType + '(' + accountValue[0 : len(accountValue) - 1] + '),\n'
                            accountValue = ''
                            accountType = ''
                    
                    group = item[0 : item.find(':')]
                elif accountTag:
                    accountValue += item + '*'
                else:
                    key = ''

                    if item.find(' - ') != -1:
                        parts = item.split(' - ')
                        key = parts[0]
                        item = parts[1]
                    else:

                        key = item.replace('https', 'http').replace('http','').replace('://','').replace('www.', '')
                        if key.find('.') != -1:
                            key = key[0 : key.find('.')]

                    convertText += key + '<' + group + '>' + '(' + item + '),\n'


            if accountValue != '':
                convertText += accountType + '(' + accountValue[0 : len(accountValue) - 1] + '),\n'


            convertText = convertText[0 : len(convertText) - 2].strip() + '\n'
            print convertText
            return convertText

        else:
            return textContent


    def excute(self, form_dict):
        print form_dict
        rID = form_dict['rID'].strip()
        rTitle = form_dict['rTitle'].replace('%20', ' ').strip()
        fileName = form_dict['fileName'].strip()
        originFileName = form_dict['originFileName'].strip()
        divID = form_dict['divID']

        if divID.find('-history-') != -1 and divID.find('-content-') != -1:
            fileName = fileName[fileName.rfind('/') + 1 :]
            fileName = os.getcwd() + '/extensions/content/data/' + fileName + '-history-content'
        elif divID.find('-content-') != -1 and divID.find('-edit') != -1:
            originFileName = originFileName[originFileName.rfind('/') + 1 :]
            fileName = os.getcwd() + '/extensions/content/data/' + originFileName + '-content'


        library = form_dict['fileName']

        if form_dict.has_key('textContent'):
            textContent = form_dict['textContent']

            if rID.startswith('loop-h-') or rID.find('plugin') != -1:
                editedData = ''
                textContent = self.textFormatConvert(textContent)

                textContent = textContent.replace(',\n', '+')
                textContent = self.utils.removeDoubleSpace(textContent)
                textContent = textContent.replace(', ', '+')
                textContent = textContent.replace(',', '+')
                textContent = textContent.replace('\n', '')
                editedData = rTitle + '(' + textContent + ')'
                print 'editedData--->' + editedData

                #return 

                historyRecord = None
                r = None
                print rID
                r, historyRecord = self.getRecordByHistory(rID, rTitle, fileName)

                if rID.find('plugin') != -1 and historyRecord == None:
                    pid = rID.replace('custom-plugin-', '')
                    if pid.find('-pg') != -1:
                        pid = pid[0 : pid.find('-pg')]
                    r = self.utils.getRecord(pid, path=fileName, use_cache=False)

                #print historyRecord.line
                #return 'error'

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
                            result = self.editRecord(editRID, self.utils.removeDoubleSpace(newData), originFileName, library=library, resourceType=resourceType, divID=divID)


                            return result

                return 'error'
            
            else:
                textContent = self.utils.removeDoubleSpace(textContent.replace(',\n  ', ', ').replace('\n', ' '))

                print textContent

                return self.editRecord(rID, textContent, originFileName, library=library, divID=divID)
            

            return 'error'


        column = str(form_dict['column'])
        print fileName
        r = None
        if rTitle.startswith('library/') and rID.find('custom-plugin') != -1:
            rTitle = rTitle.replace('==', '->')
            r = self.utils.crossref2Record(rTitle, rID='custom-plugin')
            print r.line 
            fileName = 'db/' + rTitle[0 : rTitle.find('#')]
            originFileName = fileName
            rTitle = r.get_title().strip()
        else:
            if rTitle.startswith('library/'):
                fileName = 'db/' + rTitle[0 : rTitle.find('#')]
                if rTitle.find('==') != -1:
                    rTitle = rTitle[rTitle.find('==') + 2 :]
            r = self.utils.getRecord(rID, path=fileName, use_cache=False)
        print fileName
        html = 'not found'


        areaID = rID.replace(' ', '-').replace('.', '-') + '-area'

        if rID.startswith('loop-h-') or rID.find('plugin') != -1:
            if rID.find('plugin') == -1:
                r, historyRecord = self.getRecordByHistory(rID, rTitle, fileName)

            if r != None:
                #print r.line
                item = ''
                if rID.find('plugin') == -1:
                    item = r.get_desc_field2(self.utils, rTitle, self.tag.get_tag_list(library), library=library)
                else:
                    item = rTitle + '(' + self.utils.desc2ValueText(r.get_describe(), self.tag.get_tag_list(library)) + ')'
                    #rID = rID.replace('custom-plugin-', '')
                    #print 'item:' + item
                    rID = rID.replace('-' + rTitle.lower().strip().replace(' ', '-'), '')


                if item != '':
                    print '---->' + rID + '----' + item

                    text = value = self.utils.getValueOrText(item, returnType='text')
                    value = self.utils.getValueOrText(item, returnType='value')

                    rows, cols = self.getRowsCols(column)
                    html = '<div class="ref">'
                    html += self.genTextareaHtml(rows, cols, areaID, value.replace('+', ',\n'))
                    html += '<br>'
                    html += self.genEditButton(areaID, rID, text, fileName, divID, originFileName)
                    html += '</div>'
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
                end = self.utils.next_pos(desc, start, int(cols), self.tag.get_tag_list(library), library=library, shortPos=True) 
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

            if form_dict.has_key('appendText') and form_dict['appendText'] != '':
                text += '\n' + form_dict['appendText'] + '\n'


            html += self.genTextareaHtml(rows, cols, areaID, text)
            html += '<br>'
            html += self.genEditButton(areaID, rID, rTitle, fileName, divID, originFileName)
        return html

    def getRecordByHistory(self, rid, title, fileName):
        path = fileName[0 : fileName.find('db/')] + 'extensions/history/data/' + fileName[fileName.rfind('/') + 1:] + '-history'
        if os.path.exists(path):
            print path
            print title
            rList = self.utils.getRecord(title, path=path, use_cache=False, accurate=False, matchType=2, return_all=True, log=True)

            if rList != None:
                record = None
                hRecord = None
                for historyRecord in rList:
                    historyRID = historyRecord.get_id().strip()
                    historyTitle = historyRecord.get_title().strip()
                    print 'historyRID:' + historyRID + ' rid:' + rid
                    print 'historyTitle:' + historyTitle + ' title:' + title
                    if historyRID != '':

                        if rid.find(historyRID) != -1:
                            record = self.utils.getRecord(historyRID, path=fileName, use_cache=False)
                            if title == historyTitle:
                                return record, historyRecord
                            else:
                                hRecord = historyRecord
                return record, hRecord

        return None, None

    def genEditButton(self, areaID, rID, rTitle, fileName, divID, originFileName):
        script = "var text = $('#" + areaID + "'); console.log('', text[0].value);"
        script += "var postArgs = {name : 'edit', rID : '" + rID + "', rTitle : '" + rTitle +"', check: 'false', fileName : '" + fileName + "', divID : '" + divID + "', originFileName : '" + originFileName+ "', textContent: text[0].value};";
        linkid = divID.replace('-edit', '').replace('div', 'a')
        if rID.find('plugin') != -1:
            script += "$.post('/extensions', postArgs, function(data) { \
                            a = document.getElementById('searchbox-a');\
                            if (a.text == 'less'){\
                                if (popupMode == false) {\
                                   a.onclick();\
                                   a.onclick();\
                                } else {\
                                    showPopupContent(0, 20, 1444, 900, '>" + rTitle + "');\
                                }\
                            }\
                            });"
        else:
            script += "$.post('/extensions', postArgs, function(data) { \
                            console.log('refresh:' + data);\
                            if (data.indexOf('#') != -1) {\
                                dataList = data.split('#');\
                                if (dataList.length == 3) {\
                                    refreshTab(dataList[2], dataList[1]);\
                                    return;\
                                }\
                            }\
                            search_txt = document.getElementById('search_txt');\
                            if (search_txt != null && search_txt.value != '') {\
                                typeKeyword(search_txt.value, '');\
                            } else {\
                                window.location.href = window.location.href.replace('#', '');\
                            }\
                        });"
        # var a = document.getElementById('" + linkid + "'); var evnt = a['onclick']; evnt.call(a);


        script += 'isEditing = false;'
        html = '<button type="submit" id="edit_btn" hidefocus="true" onclick="' + script + '">submit</button>'

        return html


    def getRowsCols(self, column):
        rows = '25'
        cols = '75'
        if column == '1':
            rows = '40'
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

    def editRecord(self, rID, data, originFileName, library='', resourceType='', divID=''):
        print 'editRecord->' + data
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
            print divID
            if divID.find('-history-') != -1:
                aid = divID[0 : divID.find('-history-')].strip() + '-a-'
                result = 'refresh#history#' + aid
            elif divID.find('-content-') != -1:
                aid = divID[0 : divID.find('-content-')].strip() + '-a-'
                result = 'refresh#content#' + aid

            else:
                result = 'refresh'
        else:
            result = 'error'   

        print 'result--->' + result

        return result



    def check(self, form_dict):
        rID = form_dict['rID'].strip()
        return rID.startswith('loop') == False or rID.startswith('loop-h')
