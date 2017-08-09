#!/usr/bin/env python


import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from update.all_subject import default_subject
from record import ContentRecord
from config import Config
import re
import requests
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup

class Content(BaseExtension):

    record_content = {}

    datafile_content = {}
    optional_content = {}

    form_dict = None

   

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.data_dir = 'extensions/content/data/'
        self.data_type = 'content'
        self.contentref = ''


    def loadContent(self, rID, name, content):
	print 'rid :' + rID
	print ' loadContent filename:' + name
        if len(content) != 0 and content.has_key(rID):
            return

        if os.path.exists(name) and os.path.isfile(name):
            f = open(name, 'rU')
            all_lines = f.readlines()
            for line in all_lines:
		line = line.strip()
                record = ContentRecord(line)
                if line.startswith('#') or record.get_parentid() == None:
                    continue
                if record.get_title().strip() == '':
                    continue
                key = record.get_parentid().strip()
                if key != rID:
                    continue
                if content.has_key(key):
                    content[key].append(record)
                else:
                    content[key] = [record]

        #for (k, v) in self.record_content.items():
        #    print k

    def excute(self, form_dict):
        self.form_dict = form_dict
        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        fileName = form_dict['fileName'].encode('utf8')
        contentID = rID

        self.contentref = self.getContentRef(rID, fileName) 
        print 'contentref:' + self.contentref

        if self.contentref != '':
            contentID = self.contentref
            fileName = form_dict['originFileName'].encode('utf8')

        self.loadContent(contentID, fileName, self.optional_content)

        self.loadContent(contentID, self.getExtensionDataFilePath(self.formatFileName(fileName)), self.datafile_content)

        return self.genContentHtml(contentID, divID, form_dict['defaultLinks'])
        '''
        r = requests.get('https://www.google.com.hk/search?q=jquery+load&oq=jqload&aqs=chrome.1.69i57j0l5.9057j0j7&sourceid=chrome&ie=UTF-8')
        soup = BeautifulSoup(r.text) 
        for a in soup.find_all('a'):
            if a['href'].startswith('http') == False:
                a['href'] = 'https://www.google.com.hk' + a['href']
        return r.text
        '''

    def getExtensionDataFilePath(self, name):
        return self.data_dir + name + '-' + self.data_type

    def check(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        fileName = form_dict['fileName'].encode('utf8')
        #return True

        #    print 'xwwwww' + r.line
        #    return True
        p = self.utils.find_file_by_pattern_path(re.compile(rID, re.I), self.getExtensionDataFilePath(self.formatFileName(fileName)))
        print p
        if p != '':
            return True

        if self.getContentRef(rID, fileName) != '':
            return True

        return False

        #self.loadContent(rID, fileName, self.optional_content)
        #self.loadContent(rID, self.getExtensionDataFilePath(self.formatFileName(fileName)), self.datafile_content)
        #print self.record_content
        #print self.optional_content
        #print self.datafile_content
        #return self.datafile_content.has_key(rID) or self.optional_content.has_key(rID)

    def getContentRef(self, rID, fileName):
        record = self.utils.getRecord(rID, path=fileName)
        if record != None and record.line.strip() != '':
            contentref = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'contentref'})
            if contentref != None:

                return contentref.strip()
        return ''


    def write(self, html):
        f = open('temp/test.html', 'w')
        for line in html:
            f.write(line)
        #print 'write ' + html + ' to file'
        f.close

    def genContentHtml(self, key, content_divID, defaultLinks):
        return self.genMetadataHtml(key, content_divID, defaultLinks)

    def genMetadataHtml(self, key, content_divID, defaultLinks):
        html = '<div class="ref"><ol>'
        if self.form_dict['column'] == '3' and int(self.form_dict['extension_count']) > 10:
            html = '<div class="ref"><br><ol>'

        count = 0
        if self.datafile_content.has_key(key):
            self.record_content = self.datafile_content
        elif self.optional_content.has_key(key):
            self.record_content = self.optional_content

        if self.record_content.has_key(key):
            #print key
            for r in self.record_content[key]:
                count += 1
                format_index = ''
                pRecord = None
                pid = r.get_parentid().strip()
                if self.record_content.has_key(pid) and key.find('-') != -1:
                    pRecord = self.record_content[pid] 
		    if content_divID.find(self.data_type) == content_divID.rfind(self.data_type):
                        format_index = str(count)
		    else:
                        format_index = pid[pid.rfind('-') + 1 :] + '.' + str(count)
                elif r.get_id().find('-') != -1:
                    format_index = r.get_id()[r.get_id().rfind('-') + 1 : ].strip()
		while format_index.find('-') != -1:
		    format_index = format_index[format_index.find('-') + 1 :]
                html += '<li><span>' + format_index + '</span>'
                if len(format_index) > 5:
                    html += '</li><br/><li>'
                
                content_divID += '-' + str(count)
                linkID = 'a-' + content_divID[content_divID.find('-') + 1 :]
                title = r.get_title().strip().replace(' ', '%20')
                script = self.utils.genMoreEnginScript(linkID, content_divID, r.get_id().strip(), self.utils.clearHtmlTag(title), r.get_url().strip(), '-', hidenEnginSection=Config.content_hiden_engin_section)
                moreHtml = self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', content_divID, '', False);
                if self.record_content.has_key(r.get_id().strip()) or r.get_url().strip() == '':
                    if r.get_url().strip() != '':
                        html += '<p>' + self.genMetadataLink(r.get_title().strip(), r.get_url().strip())
                    else:
                        html += '<p>' + self.utils.toSmartLink(r.get_title().strip(), 45, module='content', rid=self.form_dict['rID'], library=self.form_dict['originFileName'])
                    #html += self.utils.getDefaultEnginHtml(title, defaultLinks)
                    if moreHtml != "":
                        html += moreHtml
                    html += '</p>'
                elif r.get_url().strip() != '':
                    html += '<p>' + self.genMetadataLink(r.get_title().strip(), r.get_url().strip())  + moreHtml + '</p>'
                html += '</li>'
        else:
            return ''

        html += "</ol></div>"
        return html


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
            title = self.utils.enhancedLink(url, self.utils.formatTitle(title, 45), module='content', rid=self.form_dict['rID'], library=self.form_dict['originFileName'])
        return title
