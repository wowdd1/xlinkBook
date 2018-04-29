#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from config import Config
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record
from record import Tag


class Convert(BaseExtension):

    form_dict = None
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.count = 0
        self.tag = Tag()

        self.convert_url_args = '' #'?start=' #'?start=0&tag='
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
        self.convert_output_data_to_new_tab = False
        self.convert_output_data_format = ''
        self.convert_cut_start = ''
        self.convert_cut_start_offset = 0
        self.convert_cut_end = ''
        self.convert_cut_end_offset = 0
        self.convert_remove = []
        self.convert_cut_max_len = 1000
        self.convert_script = ''
        self.convert_script_custom_ui = False
        self.convert_smart_engine = ''
        self.url_prefix = ''

    def initArgs(self, url, resourceType):
        self.convert_url_args = Config.convert_url_args #'?start=' #'?start=0&tag='
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
        self.convert_output_data_to_new_tab = Config.convert_output_data_to_new_tab
        self.convert_output_data_format = Config.convert_output_data_format  
        self.convert_cut_start = Config.convert_cut_start
        self.convert_cut_start_offset = Config.convert_cut_start_offset
        self.convert_cut_end = Config.convert_cut_end
        self.convert_cut_end_offset = Config.convert_cut_end_offset
        self.convert_remove = Config.convert_remove
        self.convert_cut_max_len = Config.convert_cut_max_len
        self.convert_script = Config.convert_script
        self.convert_script_custom_ui = Config.convert_script_custom_ui
        self.convert_smart_engine = Config.convert_smart_engine

        for k, v in Config.convert_dict.items():
            if url.find(k) != -1 or (resourceType != '' and k.lower() == resourceType.lower()):
                #print 'k:' + k 
                #print v
                if v.has_key('url_args'):
                    self.convert_url_args = v['url_args']
                if v.has_key('page_step'):
                    self.convert_page_step = v['page_step']
                if v.has_key('page_start'):
                    self.convert_page_start = v['page_start']                
                if v.has_key('page_max'):
                    self.convert_page_max = v['page_max']
                if v.has_key('page_to_end'):
                    self.convert_page_to_end = v['page_to_end']
                if v.has_key('tag'):
                    self.convert_tag = v['tag']   
                if v.has_key('min_num'):
                    self.convert_min_num = v['min_num']
                if v.has_key('max_num'):
                    self.convert_max_num = v['max_num']
                if v.has_key('filter'):
                    self.convert_filter = v['filter']   
                if v.has_key('contain'):
                    self.convert_contain = v['contain']
                if v.has_key('start'):
                    self.convert_start = v['start']
                if v.has_key('split_column_number'):
                    self.convert_split_column_number = v['split_column_number']   
                if v.has_key('output_data_to_new_tab'):
                    self.convert_output_data_to_new_tab = v['output_data_to_new_tab']   
                if v.has_key('output_data_format'):
                    self.convert_output_data_format = v['output_data_format']   
                if v.has_key('cut_start'):
                    self.convert_cut_start = v['cut_start'] 
                if v.has_key('cut_start_offset'):
                    self.convert_cut_start_offset = v['cut_start_offset'] 
                if v.has_key('cut_end'):
                    self.convert_cut_end = v['cut_end'] 
                if v.has_key('cut_end_offset'):
                    self.convert_cut_end_offset = v['cut_end_offset']   
                if v.has_key('remove'):
                    self.convert_remove = v['remove'] 
                if v.has_key('cut_max_len'):
                    self.convert_cut_max_len = v['cut_max_len'] 
                if v.has_key('script'):
                    self.convert_script = v['script'] 
                if v.has_key('script_custom_ui'):
                    self.convert_script_custom_ui = v['script_custom_ui'] 
                if v.has_key('smart_engine'):
                    self.convert_smart_engine = v['smart_engine'] 
 
                if self.convert_smart_engine == '' and self.utils.search_engin_dict.has_key(k):
                    self.convert_smart_engine = k
                break

    def processData(self, data):
        result = ''
        info = ''
        for line in data.split('\n'):
            r = Record(line)
            url = r.get_url().strip()

            if self.convert_contain != '' and line.find(self.convert_contain) == -1:
                continue

            if self.convert_filter != '' and line.find(self.convert_filter) != -1:
                continue


            if url.find('twitter') != -1:
                info += url[url.rfind('/') + 1 :] + ', '

            result += line + '\n'

        print info[0 : len(info) - 2]

        return result
      
    def excute(self, form_dict):
        print 'excute'
        #print form_dict
        self.form_dict = form_dict
        url = form_dict['url'].encode('utf8')

        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        
        resourceType = ''
        if form_dict.has_key('resourceType'):
            resourceType = form_dict['resourceType'].encode('utf8')

        self.initArgs(url, resourceType)

        #print self.convert_remove
        #print 'convert_script:' + self.convert_script
        html = ''
        if self.convert_script != '':
            cmd = './extensions/convert/' + self.convert_script + ' -u "' + url + '" '
            print cmd

            data = subprocess.check_output(cmd, shell=True)

            print 'convert_script_custom_ui:' + str(self.convert_script_custom_ui)
            print 'data:' + data
            if self.convert_script_custom_ui:
                return data.replace('\n', '<br>')
            else:
                return self.genHtml(self.processData(data), divID, rID, resourceType)

        else:
            if url == '':
                url = self.utils.bestMatchEnginUrl(form_dict['rTitle'].encode('utf8'))
            if self.convert_url_args != '':
                url += self.convert_url_args
            print url

            step = self.convert_page_start
            #new_url = url
            new_url = url

            if self.convert_url_args != '':
                new_url = url + str(step)

            self.count = 0
            print self.convert_page_step
            print self.convert_url_args
            if self.convert_page_step > 0 and self.convert_url_args != '':
                all_data = ''
                while True:
                    data = self.convert2data(new_url)
                    if data != '' and data != None:
                        all_data += data + '\n'
                    elif data == '':
                        if self.convert_page_to_end == False:
                            break
                    step += self.convert_page_step
                    if step > self.convert_page_max:
                        break
                    new_url = url + str(step)
                if all_data != '':
                    return self.genHtml(all_data, divID, rID, resourceType)
                else:
                    return ''
            else:
                html = self.genHtml(self.convert2data(new_url), divID, rID, resourceType)

        return html

    def convert2data(self, url):

        self.url_prefix = url[0 : url.find('/', url.find('//') + 2)]

            
        cmd = './convert.py -i "' + url + '" '

        if self.convert_tag != '':
            cmd += '-t "' + self.convert_tag + '" '
        if self.convert_min_num >= 0:
            cmd += '-n ' + str(self.convert_min_num) + ' '
        if self.convert_max_num >= 0:
            cmd += '-m ' + str(self.convert_max_num) + ' '

        if self.convert_filter != '':
            cmd += '-f "' + self.convert_filter + '" '
        if self.convert_contain != '':
            cmd += '-c "' + self.convert_contain + '" '
        if self.convert_start > 0:
            cmd += '-s ' + str(self.convert_start) + ' '
        if Config.delete_from_char != '':
            cmd += '-d "' + Config.delete_from_char + '" '

        print 'cmd ----> ' + cmd + ' <----'
        data = subprocess.check_output(cmd, shell=True)

        return data.strip()


    def genHtml(self, data, divID, rID, resourceType):
        
        html = ''
        start = False
        if self.convert_split_column_number == 0:
            html = '<div class="ref"><ol>'
            start = True
        count = 0
        records = []
        titles = ''
        debugSplitChar = '\n '
        noNumber = False
        desc = ''
        for line in data.split('\n'):
            line = line.encode('utf-8')
            r = Record(line)

            id = r.get_id().strip()
            title = r.get_title().strip().encode('utf-8')
            title = self.customFormat(title)

            if title.strip() == '':
                continue
            link = r.get_url().strip()
            if link != '' and link.startswith('http') == False:
                link = self.url_prefix + link
            elif link == '' and self.convert_smart_engine != '':
                link = self.utils.toQueryUrl(self.convert_smart_engine, title.lower().replace('"', '').replace("'", ''))

            desc = r.get_describe().strip()

            self.count += 1
            count += 1
            titles += title + debugSplitChar
            r = Record('convert-' + str(count) + ' | ' + title + ' | ' + link + ' | ' + desc)
            records.append(r)


            if link != '':
                title = '<a href="' + link + '" target="_blank">' + title + "</a>"
            else:
                title = self.utils.toSmartLink(title)

            if desc.find('icon:') != -1:
                icon = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : 'icon'})

                title = ' <a href="javascript:void(0);" onclick="' + "openUrl('" + link + "', '" + link[link.rfind('/') + 1 :] + "', true, false, '" + rID + "', '" + resourceType + "', '', 'convert', '');" + '"><img width="48" height="48" src="' + icon + '"' + ' alt="' + r.get_title().strip() + '"  style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'


            if self.convert_split_column_number > 0 and (self.count== 1 or self.count > self.convert_split_column_number):
                if start:
                    html += '</ol></div>'
                    self.count = 1
                
                html += '<div style="float:left;"><ol>'
                noNumber = True
                start = True


            html += '<li>'
            if noNumber == False:
                html += '<span>' + str(count) + '.</span><p>'
            html += title

            ref_divID = divID + '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), self.customFormat(r.get_title().strip()), link, '-', hidenEnginSection=True)

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
            return html

    def customFormat(self, text):
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


        if len(text) > self.convert_cut_max_len:
            text = text[0 : self.convert_cut_max_len]

        return text

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != '' and url.startswith('http')
        #url = form_dict['url'].encode('utf8')
        #return url != "" and url.startswith('http')
