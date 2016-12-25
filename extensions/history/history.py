#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import json
from config import Config
import subprocess
from record import Record
from record import Tag

class History(BaseExtension):

    raw_data = ''
    jobj_list = []
    tag = Tag()

    """docstring for History"""
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.loadHistory()
        self.form_dict = None

    def loadHistory(self):
        self.updateHistory()
        if os.path.exists('extensions/history/data/chrome_history.json'):
            f = open('extensions/history/data/chrome_history.json', 'rU')
            self.raw_data = f.read()
            self.jobj_list = json.loads(self.raw_data)
            f.close()

    def updateHistory(self):
        if os.path.exists(Config.history_file_path):
            subprocess.check_output("mv " + Config.history_file_path + " extensions/history/data/chrome_history.json", shell=True)
            self.loadHistory()

    def getAlias(self, rID, file, nocache):
        alias = ''
        use_cache = nocache == False
        record = self.utils.getRecord(rID.strip(), path=file, log=True, use_cache=use_cache)
        if record != None and record.get_id().strip() != '':
            ret = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'alias'})
            if ret != None:
                alias = ret.strip()
                print 'alias:' + alias

        if alias.find(',') != -1:
            return alias.split(',')
        elif alias != '':
            return [alias]
        else:
            return []

    def excute(self, form_dict):
        self.form_dict = form_dict
        if form_dict.has_key('nocache'):
            nocache = form_dict['nocache'].encode('utf8')
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        rID = form_dict['rID'].encode('utf8')
        divID = form_dict['divID'].encode('utf8')
        alias = self.getAlias(rID.strip(), form_dict['originFileName'], nocache)

        self.updateHistory()

        html = ''
        if form_dict['column'] != '1' and form_dict.has_key('extension_count') and int(form_dict['extension_count']) > 12:
            html += '<br>'
        html += '<div class="ref"><ol>'
        count = 0
        item_dict = {}
        for jobj in self.jobj_list:
            if self.match_item(jobj, [rTitle]) or self.match_item(jobj, alias):
                if item_dict.has_key(jobj['title'].strip()):
                    continue
                item_dict[jobj['title'].strip()] = ''
                count += 1
                html += self.gen_item(rID, divID, count, jobj, True, form_dict['originFileName'])

        html += "</ol></div>"

        if count == 0:
            html = ''
        return html

    def gen_item(self, rID, ref_divID, count, jobj, moreOption, orginFilename, keywords=[]):
        html = ''
        
        html += '<li><span>' + str(count) + '.</span>'

        url = ''
        if jobj.has_key('url'):
            url = jobj['url']

        if url != '':
            html += '<p>' + self.utils.enhancedLink(url, self.utils.formatTitle(jobj['title'], Config.smart_link_br_len, keywords), module='history', library=orginFilename, rid=rID) + self.utils.getIconHtml(url)
        else:
            html += '<p>' + jobj['title'] + ' > '
        #if self.existChild(str(jobj['id'])):
        #    html += ' > '

        if moreOption:
            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-h-" + rID.replace(' ', '-') + '-' + str(appendID) + '-' + str(jobj['id']), jobj['title'], url, '-', hidenEnginSection=Config.history_hiden_engin_section)

            descHtml = ''
            #if url != '':
            #    descHtml = self.utils.genDescHtml('url:' + url, Config.course_name_len, self.tag.tag_list)
            #print 'descHtml:' + descHtml
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

        html += '</p></li>'

        return html

    def match_item(self, jobj, rTitleList):
        if len(rTitleList) == 0:
            return False
        for rTitle in rTitleList:
            if rTitle.strip() == '':
                continue
            if self.containIgoncase(jobj['title'].strip(), rTitle.strip()):
                #print jobj['title'].strip() + ' ' + rTitle.strip()
                return True
        return False

    def containIgoncase(self, leftData, rightData):
        return leftData.lower().find(rightData.lower()) != -1

    def check(self, form_dict):
        self.updateHistory()
        rTitle = form_dict['rTitle'].encode('utf8').replace('%20', ' ')
        return os.path.exists('extensions/history/data/chrome_history.json') and self.containIgoncase(self.raw_data, rTitle)

