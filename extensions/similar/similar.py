#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import PaperRecord
import cPickle as pickle

class Similar(BaseExtension):

    papers_dict = {}
    sim_dict = {}
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

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
        rID = form_dict['rID']
        if rID.startswith('arxiv') == False:
            return ''
        record = self.utils.getRecord(rID.strip())
        pid = self.getPid(record.get_url())

        self.loadPapers()
        self.loadSimDict()
        #print sim_dict
        print 'request:'
        print pid + ' ' + self.papers_dict[pid].get_title()
        if pid in self.sim_dict:
            print 'resutl:'
            for k in self.sim_dict[pid]:
                print k + ' ' + self.papers_dict[k].get_title()
            return self.genHtml(pid)
        return ''

    def genHtml(self, pid):
        html = '<div class="ref"><ol>'
        records = []
        for k in self.sim_dict[pid]:
            records.append(self.papers_dict[k])
        #self.utils.sortRecords(records)
        records = records[1 : ]
        for record in records:
            #html += '<li><span>' + record.get_id().strip() + '</span><br/>'
            html += '<li>'
            html += '<p><a target="_blank" href="' + record.get_url() + '">' + record.get_title() + "</a></p></li>"

        html += "</ol></div>"
        return html



    def check(self, form_dict):
        rID = form_dict['rID']
        return rID.startswith('arxiv')
