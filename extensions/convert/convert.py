#!/usr/bin/env python

import subprocess
from config import Config
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record

class Convert(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        url  = form_dict['url'].encode('utf8')
        url_prefix = url[0 : url.find('/', url.find('//') + 2)]
        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')

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

        print 'cmd ----> ' + cmd + ' <----'
        data = subprocess.check_output(cmd, shell=True)

        
        count = 0
        html = '<div class="ref"><ol><br>'
        for line in data.split('\n'):
            if line.strip() == '':
                continue
            r = Record(line)
            id = r.get_id().strip()
            title = r.get_title().strip()
            link = r.get_url().strip()
            if link != '' and link.startswith('http') == False:
                link = url_prefix + link

            if link != '':
                title = '<a href="' + link + '" target="_blank">' + title + "</a>"
            else:
                title = self.utils.toSmartLink(title)

            count += 1
            html += '<li><span>' + str(count) + '.</span>'
            html += '<p>' + title

            ref_divID = divID + '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), r.get_title().strip(), link, '-')
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            html += '</p></li>'

        html += "</ol></div>"
        return html

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != "" and url.startswith('http')
