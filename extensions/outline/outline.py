#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils
from config import Config
import subprocess

class Outline(BaseExtension):

    def __init__(self):
	   BaseExtension.__init__(self)
	   self.utils = Utils()

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
        url = url.replace('#space', ' ')
        divID = form_dict['divID']
        rID = form_dict['rID']
        cmd = './outline.py -i "' + url + '"'
        output = subprocess.check_output(cmd, shell=True).strip()
        html = '<div class="ref"><ol>'
        count = 0
        for line in output.split('\n'):
            if line.strip() == '':
                continue
            count += 1
            html += '<li><span>' + str(count) + '.</span>'
            html += '<p>' + self.utils.toSmartLink(line.strip())

            divID += '-' + str(count)
            linkID = 'a-' + divID[divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, divID, "loop-o-" + rID.replace(' ', '-') + '-' + str(appendID) , line, '', '-', hidenEnginSection=Config.bookmark_hiden_engin_section)
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', divID, '', False);


            html += '</p></li>'

        html += '</ol></div>'
        return html


    def check(self, form_dict):
        url = form_dict['url'].encode('utf8').strip()
        print url
        #print url.startswith('http') == False
        print url != '' and url.startswith('http') == False and url.endswith('.pdf')
        return url != '' and url.startswith('http') == False and url.endswith('.pdf')
