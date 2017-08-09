#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from config import Config
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record

class Convert(BaseExtension):

    form_dict = None
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.count = 0

    def excute(self, form_dict):
        print 'excute'
        self.form_dict = form_dict
        url = form_dict['url'].encode('utf8')
        if url == '':
            url = self.utils.bestMatchEnginUrl(form_dict['rTitle'].encode('utf8'))
        if Config.convert_url_args != '':
            url += Config.convert_url_args
        print url

        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        html = ''
        step = Config.convert_page_start
        #new_url = url
        new_url = url

        if Config.convert_url_args != '':
            new_url = url + str(step)

        self.count = 0
        if Config.convert_page_step > 0 and Config.convert_url_args != '':
            all_data = ''
            while True:
                data = self.convert2data(new_url)
                if data != '' and data != None:
                    all_data += data + '\n'
                elif data == '':
                    if Config.convert_page_to_end == False:
                        break
                step += Config.convert_page_step
                if step > Config.convert_page_max:
                    break
                new_url = url + str(step)
            if all_data != '':
                return self.genHtml(all_data, divID, rID)
            else:
                return ''
        else:
            html = self.genHtml(self.convert2data(new_url), divID, rID)

        return html

    def convert2data(self, url):

        url_prefix = url[0 : url.find('/', url.find('//') + 2)]

            
        cmd = './convert.py -i "' + url + '" '

        if Config.convert_tag != '':
            cmd += '-t "' + Config.convert_tag + '" '
        if Config.convert_min_num >= 0:
            cmd += '-n ' + str(Config.convert_min_num) + ' '
        if Config.convert_max_num >= 0:
            cmd += '-m ' + str(Config.convert_max_num) + ' '

        if Config.convert_filter != '':
            cmd += '-f "' + Config.convert_filter + '" '
        if Config.convert_contain != '':
            cmd += '-c "' + Config.convert_contain + '" '
        if Config.convert_start > 0:
            cmd += '-s ' + str(Config.convert_start) + ' '
        if Config.delete_from_char != '':
            cmd += '-d "' + Config.delete_from_char + '" '

        print 'cmd ----> ' + cmd + ' <----'
        data = subprocess.check_output(cmd, shell=True)

        return data.strip()


    def genHtml(self, data, divID, rID):
        
        html = ''
        start = False
        if Config.convert_split_column_number == 0:
            html = '<div class="ref"><ol>'
            start = True
        count = 0
        records = []
        titles = ''
        for line in data.split('\n'):
            
            r = Record(line)
            id = r.get_id().strip()
            title = r.get_title().strip()
            if title.strip() == '':
                continue
            link = r.get_url().strip()
            if link != '' and link.startswith('http') == False:
                link = url_prefix + link


            self.count += 1
            count += 1
            titles += title + ', '
            records.append(Record('convert-' + str(count) + ' | ' + title + ' | ' + link + ' | '))
            if link != '':
                title = '<a href="' + link + '" target="_blank">' + title + "</a>"
            else:
                title = self.utils.toSmartLink(title)


            if Config.convert_split_column_number > 0 and (self.count== 1 or self.count > Config.convert_split_column_number):
                if start:
                    html += '</ol></div>'
                    self.count = 1
                
                html += '<div style="float:left;"><ol>'
                start = True


            html += '<li><span>' + str(count) + '.</span>'
            html +=  '<p>' + title

            ref_divID = divID + '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), r.get_title().strip(), link, '-', hidenEnginSection=True)
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            #html += '<br>'
            html += '</p></li>'

        if start:
            html += '</ol></div>'
        #html += "</ol></div>"
        print '\n' + titles + '\n'
        if Config.convert_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'convert', self.form_dict['rTitle'], Config.convert_output_data_format)
        else:
            return html

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != '' and url.startswith('http')
        #url = form_dict['url'].encode('utf8')
        #return url != "" and url.startswith('http')
