#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from update.all_subject import default_subject
from record import ReferenceRecord
from record import CategoryRecord, Category
from semanticscholar import Semanticscholar
from config import Config
from bs4 import BeautifulSoup
import requests

class Reference(BaseExtension):

    record_reference = {}
    html = ''

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.semanticscholar = Semanticscholar()
        self.category_obj = Category()

    def loadReference(self, filename, rID):
        if len(self.record_reference) != 0 and self.record_reference.has_key(rID):
            return
        name = 'extensions/reference/data/' + filename + '-reference'
        if os.path.exists(name):
            f = open(name, 'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                record = ReferenceRecord(line)
                key = record.get_id().strip()
                if key != rID:
                    continue

                if self.record_reference.has_key(key):
                    self.record_reference[key].append(record)
                else:
                    self.record_reference[key] = [record]

        #for (k, v) in self.record_reference.items():
        #    print k

    def excute(self, form_dict):
      
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadReference(self.formatFileName(fileName), rID)
        #print self.record_reference
        if self.record_reference.has_key(rID):
            #print result
            return self.genReferenceHtml(rID, form_dict['divID'].encode('utf8'))
        elif rID.find('arxiv') >= 0:
            return self.genReferenceHtml2(self.semanticscholar.getReferences(form_dict['rTitle']), form_dict['divID'].encode('utf8'),
                                          form_dict['defaultLinks'], form_dict['rID'])
        else:
            return self.getAllLinks(form_dict['url'])          


    def getAllLinks(self, url):
        if url == '':
            return ''
        else:
            user_agent = {'User-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(r.text)
            count = 0
            link_dict = {}
            html = ''
            html += '<div class="ref"><ol>'
            count = 0
            for a in soup.find_all('a'):
                if a.attrs.has_key('href') == False or link_dict.has_key(a['href']):
                    continue
                link = a['href']
                title = a.text.strip().encode('utf-8')
                if title == '':
                    title = link.replace('http://', '').replace('www.', '')
                link_dict[link] = link
                link = self.utils.fixUrl(url, link)
                count += 1
                print str(count) + ' ' + title + ' ' + link
                html += '<li><span>' + str(count) + '.</span>'
                html += '<p>' + '<a target="_blank" href="' + link + '">' + title + '</a></li>'
            html += '</ol></div>'
        if count == 0:
            html = ''
        return html

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadReference(self.formatFileName(fileName), rID)
        category = ''
        print 'check filename ' + fileName
        if rID.startswith('loop') == False:
            record = self.utils.getRecord(rID, path=fileName)
            if record != None:
                category = CategoryRecord(record.line).get_category()
        if self.record_reference.has_key(rID) or rID.startswith('arxiv') or rID.startswith('loop') or (category == self.category_obj.paper) or form_dict['url'] != '':
            return True
        return False
                

    def genReferenceHtml2(self, alist, divid, defaultLinks, rID):
        return self.genMetadataHtml2(alist, divid, defaultLinks, rID)
    
    def genMetadataHtml2(self, alist, ref_divID, defaultLinks, rID):
            self.html = '<div class="ref"><ol>'
            count = 0
            for r in alist:
                count += 1
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                if rID.startswith('loop'):
                    appendID = rID[rID.rfind('-') + 1 :].replace('R', '.') + '.' + str(count) 
                    self.html += '<li><span>' + appendID + '.</span>'
                    if len(appendID) >= 5:
                        self.html += '<br/>'
                    appendID = appendID.replace('.','R')
                else:
                    self.html += '<li><span>' + str(count) + '.</span>'
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID + '-' + str(appendID), r[0], r[1], '-')
                if r[1] != '':
                    self.html += '<p>' + '<a target="_blank" href="' + r[1] + '">' + r[0] + '</a>'
                else:
                    self.html += '<p>' + r[0]
                #self.html += self.utils.getDefaultEnginHtml(r[0], defaultLinks)
                if script != "":
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                self.html += '</p></li>'
            return self.html + "</div>"


    def genReferenceHtml(self, rID, ref_divID):
        return self.genMetadataHtml(rID, ref_divID)

    def genMetadataHtml(self, key, ref_divID):
        if self.record_reference.has_key(key):
            self.html = '<div class="ref"><ol>'
            count = 0
            for r in self.record_reference[key]:
                count += 1
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key + '-' + str(appendID), self.utils.clearHtmlTag(r.get_title().strip()), r.get_url().strip(), '-')

                self.html += '<li><span>' + str(count) + '.</span>'
                self.html += '<p>' + self.genMetadataLink(r.get_title().strip(), r.get_url().strip())
                if script != "":
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                self.html += '</p></li>'
            return self.html + "</div>"
        else:
            return ''


    def genMetadataLink(self, title, url):
        if url.find('[') != -1:
            ft = url.replace('[', '').replace(']', '').strip()
            r = self.utils.getRecord(ft, '','', False, False)
            key = r.get_path()[r.get_path().find(default_subject) + len(default_subject) + 1 :]
            url = 'http://' + Config.ip_adress + '?db=' + default_subject + '/&key=' + key + '&filter=' + ft  + '&desc=true'

        return self.genMetadataLinkEx(title, url)


    def genMetadataLinkEx(self, title, url):
        if title.find('<a>') != -1:
            title = title.replace('<a>', '<a target="_blank" href="' + url + '">')
        else:
            title = '<a target="_blank" href="' + url + '">' + title + '</a>'
        return title
