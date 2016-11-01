#!/usr/bin/env python 

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import subprocess
from config import Config
import datetime

class Filefinder(BaseExtension):
    form_dict = None
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()


    def excute(self, form_dict):
        self.form_dict = form_dict
        rTitle = form_dict['rTitle'] 
        rID = form_dict['rID']
        if form_dict.has_key('selection') and form_dict['selection'] != '':
            rTitle = form_dict['selection'].strip()
        html = ''
        localFiles = self.genFileList(self.getMatchFiles(rTitle.strip()).split('\n'))
        if localFiles != '':
            html += '<br>' + localFiles

        alias = ''
        aliasList = []
        record = self.utils.getRecord(rID.strip(), path=form_dict['originFileName'], log=True)
        if record != None and record.get_id().strip() != '':
            ret = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'alias'})
            if ret != None:
                alias = ret.strip()
                print 'alias:' + alias
                if alias != '':
                    if alias.find(',') != -1:
                        aliasList = alias.split(',')
                        for als in aliasList:
                            result = self.genFileList(self.getMatchFiles(als.strip()).split('\n'))
                            if result != '':
                                html += als + ':<br>' + result
                    else:
                        aliasList = [alias.strip()]
                        result = self.genFileList(self.getMatchFiles(alias.strip()).split('\n'))
                        if result != '':
                            html += alias + ':<br>' + result

        html += '<div class="ref"><br>search my baidu disk ' + self.utils.toSmartLink(rTitle, engin="pan.baidu", showText="1", rid=self.form_dict['rID'], library=self.form_dict['originFileName'], module='filefinder') + '&nbsp;'
        count = 1
        for alias in aliasList:
            count += 1
            html += self.utils.toSmartLink(alias.strip(), engin="pan.baidu", showText=str(count), rid=self.form_dict['rID'], library=self.form_dict['originFileName'], module='filefinder') 
            html += '&nbsp;'

        html += '</div>'

        return html

    def getMatchFiles(self, title):
        output = ''
        for path in Config.filefinder_dirs:
            if path != '':
                cmd = 'find ' + path + ' -iname "*' + title.replace('"', '').replace('%20', ' ').replace(' ', '*') + '*"'
                print 'cmd ' + cmd 
                output += subprocess.check_output(cmd, shell=True)
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
                if line != '' and (line.find(Config.output_data_to_new_tab_path) == -1 or line.find('.') != -1):
                    count += 1
                    html += '<li><span>' + str(count) + '.</span>'
                    if line.startswith('db/') and line.endswith(str(datetime.date.today().year)):
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