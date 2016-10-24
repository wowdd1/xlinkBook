#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import subprocess
from config import Config

class Filefinder(BaseExtension):
    form_dict = None
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()


    def excute(self, form_dict):
        self.form_dict = form_dict
        rTitle = form_dict['rTitle'] 
        if form_dict.has_key('selection') and form_dict['selection'] != '':
            rTitle = form_dict['selection'].strip()
        html = ''
        localFiles = self.genFileList(self.getMatchFiles(rTitle.strip()).split('\n'))
        if localFiles != '':
            html += '<br>' + localFiles

        html += '<div class="ref"><br>' + self.utils.toSmartLink(rTitle, engin="pan.baidu", showText="search my baidu disk", rid=self.form_dict['rID'], library=self.form_dict['originFileName'], module='filefinder') + '</div>'

        return html

    def getMatchFiles(self, title):
        output = ''
        for path in Config.filefinder_dirs:
            if path != '':
                cmd = 'find ' + path + ' -iname "*' + title.replace('"', '').replace('%20', ' ').replace(' ', '*') + '*"'
                print 'cmd ' + cmd 
                output = subprocess.check_output(cmd, shell=True)
            if output.find('No such file') != -1:
                continue
            if output.find('//') != -1:
                output = output.replace('//', '/')
        return output

    def genFileList(self, dataList):
        print 'genFileList ' + ''.join(dataList)
        html = ''
        count = 0
        if len(dataList) > 0:
            html = '<div class="ref"><ol>'
            for line in dataList:
                if line != '':
                    count += 1
                    html += '<li><span>' + str(count) + '.</span>'
                    if line.startswith('db/'):
                        url = 'http://' + Config.ip_adress + '/?db=' + line[line.find('/') + 1 : line.rfind('/') + 1] + '&key=' + line[line.rfind('/') + 1 :] + '&column=' + Config.column_num + '&width=' + Config.default_width
                        html += '<p>' + self.utils.enhancedLink(url, line[line.rfind('/') + 1 :], module='filefinder', rid=self.form_dict['rID'], library=self.form_dict['originFileName'])
                    else:
                        html += '<p>' + self.utils.enhancedLink(line, line[line.rfind('/') + 1 :], module='filefinder', rid=self.form_dict['rID'], library=self.form_dict['originFileName'])

                    html += '</p></li>'
            html += "</ol></div>"
        if count == 0:
            html = ''

        return html

    def check(self, form_dict):
        return True