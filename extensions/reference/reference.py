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
from extensions.reference.youtube_helper import YoutubeHelper
from record import Record

class Reference(BaseExtension):

    record_reference = {}
    html = ''
    form_dict = None

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.semanticscholar = Semanticscholar()
        self.category_obj = Category()
        self.helper = YoutubeHelper()

    def loadReference(self, filename, rID):
        print 'loadReference ' + filename + ' rID:' + rID
        if len(self.record_reference) != 0 and self.record_reference.has_key(rID):
            return
        name = 'extensions/reference/data/' + filename + '-reference'
        if os.path.exists(name):
            print 'loadReference ' + name
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

        print len(self.record_reference)

        #for (k, v) in self.record_reference.items():
        #    print k

    def excute(self, form_dict):
        self.form_dict = form_dict
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        if self.isYoutubeRssUrl(form_dict['url']):
            return self.youtubeRssHtml(form_dict['url'], rID, form_dict['rID'])

        self.loadReference(self.formatFileName(fileName), rID)
        #print self.record_reference
        if self.record_reference.has_key(rID):
            #print result
            return self.genReferenceHtml(rID, form_dict['divID'].encode('utf8'))
        elif fileName.find('papers') != -1:
            return self.genReferenceHtml2(self.semanticscholar.getReferences(form_dict['rTitle']), form_dict['divID'].encode('utf8'),
                                          form_dict['defaultLinks'], form_dict['rID'])
        else:
            return self.getAllLinks(form_dict['url'], form_dict['divID'].encode('utf8'), form_dict['rID'])          

    def passItem(self, title, url):
        contain = Config.reference_contain
        ft = Config.reference_filter
        if Config.reference_igon_case:
            title = title.lower()
            contain = contain.lower()
            ft = ft.lower()
        if contain != '' and title.find(contain) == -1:
            return True
        if ft != '' and title.find(ft) != -1:
            return True
        print 'found ' + title
        return False

    def getAllLinks(self, url, ref_divID, rID):
        print 'getAllLinks ' + url
        if url == '' or url.startswith('http') == False:
            return ''
        else:
            user_agent = {'User-agent': 'Mozilla/5.0'}
	    url = url.replace('http://', 'https://')
	    print '---- ' + url + ' ---'

            r = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(r.text)
            count = 0
            link_dict = {}
            html = ''
            html += '<div class="ref"><ol>'
            count = 0
            records = []
            for a in soup.find_all('a'):
                if a.attrs.has_key('href') == False or link_dict.has_key(a['href']):
                    continue
                if url.find('youtube') != -1 and url.endswith('videos') == False:
                    if url.find('watch') != -1 and a.text.find('Duration') == -1 and a['href'].startswith('/watch') == False:
                        continue
                    if a['href'].startswith('/watch') == False and a['href'].startswith('/playlist') == False:
                        continue
		    if a.text.strip().find('Play all') != -1:
			continue
		if url.endswith('videos'):
		    if a['href'].startswith('/watch') and a.text.strip() != '':
		        link = 'https://www.youtube.com' + a['href']
		    else:
			continue
		elif a['href'].startswith('/playlist'):
		    link = 'http://www.youtube.com' + a['href']
		else:
                    link = a['href']
                print a['href']
                if self.passItem(a.text.strip(), link):
                    continue
                title = a.text.strip().encode('utf-8')
                if title == '':
                    title = link.replace('http://', '').replace('www.', '')
                link_dict[link] = link
                link = self.utils.fixUrl(url, link)
                text = title
                if url.find('youtube') != -1 and link.find('watch') != -1:
                    link = 'https://www.youtube.com' + link[link.rfind('/watch') :]
                    if url.find('playlist') == -1:
                        if a.text.find('Duration') != -1:
                            text = self.formatYoutubeLink(a, True).replace(' ', '%20') 
                            title = self.formatYoutubeLink(a, False)
                        else:
                            text = self.utils.removeDoubleSpace(a.text.strip()).replace(' ', '%20')
                        if title.startswith('/watch'):
                            continue
		    elif url.endswith('playlist') == False:
                        if count == 0:
                            return self.getAllLinks(link, ref_divID, rID)
                count += 1
                print str(count) + ' ' + title + ' ' + link
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), text, link, '-', hidenEnginSection=Config.reference_hiden_engin_section) 
		#if a.img != None and a.img['src'].endswith('gif') == False:
		#    html += '<img width="48" height="48" src="' + a.img['src'] + '">'
                html += '<li><span>' + str(count) + '.</span>'
		if title.find('- Duration') != -1:
		    html += '<p>' + self.utils.enhancedLink(link, self.utils.formatTitle(title[0 : title.find('- Duration')], Config.smart_link_br_len), module='reference') + title[title.find('- Duration') :]
                    records.append(self.toRecord('reference-' + str(count), title[0 : title.find('- Duration')], link))
	        else:
                    html += '<p>' + self.utils.enhancedLink(link, self.utils.formatTitle(title, Config.smart_link_br_len), module='reference')
                    records.append(self.toRecord('reference-' + str(count), title, link))

                if script != "":
                    html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                html += '</p></li>'
            html += '</ol></div>'
        if count == 0:
            html = ''
        
        if Config.reference_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'reference', self.form_dict['rTitle'], Config.reference_output_data_format)
        else:
            return html

    def toRecord(self, rid, title, url):
        return Record(rid + ' | ' + title.replace('\n', '') + ' | ' + url + ' | ')

    def isYoutubeRssUrl(self, url):
        return (url.find('user') != -1 or url.find('channel') != -1) and (url.find('playlists') != -1 or url.find('videos') != -1) and url.find('watch') == -1 and url.find('youtube') != -1

    def youtubeRssHtml(self, url, rid, divid):
        if url.find('playlist') != -1:
            return self.genRssHtml(self.helper.getPlaylists(url), rid, divid)
        elif url.find('video') != -1:
            videos = self.helper.getVideos(url)
            return self.genRssHtml(videos, rid, divid)
        return ''

    def genRssHtml(self, data, key, ref_divID):
        html = '<div class="ref"><ol>'

        count = 0
        for item in data:
            if self.passItem(item[0], item[1]):
                continue
            count += 1
            html += '<li><span>' + str(count) + '.</span>'
            html += '<p>' + self.utils.enhancedLink(item[1], self.utils.formatTitle(item[0], Config.smart_link_br_len), module='reference')

            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key.replace(' ', '-') + '-' + str(appendID), item[0], item[1], '-', hidenEnginSection=Config.reference_hiden_engin_section)
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            html += '</p></li>'


        html += "</ol></div>"
        return html
                                                        


    def formatYoutubeLink(self, a, title_only):
        sp = BeautifulSoup(a.prettify())
        title = sp.find('span', class_='title').text.strip()
        if title_only:
            return self.utils.removeDoubleSpace(title)
        title += ' ' + sp.find('span', class_='accessible-description').text.strip() + ' '
        title += sp.find('span', class_='g-hovercard').text.strip() + ', '
        views = sp.find('span', class_='stat view-count').text.strip().strip()
        views = views[0 : views.find(' ')]
	font_size = len(views.replace(',', ''))
	if font_size - 2 > 0:
	    font_size -= 2
        title += '<font size="' + str(font_size) + '" color="rgb(212, 51, 51)">' + views + '</font> views'
        return self.utils.removeDoubleSpace(title)

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        url = form_dict['url'].encode('utf8')
        if url == '':
            return False
        self.loadReference(self.formatFileName(fileName), rID)
        if self.record_reference.has_key(rID) or fileName.find('papers') != -1 or form_dict['url'] != '' and form_dict['url'].startswith('http'):
            return True
        return False
                

    def genReferenceHtml2(self, alist, divid, defaultLinks, rID):
        return self.genMetadataHtml2(alist, divid, defaultLinks, rID)
    
    def genMetadataHtml2(self, alist, ref_divID, defaultLinks, rID):
            self.html = '<div class="ref"><ol>'
            count = 0
            for r in alist:
                if self.passItem(r[0], r[1]):
                    continue
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
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), r[0], r[1], '-', hidenEnginSection=Config.reference_hiden_engin_section)
                if r[1] != '':
                    self.html += '<p>' + self.utils.enhancedLink(r[1], self.utils.formatTitle(r[0], Config.smart_link_br_len), module='reference', rid=rID, library=self.form_dict['originFileName'])
                else:
                    self.html += '<p>' + self.utils.toSmartLink(r[0], Config.smart_link_br_len, module='reference', rid=rID, library=self.form_dict['originFileName'])
                #self.html += self.utils.getDefaultEnginHtml(r[0], defaultLinks)
                if script != "":
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                #title = a.text.strip()
                self.html += '</p></li>'
            return self.html + "</ol></div>"


    def genReferenceHtml(self, rID, ref_divID):
        return self.genMetadataHtml(rID, ref_divID)

    def genMetadataHtml(self, key, ref_divID):
        if self.record_reference.has_key(key):
            self.html = '<div class="ref"><br><ol>'
            if self.form_dict['column'] == '1':
                self.html = '<div class="ref"><ol>'
            count = 0
            for r in self.record_reference[key]:
                count += 1
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key.replace(' ', '-') + '-' + str(appendID), self.utils.clearHtmlTag(r.get_title().strip()), r.get_url().strip(), '-', hidenEnginSection=Config.reference_hiden_engin_section)

                self.html += '<li><span>' + str(count) + '.</span>'
                self.html += '<p>' + self.genMetadataLink(r.get_title().strip(), r.get_url().strip(), rID=key)
                if script != "":
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                self.html += '</p></li>'
            return self.html + "</ol></div>"
        else:
            return ''


    def genMetadataLink(self, title, url, rID=''):
        if url.find('[') != -1:
            ft = url.replace('[', '').replace(']', '').strip()
            r = self.utils.getRecord(ft, '','', False, False)
            key = r.get_path()[r.get_path().find(default_subject) + len(default_subject) + 1 :]
            url = 'http://' + Config.ip_adress + '?db=' + default_subject + '/&key=' + key + '&filter=' + ft  + '&desc=true'

        return self.genMetadataLinkEx(title, url, rID=rID)


    def genMetadataLinkEx(self, title, url, rID=''):
        if title.find('<a>') != -1:
            title = title.replace('<a>', '<a target="_blank" href="' + url + '">')
        else:
            title = self.utils.enhancedLink(url, self.utils.formatTitle(title, Config.smart_link_br_len), module='reference', rid=rID, library=self.form_dict['originFileName'])
        return title
