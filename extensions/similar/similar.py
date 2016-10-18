#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import PaperRecord, Category
import cPickle as pickle
import requests
from bs4 import BeautifulSoup
from config import Config
import subprocess

class Similar(BaseExtension):

    papers_dict = {}
    sim_dict = {}
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.category_obj = Category()
        self.img_style = "-webkit-border-radius: 8px; -moz-border-radius: 8px; border-radius: 8px; background: #f8f8f8; border-top:1px solid #ccc; border-right:1px solid #666; border-bottom:2px solid #999; border-left:1px solid #ccc; padding: 0px;"

    def loadPapers(self):
        if len(self.papers_dict) > 0:
            return
        files = os.listdir('db/eecs/papers/arxiv/')
        for item in files:
            f = open('db/eecs/papers/arxiv/' + item, 'rU')
            lines = f.readlines()
            f.close()
            for line in lines: 
                record = PaperRecord(line)
                self.papers_dict[self.getPid(record.get_url())] = record


    def loadSimDict(self):
        if len(self.sim_dict) == 0:
            self.sim_dict = pickle.load(open("analysis/tfidf/sim_dict.p", "rb"))

    def getPid(self, url):
        return url[url.rfind('/') + 1 : ].replace('.pdf', '').strip()

    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf-8')
        fileName = form_dict['fileName']
        record = self.utils.getRecord(rID, path=fileName)
        if rID.startswith('arxiv'):
            pid = self.getPid(record.get_url())

            self.loadPapers()
            self.loadSimDict()
            #print sim_dict
            if self.papers_dict.has_key(pid) == False:
                return ''
            print 'request:'
            print pid + ' ' + self.papers_dict[pid].get_title()
            if pid in self.sim_dict:
                print 'resutl:'
                for k in self.sim_dict[pid]:
                    if self.papers_dict.has_key(k):
                        print k + ' ' + self.papers_dict[k].get_title()
                return self.genHtml(pid)
        return ''

    def genHtml(self, pid):
        html = '<div class="ref"><ol width="100%">'
        records = []
        for k in self.sim_dict[pid]:
            records.append(self.papers_dict[k])
        #self.utils.sortRecords(records)
        #records = records[1 : ]
        count = 0
        for record in records:
            #html += '<li><span>' + record.get_id().strip() + '</span><br/>'
            #version = record.get_version()
            #if version == None or version.strip() == '':
            version = '1'
            
            found = False
            thumbs = ''
            retry = 0
            while found == False and retry < 3:
                thumbs = "http://www.arxiv-sanity.com/static/thumbs/" + self.getPid(record.get_url()) + "v" + version + ".pdf.jpg"
                output = ''
                try:
                    output = subprocess.check_output("curl --max-time 1 --head " + thumbs, shell=True)
                except Exception as e:
                    print e
                print output
                if output.find('200 OK') != -1:
                    found = True
                else:
                    retry += 1
                    version = str(int(version) + 1)
            if found == False:
                thumbs = ''
            
                    
            authors = record.get_author().split(',')
            categorys = record.get_category().split(' ')
            date_cat =  record.get_published() + "&nbsp;&nbsp; " + self.genListHtml(categorys, "category:")
            count += 1
            html += '<li><span>' + str(count) + '</span>'
            html += '<p><a target="_blank" href="' + record.get_url() + '">' + record.get_title() + '</a><p>'
            html += '<div>' + self.genListHtml(authors, "author:") + '</div><div>' + date_cat + '</div>'
            if thumbs != '':
                html += '<image width="570px" src="' + thumbs + '" style="' + self.img_style + '"></image>'
            else:
                html += '<br\>'
            html += '<div>' + record.get_summary() + "</div></li><br/>"
        html += "</ol></div>"
        return html

    def genListHtml(self, alist, category):
        html = ''
        for item in alist:
            if item.strip() == "":
                continue
            html += '<a target="_blank" href="http://' + Config.ip_adress + '?db=eecs/papers/arxiv/&filter=' + category + item.strip().replace(' ', '%20') + '">'+ item.strip() + '</a>'
            if item != alist[len(alist) - 1]:
                html += ', '
            else:  
                html += ' '
 
        return html
       

    def check(self, form_dict):
        rID = form_dict['rID'].encode('utf-8')
        fileName = form_dict['fileName']
        return rID.startswith('arxiv')
