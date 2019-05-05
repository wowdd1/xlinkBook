#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from config import Config
from private_config import PrivateConfig
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record
from record import Tag
from bs4 import BeautifulSoup
import requests
import os


class Convert(BaseExtension):

    form_dict = None
    convert_data_file = 'web_content/convert_data'
    convert_output_file = ''
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.count = 0
        self.tag = Tag()
        self.statDict = {}
        self.convert_command = ''
        self.resetArgs()

        self.search_keyword_len = 0

        self.crossrefQuery = ''

    def resetArgs(self):
        self.convert_url_is_base = False
        self.convert_url_args = '' #'?start=' #'?start=0&tag='
        self.convert_url_args_2 = ''
        self.convert_next_page = ''
        self.convert_no_url_args_4_1st_page = False
        self.convert_page_step = 1
        self.convert_page_start = 1
        self.convert_page_max = 10
        self.convert_page_to_end = False
        self.convert_tag = '' #"div#title"  # tag#class or tag
        self.convert_min_num = 0
        self.convert_max_num = 1000
        self.convert_filter = ""
        self.convert_contain = ""
        self.convert_start = 0
        self.convert_split_column_number = 0
        self.convert_top_item_number = 0
        self.convert_output_data_to_new_tab = False
        self.convert_output_data_to_temp = False
        self.convert_output_data_format = ''
        self.convert_cut_start = ''
        self.convert_cut_start_offset = 0
        self.convert_cut_end = ''
        self.convert_cut_end_offset = 0
        self.convert_remove = []
        self.convert_replace = {}
        self.convert_append = ''
        self.convert_cut_max_len = 1000
        self.convert_script = ''
        self.convert_script_custom_ui = False
        self.convert_smart_engine = ''
        self.convert_div_width_ratio = 0
        self.convert_div_height_ratio = 0
        self.convert_show_url_icon = False
        self.url_prefix = ''
        self.convert_priority = 0
        self.convert_stat_field = []
        self.convert_stat_enable = False
        self.convert_confirm_argv = False
        self.convert_removal = True
        self.argvStr = ''

        self.convert_pass2 = False

        self.convert_tag_pass2 = ''

        self.highLightText = ''

        self.search_keyword_len = 0

    def resetFormatArgs(self):
        self.convert_cut_start = ''
        self.convert_cut_end = ''
        self.convert_remove = ''
        self.convert_replace = {}
        self.convert_append = ''
        self.convert_cut_max_len = 10000

    def loadDefaultConfig(self):
        self.convert_url_is_base = Config.convert_url_is_base
        self.convert_url_args = Config.convert_url_args #'?start=' #'?start=0&tag='
        self.convert_url_args_2 = Config.convert_url_args_2
        self.convert_next_page = Config.convert_next_page
        self.convert_no_url_args_4_1st_page = Config.convert_no_url_args_4_1st_page
        self.convert_page_step = Config.convert_page_step
        self.convert_page_start = Config.convert_page_start
        self.convert_page_max = Config.convert_page_max
        self.convert_page_to_end = Config.convert_page_to_end
        self.convert_tag = Config.convert_tag #"div#title"  # tag#class or tag
        self.convert_min_num = Config.convert_min_num
        self.convert_max_num = Config.convert_max_num
        self.convert_filter = Config.convert_filter
        self.convert_contain = Config.convert_contain
        self.convert_start = Config.convert_start
        self.convert_split_column_number = Config.convert_split_column_number
        self.convert_top_item_number = Config.convert_top_item_number
        self.convert_output_data_to_new_tab = Config.convert_output_data_to_new_tab
        self.convert_output_data_to_temp = Config.convert_output_data_to_temp
        self.convert_output_data_format = Config.convert_output_data_format  
        self.convert_cut_start = Config.convert_cut_start
        self.convert_cut_start_offset = Config.convert_cut_start_offset
        self.convert_cut_end = Config.convert_cut_end
        self.convert_cut_end_offset = Config.convert_cut_end_offset
        self.convert_cut_to_desc = Config.convert_cut_to_desc
        self.convert_remove = Config.convert_remove
        self.convert_replace = Config.convert_replace
        self.convert_append = Config.convert_append
        self.convert_cut_max_len = Config.convert_cut_max_len
        self.convert_script = Config.convert_script
        self.convert_script_custom_ui = Config.convert_script_custom_ui
        self.convert_smart_engine = Config.convert_smart_engine
        self.convert_div_width_ratio = Config.convert_div_width_ratio
        self.convert_div_height_ratio = Config.convert_div_height_ratio
        self.convert_show_url_icon = Config.convert_show_url_icon
        self.convert_priority = Config.convert_priority
        self.convert_stat_field = Config.convert_stat_field
        self.convert_stat_enable = Config.convert_stat_enable
        self.convert_confirm_argv = Config.convert_confirm_argv
        self.convert_removal = Config.convert_removal

        self.convert_pass2 = Config.convert_pass2
        self.convert_tag_pass2 = Config.convert_tag_pass2

    def initArgs(self, url, resourceType, isEnginUrl=False, argvDict=None, pass2=False):
        self.resetArgs()
        if url.startswith('http') == False:
            if url.find('[') != -1:
                url = url[url.find('(') + 1 : url.find(')')]
        self.loadDefaultConfig()


        if argvDict != None and len(argvDict) > 0:
            self.initArgs2(argvDict)
            return

        items = PrivateConfig.convert_dict.items()
        if isEnginUrl:
            items = Config.convert_engin_dict.items()

        maxLength = 0
        matchedArgs = []
        for k, v in items:
            if url.lower().find(k.lower()) != -1 or (resourceType != '' and k.lower() == resourceType.lower()):
                print 'matched' + k 
                if len(k) > maxLength:
                    maxLength = len(k)
                    matchedArgs = v
        if len(matchedArgs) > 0:
            self.initArgs2(matchedArgs, pass2=pass2)
        #if self.convert_smart_engine == '' and self.utils.search_engin_dict.has_key(k):
        #    self.convert_smart_engine = k


    def initArgs2(self, v, pass2=False):
        print v
        argvStr = ''
        for k, value in v.items():
            if type(value) == list:
                value = '[' + '+'.join(value) + ']'
            argvStr += k + '=' + str(value) + ', '

        self.argvStr = argvStr[0 : len(argvStr) - 2]

        passStr = ''

        if pass2:
            self.loadDefaultConfig()
            passStr = '_pass2'
            print passStr

        if v.has_key('pass2'):
            self.convert_pass2 = v['pass2']


        if v.has_key('url_is_base' + passStr):
            isTrue = 'True' == str(v['url_is_base' + passStr])
            self.convert_url_is_base = isTrue
        if v.has_key('url_args' + passStr):
            self.convert_url_args = v['url_args' + passStr]
        if v.has_key('url_args_2' + passStr):
            self.convert_url_args_2 = v['url_args_2' + passStr]
        if v.has_key('next_page' + passStr):
            self.convert_next_page = v['next_page' + passStr]
        if v.has_key('no_url_args_4_1st_page' + passStr):
            self.convert_no_url_args_4_1st_page = v['no_url_args_4_1st_page' + passStr]
        if v.has_key('page_step' + passStr):
            self.convert_page_step = int(v['page_step' + passStr])
        if v.has_key('page_start' + passStr):
            self.convert_page_start = int(v['page_start' + passStr])             
        if v.has_key('page_max' + passStr):
            self.convert_page_max = int(v['page_max' + passStr])
        if v.has_key('page_to_end' + passStr):
            self.convert_page_to_end = v['page_to_end' + passStr]
        if v.has_key('tag' + passStr):
            self.convert_tag = v['tag' + passStr]   
        if v.has_key('min_num' + passStr):
            self.convert_min_num = int(v['min_num' + passStr])
        if v.has_key('max_num' + passStr):
            self.convert_max_num = int(v['max_num' + passStr])
        if v.has_key('filter' + passStr):
            self.convert_filter = v['filter' + passStr]   
        if v.has_key('contain' + passStr):
            self.convert_contain = v['contain' + passStr]
        if v.has_key('start' + passStr):
            self.convert_start = v['start' + passStr]
        if v.has_key('split_column_number' + passStr):
            self.convert_split_column_number = int(v['split_column_number' + passStr])
        if v.has_key('top_item_number' + passStr):
            self.convert_top_item_number = v['top_item_number' + passStr]
        if v.has_key('output_data_to_new_tab' + passStr):
            isTrue = 'True' == str(v['output_data_to_new_tab' + passStr])
            self.convert_output_data_to_new_tab = isTrue  
        if v.has_key('output_data_to_temp' + passStr):
            isTrue = 'True' == str(v['output_data_to_temp' + passStr])
            self.convert_output_data_to_temp = isTrue 
        if v.has_key('output_data_format' + passStr):
            self.convert_output_data_format = v['output_data_format' + passStr]   
        if v.has_key('cut_start' + passStr):
            self.convert_cut_start = v['cut_start' + passStr] 
        if v.has_key('cut_start_offset' + passStr):
            self.convert_cut_start_offset = v['cut_start_offset' + passStr] 
        if v.has_key('cut_end' + passStr):
            self.convert_cut_end = v['cut_end' + passStr] 
        if v.has_key('cut_end_offset' + passStr):
            self.convert_cut_end_offset = int(v['cut_end_offset' + passStr])
        if v.has_key('cut_to_desc' + passStr):
            self.convert_cut_to_desc = v['cut_to_desc' + passStr]
        if v.has_key('remove' + passStr):
            self.convert_remove = v['remove' + passStr] 
        if v.has_key('replace' + passStr):
            self.convert_replace = v['replace' + passStr]
        if v.has_key('append' + passStr):
            self.convert_append = v['append' + passStr]
        if v.has_key('cut_max_len' + passStr):
            self.convert_cut_max_len = int(v['cut_max_len' + passStr])
        if v.has_key('script' + passStr):
            self.convert_script = v['script' + passStr] 
        if v.has_key('script_custom_ui' + passStr):
            isTrue = 'True' == str(v['script_custom_ui' + passStr])
            self.convert_script_custom_ui = isTrue
        if v.has_key('smart_engine' + passStr):
            self.convert_smart_engine = v['smart_engine' + passStr] 
        if v.has_key('div_width_ratio' + passStr):
            self.convert_div_width_ratio = v['div_width_ratio' + passStr] 
        if v.has_key('div_height_ratio' + passStr):
            self.convert_div_height_ratio = v['div_height_ratio' + passStr] 
        if v.has_key('show_url_icon' + passStr):
            isTrue = 'True' == str(v['show_url_icon' + passStr])
            self.convert_show_url_icon = isTrue
        if v.has_key('priority' + passStr):
            self.convert_priority = v['priority' + passStr]
        if v.has_key('stat_field' + passStr):
            if type(v['stat_field']) != list:
                self.convert_stat_field = [v['stat_field' + passStr]]
            else:
                self.convert_stat_field = v['stat_field' + passStr]
        if v.has_key('stat_enable' + passStr):
            isTrue = 'True' == str(v['stat_enable' + passStr])
            self.convert_stat_enable = isTrue

        if v.has_key('confirm_argv' + passStr):
            isTrue = 'True' == str(v['confirm_argv' + passStr])
            self.convert_confirm_argv = isTrue

        if v.has_key('removal' + passStr):
            isTrue = 'True' == str(v['removal' + passStr])
            self.convert_removal = isTrue



    def processData(self, data, dataToTemp=False, dataStat=False, appendToTemp=False, highLight=True):
        result = ''
        info = ''

        datas = data.split('\n')
        self.statDict = {}

        if len(datas) <= self.convert_split_column_number:
            self.convert_cut_max_len = 1000
        elif len(datas) <= (self.convert_split_column_number * 2):
            self.convert_cut_max_len += self.convert_cut_max_len / 2
        for line in datas:
            if line.strip() == '':
                continue
            #print line
            r = Record(line)
            url = r.get_url().strip()
            desc = r.get_describe().strip()

            if self.convert_contain != '' and line.lower().find(self.convert_contain.lower()) == -1:
                #print line
                continue

            if self.convert_filter != '' and line.lower().find(self.convert_filter.lower()) != -1:
                continue

            if url.find('twitter') != -1:
                info += url[url.rfind('/') + 1 :] + ', '

            title = r.get_title().strip()


            if title != '':
                title = self.customFormat(title)
                newUrl = url

                if self.convert_smart_engine != '':
                    if url == '' or (self.convert_smart_engine != 'glucky' and url.find('btnI=') != -1):
                        newUrl = self.utils.toQueryUrl(self.utils.getEnginUrl(self.convert_smart_engine), title)

                if highLight and self.highLightText != '':
                    highLightTextList = self.highLightText.replace('#and', '#').replace('#or', '#').replace('#not', '#').split('#')
                    #print highLightTextList
                    for ht in highLightTextList:
                        ht = ht.strip()
                        if '<i><strong></strong></i>'.find(ht.lower()) == -1:
                            title = self.utils.replaceEx(title, ht, '<i><strong>' + ht + '</strong></i>')
                #print title + ' ' + self.highLightText + '111'

                if self.convert_cut_to_desc != '':
                    if title.find(self.convert_cut_to_desc) != -1:
                        cut2Desc = title[title.find(self.convert_cut_to_desc) : ]
                        #print 'cut2Desc:' + cut2Desc
                        title = title[0 : title.find(self.convert_cut_to_desc)]
                        desc += ' description:' + cut2Desc.strip()

                line = r.get_id().strip() + ' | ' + title + ' | ' + newUrl + ' | ' + desc

                result += line.encode('utf-8') + '\n'

            if dataStat and len(self.convert_stat_field) > 0:
                self.statistics(Record(line))

        if dataStat and len(self.statDict) > 0:
            result = self.getStatisticsData(self.statDict)

        if dataToTemp and self.convert_output_data_to_new_tab == False:
            flag = 'w'
            if self.form_dict['fileName'].find('exclusive') != -1 and Config.exclusive_append_mode:
                flag = 'a'
            if appendToTemp:
                flag = 'a'
            self.write2DataFile(result, flag)

        print info[0 : len(info) - 2]

        return result

    def write2DataFile(self, data, flag):
        f = open(self.convert_data_file, flag)
        #f.write(self.utils.clearHtmlTag(line) + '\n')
        f.write(data + '\n')
        f.close()       

    def getStatisticsData(self, statDict):
        data = ''
        enginData = ''
        allLinks = ''
        if len(statDict) > 0:
            print statDict.keys()
            for item in sorted(statDict.items(), key=lambda statDict:int(len(statDict[1])), reverse=True):
            #for item in self.statDict.items():
                website = 'website:'
                keyDict = {}
                for key in sorted(item[1], reverse=True):
                    if keyDict.has_key(key):
                        continue
                    else:
                        keyDict[key] = key
                    website += key + ', '

                    hTitle = self.utils.getValueOrText(key, returnType='text')
                    hUrl = self.utils.getValueOrText(key, returnType='value')

                website = website.strip()
                if website.endswith(','):
                    website = website[0 : len(website) - 1]
                title = item[0]
                if title.startswith('http'):
                    title = item[0][item[0].find('//') + 2 : item[0].rfind('.')]
    
                data += ' | ' +  str(len(item[1])) + ' -- ' + title + ' | ' + item[0] + ' | ' + website + '\n'

                allLinks += title + '(' + item[0] + ')+'

                enginList = [item[0][item[0].find('//') + 2 : item[0].find('.')], item[0][item[0].find('//') + 2 :]]
                for engin in enginList:
                    if self.utils.search_engin_dict.has_key(engin):
                        enginData += engin + ' '

        if enginData != '':
            print ''
            print '---->enginData<----'
            print enginData
            print ''
            print allLinks[0 : len(allLinks) - 1]
            #data += ' | ' + enginData + ' | | \n' 

        return data

    def statistics(self, record):
        #print record.line
        #print self.convert_stat_field
        url = record.get_url().strip()
        for field in self.convert_stat_field:
            urlList = []
            textList = [] 

            if field == 'url':
                if url == '':
                    return
                urlList.append(url)
                textList.append(record.get_title().strip())
            else:
                #print record.line
                fieldValue = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : field})
                #print fieldValue
                if fieldValue != None:
                    fieldValue = fieldValue.strip()
                    if field == 'website':
                        fieldValue = fieldValue.strip()
                        fieldValueList = fieldValue.split(',')
        
                        for fv in fieldValueList:
                            fv = fv.strip()
                            
                            urlList.append(self.utils.getValueOrText(fv, returnType='value'))
                            textList.append(self.utils.getValueOrText(fv, returnType='text'))
                    else:
                        if url == '':
                            url = self.utils.toQueryUrl(self.utils.getEnginUrl('glucky'), record.get_title().strip())
                        urlList.append(url)
                        textList.append(fieldValue)


            for i in range(0, len(urlList)):
                text = textList[i]
                url = urlList[i]
                statKey = ''

                if field == 'website' or field == 'url':

                    if url.startswith('http') == False:
                        continue
                    url = url.replace('https', 'http').replace('www.', '')
                    statKey = url
                    index = url.find('/', url.find('://') + 3)
                    if index != -1:
                        statKey = url[0 : index].strip()
                    if text == '':
                        text = 'link'
                    if text.startswith('http'):
    
                        if text.find(',') != -1:
                            text = text.replace(',', '')
                        linkText = text
                        if linkText.endswith('/'):
                            linkText = linkText[0 : len(linkText) - 1]
                        if linkText.find('/') != -1:
    
                            linkText = linkText[linkText.rfind('/') + 1 : ]
                            
                        linkText = linkText.replace('"', '').replace("'", '')
                        if len(urlList) == 1 and len(linkText) > 60:
                            linkText = linkText[0 : 60]
                        elif len(urlList) > 1 and len(linkText) > 15:
                            linkText = linkText[0 : 15]
    
                        text = linkText
    
            
                    if url.endswith('/') == False:
                        url += '/'
                    text = text.replace('%20', ' ').replace('%', '').strip().replace('+', ' ').replace(':', ' ')

                else:
                    statKey = text
                    text = record.get_title().strip()


                if self.statDict.has_key(statKey):
                    self.statDict[statKey].append(text + '(' + url + ')')
                else:
                    self.statDict[statKey] = [text + '(' + url + ')']
    
    def excute(self, form_dict):
        print 'excute'
        print form_dict
        #return 'xx'
        self.form_dict = form_dict
        resourceType = ''
        if form_dict.has_key('resourceType'):
            resourceType = form_dict['resourceType'].encode('utf8')

        if form_dict.has_key('crossrefQuery'):
            self.crossrefQuery = form_dict['crossrefQuery'].encode('utf8').replace('%20', ' ')

        url = form_dict['url'].encode('utf8')
        record = None
        batchPreview = False
        if form_dict['fileName'].strip() != '':
            record = self.utils.getRecord(form_dict['rID'], path=form_dict['fileName'], use_cache=False)

        if form_dict.has_key('preview'):
            batchPreview = form_dict['preview']

        argvDict = None
        if form_dict.has_key('argvStr'):
            argvDict = self.initArgvDict(form_dict['argvStr'])

        self.initArgs(url, resourceType, isEnginUrl=False, argvDict=argvDict)

        if self.convert_confirm_argv and record != None and self.argvStr != '' and record.get_describe().find('argv:') == -1:
            sourceExtension = 'convert'
            targetExtension = 'edit'
            form_dict['appendText'] = 'argv:' + self.argvStr
            #print form_dict
            #return 'xx'
            return self.utils.toExtension(sourceExtension, targetExtension, form_dict)


        urlList = []
        enginUrlList = []
        allUrl = []
        if url.find(',') != -1:
            allUrl = url.split(',')
        else:
            allUrl = [url]
        print allUrl
        for u in allUrl:
            u = u.replace('%20', ' ').strip()
            if u.startswith('http'):
                urlList.append(u)
            elif u.startswith('[') and u.find(']') != -1:
                if u.find('http') != -1:
                    urlList.append(u)
                else:
                    keyword = u[u.find('[') + 1 : u.find(']')]
                    engin = u[u.find('(') + 1 : u.find(')')]
                    for k in keyword.split('*'):
                        enginUrlList.append(self.utils.toQueryUrl(self.utils.getEnginUrl(engin), k))
 
            elif self.utils.search_engin_dict.has_key(u):
                enginUrlList.append(self.utils.toQueryUrl(self.utils.getEnginUrl(u), form_dict['rTitle'].strip()))
 
        print ','.join(urlList)
        print ','.join(enginUrlList)
        html = ''
        if len(urlList) > 0:

            urlGroup = {}
            for urlItem in urlList:
                key = urlItem[0 : 30] + '-' + str(len(urlItem))
                if urlGroup.has_key(key):
                    urlGroup[key].append(urlItem)
                else:
                    urlGroup[key] = [urlItem]
            print 'urlGroup:'
            print urlGroup

            print 'self.convert_output_data_to_temp:' + str(self.convert_output_data_to_temp)
            if len(urlGroup) > 1 and form_dict.has_key('command') == False:
                allData = ''
                count = 0
                for k, v in urlGroup.items():
                    count += 1
                    print ','.join(v)
                    self.initArgs(v[0], resourceType, isEnginUrl=False, argvDict=argvDict)
                    data = self.doConvert(','.join(v), form_dict, resourceType, isEnginUrl=False, record=record, genHtml=False)

                    appendToTemp = False
                    if count > 1:
                        appendToTemp = True
                    allData += self.processData(data, dataToTemp=self.convert_output_data_to_temp, dataStat=self.convert_stat_enable, appendToTemp=appendToTemp)

                if allData != '':
                     divID = form_dict['divID'].encode('utf8')
                     rID = form_dict['rID'].encode('utf8')
                     if batchPreview:
                        return self.genBatchPreviewHtml(allData)
                     else:
                        html = self.genHtml(allData, divID, rID, resourceType)
                        return html

                else:
                    return allData

            else:
                #for url in urlList:
                if batchPreview:
                    return self.genBatchPreviewHtml(self.doConvert(url, form_dict, resourceType, isEnginUrl=False, record=record, genHtml=False))
                else:
                    html += self.doConvert(url, form_dict, resourceType, isEnginUrl=False, record=record)

        if len(enginUrlList) > 0:
             html += self.doConvert(url, form_dict, resourceType, isEnginUrl=True, record=record)


        if self.crossrefQuery != '':
            if form_dict.has_key('command') == False or (form_dict.has_key('command') and form_dict['command'] == ''):
                form_dict['command'] = self.getDefaultCMD()
                form_dict['fileName'] = self.convert_data_file
            #form_dict['divID'] = ''
            return self.doConvert(url, form_dict, resourceType, isEnginUrl=True, record=record)

        return html


    def genBatchPreviewHtml(self, allData):
        html = ''

        titleList = []
        urlList = []
        for data in allData.split('\n'):
            data = data.strip()

            if data != '':
                r = Record(data)
                title = r.get_title().strip()
                url = r.get_url().strip()
                titleList.append(title)
                urlList.append(url)

        if len(titleList) > 0:
            htmlList, notSuportLink = self.utils.genAllInOnePage(titleList, urlList, frameCheck=False, column=2, changeBG=False, hindenLinks=True)
            if len(htmlList) > 0:
                html = htmlList[0]


        return html


    def initArgvDict(self, argvStr):
        if argvStr == '':
            return None
        argvDict = {}
        for item in argvStr.split(','):
           #argvList = item.strip().split('=')
           argvList = []
           argvList.append(item[0 : item.find('=')].strip())
           argvList.append(item[item.find('=') + 1 :].strip())
           if argvList[1].find('[') != -1 and argvList[1].find(']') != -1:
               argvList[1] = argvList[1][1: len(argvList[1]) - 1].split('+')
           argvDict[argvList[0]] = argvList[1]

        return argvDict

    def doConvert(self, url, form_dict, resourceType, isEnginUrl=False, record=None, genHtml=True, pass2=False):
        argvDict = None

        r = record
        if r != None:
            desc = r.get_describe()
            if desc.find(' argv:') != -1:
                argv = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : 'argv'})
                if argv != None:
                    argvDict = self.initArgvDict(argv)

        if form_dict.has_key('argvStr'):
            argvDict = self.initArgvDict(form_dict['argvStr'])

        self.initArgs(url, resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict, pass2=pass2)
        if form_dict.has_key('command') and form_dict['command'] != '':
            if url.find('[') != -1 and url.find(']') != -1:
                if url.startswith('['):
                    self.initArgs(url[url.find('(') + 1 : url.find(')')], resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict)
                else:
                    self.initArgs(url, resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict)
            command = form_dict['command']
            if command.startswith('./') == False:
                source = ''
                if form_dict.has_key('fileName') and form_dict['fileName'] != '':
                    source = form_dict['fileName']
                else:
                    source = self.convert_data_file
                    form_dict['fileName'] = source
                self.resetFormatArgs()
                form_dict['command'], form_dict['commandDisplay'] = self.buildCmd('list.py', source, args=form_dict['command'])
            else:
                form_dict['fileName'] = '' 
            return self.runCommand(form_dict, dataStat=self.convert_stat_enable, genHtml=genHtml)
        elif url.find(Config.ip_adress) != -1:
            urlList = [url]
            allData = ''
            if url.find('[') != -1 and url.find(']') != -1:
                value, urlList = self.genUrlList(url)
                self.initArgs(value, resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict)     

            for link in urlList:
                print link
                db = link[link.find('db=') + 3 : ]
                if db.find('&') != -1:
                    db = db[0 : db.find('&')]
    
                key = link[link.find('key=') + 4 :]
                if key.find('&') != -1:
                    key = key[0 : key.find('&')]
    
                form_dict['command'], form_dict['commandDisplay'] = self.buildCmd('list.py', 'db/' + db + key)
                form_dict['fileName'] = 'db/' + db + key
    
                print form_dict
                allData += self.runCommand(form_dict, dataStat=self.convert_stat_enable, genHtml=genHtml)

            return allData


        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')

        #print self.convert_remove
        #print 'convert_script:' + self.convert_script
        html = ''
        if self.convert_script != '':
            allData = ''
            data = ''
            urlList = [url]
            if url.find('[') != -1 and url.find(']') != -1:
                value, urlList = self.genUrlList(url)
                self.initArgs(value, resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict)

            for u in urlList:
                pageArgv = ''
                if self.convert_script == 'convert_weixin.py':
                    pageArgv = ' -p ' + + str(self.convert_page_max)
                cmd = './extensions/convert/' + self.convert_script + ' -u "' + u + '" -q "' + self.crossrefQuery + '" ' + pageArgv 
                data = ''
                self.convert_command = cmd.replace('"', "'")
                cmdList = self.cmd2CmdList(cmd)
                for cmd in cmdList:
                    data += self.execCommand(cmd, cmdNum=len(cmdList))

                print 'convert_script_custom_ui:' + str(self.convert_script_custom_ui)
                print 'data:' + data

                allData += data
            if self.convert_script_custom_ui:
                return allData.replace('\n', '<br>')
            else:
                if genHtml:
                    return self.genHtml(self.processData(allData, dataToTemp=self.convert_output_data_to_temp, dataStat=self.convert_stat_enable), divID, rID, resourceType)
                else:
                    return allData
        else:
            if url.startswith('http') and self.convert_tag == '':
                return self.genCommandBox()

            if url == '':
                url = self.utils.bestMatchEnginUrl(form_dict['rTitle'].encode('utf8'))
            if self.convert_url_args != '':
                url += self.convert_url_args
            print url

            step = self.convert_page_start
            #new_url = url
            new_url = url

            if self.convert_url_args != '':

                if self.convert_url_args.find('%s') != -1:
                    new_url = url.replace('%s', str(step))
                else:
                    new_url = url + str(step)
            if self.convert_url_args_2 != '':
                new_url += self.convert_url_args_2

            page_count = 0
            #print new_url
            #print url
            print self.convert_page_step
            print self.convert_url_args
            all_data = ''
            if self.convert_page_step > 0 and self.convert_url_args != '':
                all_data = self.convertPages2data(url)
                if genHtml and all_data != '':
                    return self.genHtml(self.processData(all_data, dataToTemp=self.convert_output_data_to_temp, dataStat=self.convert_stat_enable), divID, rID, resourceType)
                else:
                    return all_data
            elif self.convert_next_page != '':

                if self.convert_next_page.find('#') != -1:
                    args = self.convert_next_page.split('#')
                    base_url = new_url
                    if base_url.endswith('/'):
                        base_url = base_url[0 : len(base_url) - 1]
                    if base_url.find('/', base_url.find('//') + 2) != -1:
                        base_url = base_url[0 : base_url.find('/', base_url.find('//') + 2)]
                    data = self.convert2data(new_url, originUrl=url)
                    page_count += 1
                    if data != '':
                        all_data += data + '\n'
  
                        while True:
                            headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
                            r = requests.get(new_url, headers=headers)
                            #print url + ' **'
                            sp = BeautifulSoup(r.text)

                            nextLink = sp.find(args[0], class_=args[1])

                            if nextLink == None:
                                break

                            if nextLink.a != None:
                                nextLink = nextLink.a

                            if nextLink != None:
                                if nextLink['href'].startswith('http') == False and self.convert_url_is_base:
                                    if nextLink['href'].startswith('/'):
                                        new_url = base_url + '/' + nextLink['href'][1:]
                                    else:
                                        new_url = base_url + '/' + nextLink['href']
                                else:
                                    new_url = nextLink['href']


                                print new_url
                                data = self.convert2data(new_url, originUrl=url)
                                if data != '' and data != None:
                                    all_data += data + '\n'
                                    page_count += 1
                                    if page_count >= self.convert_page_max:
                                        break
                                elif data == '':
                                    if self.convert_page_to_end == False:
                                        break
                            else:
                                break

                    if genHtml and all_data != '':
                        return self.genHtml(self.processData(all_data, dataToTemp=self.convert_output_data_to_temp, dataStat=self.convert_stat_enable), divID, rID, resourceType)
                    else:
                        return all_data


            else:
                data = ''
                if url.find('[') != -1 and url.find(']') != -1:
                    value, urlList = self.genUrlList(url)
                    self.initArgs(value, resourceType, isEnginUrl=isEnginUrl, argvDict=argvDict)

                    for u in urlList:
                        #print u
                        if self.convert_page_step > 0 and self.convert_url_args != '':
                            data += self.convertPages2data(u)
                        else:
                            data += self.convert2data(u, originUrl=url)

                elif url.find(',') != -1:
                    for u in url.split(','):
                        u = u.strip()
                        if u.startswith('http'):
                            data += self.convert2data(u, originUrl=url)
                else:
                    data = self.convert2data(new_url, originUrl=url)
                if genHtml:
                    html = self.genHtml(self.processData(data, dataToTemp=self.convert_output_data_to_temp, dataStat=self.convert_stat_enable), divID, rID, resourceType)
                else:
                    html = data
        return html

    def execCommand(self, cmd, cmdNum=1):
        print 'cmd ----> ' + cmd.replace('"', "'")  + ' <----'

        if cmdNum == 1:
            self.convert_command = cmd.replace('"', "'")

        data = subprocess.check_output(cmd, shell=True)

        #print 'execCommand:' + data
        return data



    def genUrlList(self, url):
        urlList = []
        value = ''
        if url.find('[') != -1 and url.find(']') != -1:
            keys = []
            if url.startswith('['):
                args = url[1 : url.find(']')]

                keys = self.utils.splitText(args)
                value = url[url.find('(') + 1 : url.find(')')]
            else:
                part1 = url[0 : url.find('[')]
                part2 = url[url.find(']') + 1 : ]
                args = url[url.find('[') + 1 : url.find(']')]
                keys = self.utils.splitText(args)

                value = part1 + '%s' + part2
            for k in keys:
                if value.find('%s') != -1:
                    u = value.replace('%s', k)
                    urlList.append(u)
                else:
                    urlList.append(value + k)
            return value, urlList

        return url, [url]

    def getDefaultCMD(self, fileName=''):
        print 'getDefaultCMD:' + fileName
        filterStr = ''
        if self.crossrefQuery != '':
            if self.crossrefQuery.startswith(':'):
                filterStr = self.unfoldFilter(self.crossrefQuery)
            elif self.crossrefQuery.startswith('>'):
                filterStr = self.processCommand(self.crossrefQuery)

        engin = self.convert_smart_engine
        command = "-f '" + filterStr + "' -e '" + engin + "' --cut_max_len " + str(self.convert_cut_max_len) + " --split " + str(self.convert_split_column_number) + " --search_keyword_len 0 --append ''"
        return command

    def genCommandBox(self, command='', fileName='', inputID='command_txt', buttonID='command_btn', inputSize='46'):
        if inputID == 'command_txt' and command.startswith('./'):
            command = ''
        if command == '':
            command = self.getDefaultCMD(fileName=fileName)
        if command .find('--') == -1:
            command += " --cut_max_len 0 --split 0 --search_keyword_len 0"


        script = "var text = $('#" + inputID + "'); console.log('', text[0].value);"
        divID = self.form_dict['divID']
        script += "var dataDiv = $('#" + divID + "'); dataDiv.html('');"

        script += "var postArgs = {name : 'convert', command : text[0].value, rTitle : '', 'url' : '" + self.form_dict['url'] + "', check: 'false', fileName : '" + fileName + "', 'divID' : '" + divID + "'};";
        script += "var animID = showLoading('search_preview');"
        script += "$.post('/runCommand', postArgs, function(data) { \
                        stopLoading(animID);\
                        console.log('refresh:' + data);\
                        if (data.indexOf('#') != -1) {\
                            divID = data.substring(0, data.indexOf('#'));\
                            html = data.substring(data.indexOf('#') + 1);\
                            $('#'+ divID).html(html);\
                        } else {\
                            dataDiv.html(data);\
                        };\
                        });"
        box = '<br><div style="text-align:center;width:100%;margin: 0px auto;"><input id="' + inputID + '" style="border-radius:5px;border:1px solid" maxlength="256" tabindex="1" size="' + inputSize + '" name="word" autocomplete="off" type="text" value="' + command + '">&nbsp;&nbsp;'\
              '&nbsp;&nbsp;<button alog-action="g-search-anwser" type="submit" id="' + buttonID + '" hidefocus="true" tabindex="2" onClick="' + script + '">Run</button></div>'
        return box

    def runCommand(self, form_dict, dataStat=False, genHtml=True):
        cmd = form_dict['command']
        if form_dict.has_key('commandDisplay') == False:
            form_dict['commandDisplay'] = cmd
        result = ''
        self.convert_command = cmd.replace('"', "'")
        cmdList = self.cmd2CmdList(cmd)
        for cmd in cmdList:
    
            data = self.execCommand(cmd, cmdNum=len(cmdList))
            #print data
    
            
            for line in  data.split('\n'):
                line = line[line.find(' ') + 1 :].strip()
    
                if line != '' and line.find('ecords, File:') == -1:
                    #r = Record(line)
                    result += line + '\n'
    
        if genHtml and result != '':
            doPass2 = True
            if cmd.find('list.py') != -1:
                doPass2 = False
            result =  self.genHtml(self.processData(result, dataToTemp=False, dataStat=dataStat), '', '', '', command=form_dict['commandDisplay'], fileName=form_dict['fileName'], doPass2=doPass2)

            if form_dict['divID'] != '':
                if form_dict['divID'] == 'search_preview':
                    result = form_dict['divID'] + '#' + result
                else:
                    result = form_dict['divID'] + '-data#' + result

        return result

    def cmd2CmdList(self, cmd):
        cmdList = []
        if cmd.startswith('./convert') or cmd.startswith('./extensions/convert'):
            argv = '-i'
            if cmd.startswith('./extensions/convert'):
                argv = '-u'
            url = self.getCmdArg(cmd, argv)
            urlList = [url]
            if url.find('[') != -1 and url.find(']') != -1:
                cmdList = []
                value, urlList = self.genUrlList(url)
            elif url.find(',') != -1:
                urlList = url.split(',')

            for u in urlList:
                u = u.strip()
                if u.startswith('%20'):
                    u = u[3:]
                if u != '':
                    cmdList.append(self.replaceCmdArg(cmd, argv, u))

        print cmdList
        if len(cmdList) == 0:
            return [cmd]
        return cmdList


    def buildCmd(self, script, source, args=''):
        cmd = ''
        cmdDisplay = ''

        if source != '' and args.find(' -e ') == -1:
            for item in PrivateConfig.convert_source2engine_dict.items():
                if source.lower().find(item[0].lower()) != -1:
                    self.convert_smart_engine = item[1]
                    break
        if script == 'convert.py':

            cmd = './' + script + ' -i "' + source + '" '

            if self.convert_url_is_base != False:
                cmd += '-b ' + str(self.convert_url_is_base) + ' '

            if self.convert_tag != '':
                cmd += '-t "' + self.convert_tag + '" '
            if self.convert_min_num >= 0:
                cmd += '-n ' + str(self.convert_min_num) + ' '
            if self.convert_max_num >= 0:
                cmd += '-m ' + str(self.convert_max_num) + ' '

            if self.convert_filter != '':
                cmd += '-f "' + self.convert_filter + '" '
            if self.convert_contain != '':
                if self.convert_contain.find('"') != -1:
                    cmd += "-c '" + self.convert_contain + "' "
                else:
                    cmd += '-c "' + self.convert_contain + '" '
            if self.convert_start > 0:
                cmd += '-s ' + str(self.convert_start) + ' '
            if Config.delete_from_char != '':
                cmd += '-d "' + Config.delete_from_char + '" '

            if self.convert_removal == False:
                cmd += '-r "' + str(self.convert_removal) + '" '

        elif script == 'list.py':
            cmd = './' + script + " -i '" + source + "' " + args
            cmdDisplay += args
            if cmd.find(' -b ') == -1:
                cmd += " -b 'raw' "
            if cmd.find(' -f ') == -1:
                cmd += " -f '" + self.convert_contain + "' "
                cmdDisplay += " -f '" + self.convert_contain + "' "
            if cmd.find(' -e ') == -1:
                cmd += " -e '" + self.convert_smart_engine + "' "
                cmdDisplay += " -e '" + self.convert_smart_engine + "' "
            else:
                engin = cmd[cmd.find(' -e') + 3 :].strip().replace('"', '').replace("'", '')
                if engin.find(' -') != -1:
                    engin = engin[0 : engin.find(' -')].strip()
                for e in engin.split(' '):
                    if e.find('d:') == -1:
                        self.convert_smart_engine = engin
                        break

            if cmd.find(' -n ') == -1 and self.convert_min_num >= 0:
                cmd += ' -n ' + str(self.convert_min_num) + ' '
            if cmd.find(' -m ') == -1 and self.convert_max_num >= 0:
                cmd += ' -m ' + str(self.convert_max_num) + ' '


            print 'source:' + source
            if source == self.convert_data_file or source.find('db/') != -1:
                if cmd.find(' --merger ') != -1:
                    mergerFile = self.getCmdArg(cmd, '--merger')
                    cmd = self.removeCmdArg(cmd, '--merger')

                    if mergerFile != '':

                        files = []
                        if mergerFile.find(' ') != -1:
                            files = mergerFile.split(' ')
                        else:
                            files = [mergerFile]
                        for f in files:
                            if f.startswith('db/') == False:
                                f = 'db/' + f
                            if os.path.exists(f):
                                print 'mergerFile:' + f
                                mergerCmd = 'cat ' + f + ' >> ' + self.convert_data_file
                                print mergerCmd
                                data = subprocess.check_output(mergerCmd, shell=True)

                        cmdDisplay = self.removeCmdArg(cmdDisplay, '--merger')

                if cmd.find('--output') != -1:
                    self.convert_output_file = self.getCmdArg(cmd, '--output')
                    print self.convert_output_file
                    if self.convert_output_file != '':
                        command = 'cp ' + self.convert_data_file  + ' ' + self.convert_output_file
                        data = subprocess.check_output(command, shell=True)
       
                    cmd = self.removeCmdArg(cmd, '--output')
                    cmdDisplay = self.removeCmdArg(cmdDisplay, '--output')

                if cmd.find('--split') != -1:
                    value = int(self.getCmdArg(cmd, '--split'))
                    if value > 0:
                        self.convert_split_column_number = value
                    cmd = self.removeCmdArg(cmd, '--split')

                if cmd.find('--cut_max_len') != -1:
                    value = int(self.getCmdArg(cmd, '--cut_max_len'))
                    if value > 0:
                        self.convert_cut_max_len = value
                    cmd = self.removeCmdArg(cmd, '--cut_max_len')

                if cmd.find('--search_keyword_len') != -1:
                    value = int(self.getCmdArg(cmd, '--search_keyword_len'))
                    if value > 0:
                        self.search_keyword_len = value
                    cmd = self.removeCmdArg(cmd, '--search_keyword_len')

                if cmd.find('--append') != -1:
                    value = self.getCmdArg(cmd, '--append')
                    if value != '':
                        self.convert_append = value
                    cmd = self.removeCmdArg(cmd, '--append')


                if cmd.find('-f') != -1:
                    self.highLightText = self.getCmdArg(cmd, '-f').strip()
                    print 'highLightText:' + self.highLightText

                    if self.highLightText.startswith(':') or self.highLightText.startswith('>'):
                        if self.highLightText.startswith(':'):
                            self.highLightText = self.unfoldFilter(self.highLightText)
                        elif self.highLightText.startswith('>'):
                            self.highLightText = self.processCommand(self.highLightText)

                        index = cmd.find(' -f ')
                        cmd = self.removeCmdArg(cmd, '-f')

                        cmd = cmd[0: index] + ' -f "' + self.highLightText + '" ' + cmd[index : ] 


        print 'build cmd ----> ' + cmd.replace('"', "'") + ' <----'
        print 'cmdDisplay ----> ' + cmdDisplay + ' <----'


        return cmd, cmdDisplay

    def processCommand(self, cmd, connectSrt='#or'):
        print 'processCommand:' + cmd
        result = cmd
        descList = self.utils.processCommand(cmd.strip(), '', returnMatchedDesc=True)
        if len(descList) > 0:
            desc = ''
            for item in descList:
                desc = self.utils.mergerDesc(desc, item[1])
            if desc.find('alias:') != -1:
                line = ' | | | ' + desc
                alias = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'alias:'})

                print 'alias:' + alias
                result = self.utils.removeDoubleSpace(alias.replace(',', ' ' + connectSrt + ' '))

        return result


    def unfoldFilter(self, cmd, connectSrt='#or'):
        cmd = self.utils.unfoldFilter(cmd, PrivateConfig.convert_command_dict, unfoldAll=False)  
        if cmd.find(' + ') != -1:
            cmd = cmd.replace('+', ' ' + connectSrt + ' ')

        return cmd


    def getCmdArg(self, cmd, arg):
        value = cmd[cmd.find(arg) + len(arg) :].replace('"', '').replace("'", '')
        if value.find(' -') != -1:
            value = value[0 : value.find(' -')].strip()

        return value
       

    def removeCmdArg(self, cmd, arg):
        cmd1 = cmd[0 : cmd.find(' ' + arg)]
        cmd2 = ''
        index = cmd.find(' -', cmd.find(' ' + arg) + len(arg) + 1)
        if index != -1:
            cmd2 = cmd[index :]
        cmd = cmd1 + cmd2 

        return cmd.strip()

    def replaceCmdArg(self, cmd, arg, argStr):
        cmd1 = cmd[0 : cmd.find(' ' + arg)]
        cmd2 = ''
        index = cmd.find(' -', cmd.find(' ' + arg) + len(arg) + 1)
        if index != -1:
            cmd2 = cmd[index :]
        cmd = cmd1 + ' ' + arg + " '" + argStr + "' " + cmd2 

        return cmd.strip()

    def convertPages2data(self, url):
        step = self.convert_page_start
        #new_url = url
        new_url = url

        if self.convert_url_args != '':
            new_url = url + str(step)
        if self.convert_url_args_2 != '':
            new_url += self.convert_url_args_2
        all_data = ''
        count = 0
        while True:
            print new_url
            data = ''
            if self.convert_no_url_args_4_1st_page and count == 0:
                urlTemp = new_url
                if self.convert_url_args != '':
                    urlTemp = new_url[0 : new_url.rfind(self.convert_url_args)]

                    print 'urlTemp:' + urlTemp
                data = self.convert2data(urlTemp)
            else:
                data = self.convert2data(new_url)
            count += 1
            if data != '' and data != None:
                all_data += data + '\n'
            elif data == '':
                #print new_url + ' xxx'
                if self.convert_page_to_end == False:
                    break
            step += self.convert_page_step
            if step > self.convert_page_max:
                break
            if self.convert_url_args != '':
                new_url = url + str(step)
            if self.convert_url_args_2 != '':
                new_url += self.convert_url_args_2

        return all_data


    def convert2data(self, url, originUrl=''):

        self.url_prefix = url[0 : url.find('/', url.find('//') + 2)]

            
        cmd, cmdShow = self.buildCmd('convert.py', url)
        cmdNum = 1
        if originUrl != '' and originUrl.find('[') != -1 or originUrl.find(',') != -1:
            self.convert_command = self.replaceCmdArg(cmd, '-i', originUrl)
            cmdNum = 2
        data = ''
        #cmdList = self.cmd2CmdList(cmd)
        #for cmd in cmdList:
        data += self.execCommand(cmd, cmdNum=cmdNum)

        return data.strip()

    def expandData(self, data, resourceType):
        allData = ''

        for line in data.split('\n'):
            r = Record(line)
            url = r.get_url().strip()

            if url != '':
                #self.initArgs(url, resourceType, pass2=True)

                dataTemp = self.doConvert(url, self.form_dict, resourceType, isEnginUrl=False, genHtml=False, pass2=True)

                if dataTemp != '':
                    allData += dataTemp

                    print 'dataTemp:' + dataTemp

        if allData == '':
            allData = data
        elif self.convert_output_data_to_temp:
            self.write2DataFile(allData, 'w')
        return allData

    def genHtml(self, data, divID, rID, resourceType, command='', fileName='', doPass2=True):

        if doPass2 and self.convert_pass2:
            data = self.expandData(data, resourceType)
        
        html = ''
        start = False
        noNumber = False
        if self.convert_split_column_number == 0:
            html = '<div class="ref"><ol>'
            start = True
        else:
            html = '<div align="left" style="float:left;"><ol>'
            start = True
            noNumber = True
        self.count = 0
        count = 0
        itemCount = 0
        records = []
        titles = ''
        debugSplitChar = '\n '
        
        desc = ''
        line_count = 0
        show_url_icon = False
        smartIcon = self.utils.getIconHtml('', title=self.convert_smart_engine, width=8, height=6)
        if smartIcon == '':
            smartIcon = self.utils.getIconHtml('url', width=8, height=6)

        datas = data.split('\n')

        if self.convert_top_item_number > 0 and len(datas) > self.convert_top_item_number:
            datas = datas[0 : self.convert_top_item_number]
        for line in datas:
            try:
                line = line.encode('utf-8')
            except Exception as e:
                continue
            
            show_url_icon = False
            r = Record(line)
            smartLink = ''
            id = r.get_id().strip()
            title = r.get_title().strip().encode('utf-8')
            noHtmlTitle = self.utils.clearHtmlTag(title)
            #title = self.customFormat(title)
                
            if self.convert_smart_engine != '':
                smartLink = self.utils.toQueryUrl(self.convert_smart_engine, noHtmlTitle.lower().replace('"', '').replace("'", ''))
            
            if title.strip() == '':
                continue
            link = r.get_url().strip()
            if link != '' and self.convert_show_url_icon:
                show_url_icon = True

            if link != '' and link.startswith('http') == False:
                link = self.url_prefix + link
            elif link == '' and self.convert_smart_engine != '':
                link = smartLink

            desc = r.get_describe().strip()


            if self.search_keyword_len > 0:
                keywordDesc = ''
                keywordList = noHtmlTitle.split(' ')

                kwCount = 0
                kwStr = ''
                for kw in keywordList:
                    kw = kw.strip()
                    if kw == '':
                        continue
                    kwCount += 1
                    kwStr += kw + ' '
                  
                    if kwCount >= self.search_keyword_len:
                        kwCount = 0
                        keywordDesc += kwStr + '(' + self.utils.toQueryUrl(self.convert_smart_engine, kwStr) + '), '
                        kwStr = ''

                if kwStr != '':
                    kwStr = kwStr.strip()
                    keywordDesc += kwStr + '(' + self.utils.toQueryUrl(self.convert_smart_engine, kwStr) + ') '

                if keywordDesc != '':
                    if keywordDesc.endswith(', '):
                        keywordDesc = keywordDesc[0 : len(keywordDesc) - 2]
                    #print keywordDesc
                    desc += ' website:' +  keywordDesc

            self.count += 1
            count += 1
            titles += title + debugSplitChar
            r = Record('convert-' + str(count) + ' | ' + title + ' | ' + link + ' | ' + desc)
            records.append(r)


            if link != '':
                #title = '<a href="' + link + '" target="_blank">' + title + "</a>"

                title = self.utils.enhancedLink(link, noHtmlTitle, module='convert', aid='convert-' + str(self.count), showText=title)
            else:
                title = self.utils.toSmartLink(noHtmlTitle, br_number=self.convert_cut_max_len, showText=title)

            if show_url_icon:
                title += self.utils.getIconHtml('url', width=8, height=6)

            if desc.find('icon:') != -1:
                icon = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : 'icon'})

                title = ' <a href="javascript:void(0);" onclick="' + "openUrl('" + link + "', '" + link[link.rfind('/') + 1 :] + "', true, false, '" + rID + "', '" + resourceType + "', '', 'convert', '');" + '"><img width="48" height="48" src="' + icon + '"' + ' alt="' + r.get_title().strip() + '"  style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'


            if self.convert_split_column_number > 0 and (self.count == 1 or self.count > self.convert_split_column_number):
                if start:
                    html += '</ol></div>'
                    self.count = 1
                
                line_count += 1
                if line_count == 3:
                    #html += '<br>'
                    line_count = 0

                heightAndWidthStyle = ''

                if self.convert_div_height_ratio > 0:
                    height = self.convert_split_column_number * self.convert_div_height_ratio
                    heightAndWidthStyle = 'height:' + str(height) + 'px;'
                if self.convert_div_width_ratio > 0 and self.convert_cut_max_len < 100:
                    width = self.convert_div_width_ratio * self.convert_cut_max_len
                    heightAndWidthStyle += ' width:' + str(width) + 'px; '

                html += '<div align="left" style="float:left; ' + heightAndWidthStyle + '"><ol>'
                noNumber = True
                start = True


            html += '<li>'
            if noNumber == False:
                html += '<span>' + str(count) + '.</span><p>'


            if self.convert_smart_engine == 'searchin':
                js = "typeKeyword('>" + noHtmlTitle + "','');"
                title += '<a href="javascript:void(0);" onclick="' + js + '">' + smartIcon + '</a>'

            elif link != '' and smartLink != '' and show_url_icon == False:

                title += '<a target="_blank" href="' + smartLink + '">' + smartIcon + '</a>'

            html += title

            ref_divID = divID + '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :] + '-' + str(count)
            appendID = str(count)
            newTitle = self.customFormat(r.get_title().strip())

            if newTitle.find('<') != -1 and newTitle.find('>') != -1:
                newTitle = self.utils.clearHtmlTag(newTitle).replace('"', '').replace("'", '').replace('\n', ' ')
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-convert-" + rID.replace(' ', '-') + '-' + str(appendID), newTitle, link, '-', hidenEnginSection=True)

            descHtml = ''
            if desc != '':
                descHtml = self.utils.genDescHtml(desc, Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, rid=rID)
            
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

            #html += '<br>'
            if noNumber == False:
                html += '</p>'
            html += '</li>'
            if noNumber:
                html += '<div style="height:6px;"></div>'
        if start:
            html += '</ol></div>'
        #html += "</ol></div>"
        #print '\n' + titles + '\n'


        if self.convert_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'convert', self.form_dict['rTitle'], self.convert_output_data_format)
        else:
            if self.convert_output_data_to_temp and self.convert_output_data_to_new_tab == False:

                html = self.genCommandBox(command=command, fileName=fileName, inputSize='116') + '<br>' + html
                if self.convert_command != '':
                    html = self.genCommandBox(command=self.convert_command, inputID='convert_command_txt', buttonID='convert_command_btn', inputSize='116') + html

            return html


    def customFormat(self, text, cut=True):
        #text = text.replace('《','').replace('》', '').replace('"', '').replace("'", '')
        #return text[0 : text.find('/')].strip()

        if self.convert_cut_start != '' and text.find(self.convert_cut_start) != -1:
            text = text[text.find(self.convert_cut_start) + len(self.convert_cut_start) + self.convert_cut_start_offset :].strip()
        if self.convert_cut_end != '':
            text = text[0 : text.find(self.convert_cut_end) + self.convert_cut_end_offset].strip()

        if len(self.convert_remove) > 0:
            for remove in self.convert_remove:
                if text.lower().find(remove.lower()) != -1:
                    #print text
                    text = text.replace(remove, '').replace(remove.lower(), '').strip()
                    #print text
        if len(self.convert_replace.items()) > 0:
            for k, v in self.convert_replace.items():
                if text.lower().find(k.lower()) != -1:
                    text = text.replace(k, v).replace(k.lower(), v).strip()


        if self.convert_append != '':
            text = text + ' ' + self.convert_append 



        if len(text) > self.convert_cut_max_len and cut:
            text = text[0 : self.convert_cut_max_len]

        return text

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != '' 
        #return url != '' and url.startswith('http') or (url.find('[') != -1 and url.find(']') != -1)
        #url = form_dict['url'].encode('utf8')
        #return url != "" and url.startswith('http')
