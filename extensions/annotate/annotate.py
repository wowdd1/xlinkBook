#!/usr/bin/env python

import sys, os
from record import Record
from extensions.bas_extension import BaseExtension

class Annotate(BaseExtension):

    annotates = {}

    def __init__(self):
        BaseExtension.__init__(self)

    def loadAnnotates(self, fileName, rID):
        if len(self.annotates) != 0 and self.annotates.has_key(rID):
            return
        name = 'extensions/annotate/data/' + fileName + '-annotate'
        if os.path.exists(name):
            f = open(name, 'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                record = Record(line)
                key = record.get_id().strip()
                if key != rID:
                    continue

                if self.annotates.has_key(key):
                    self.annotates[key].append(record)
                else:
                    self.annotates[key] = [record]
                

    def excute(self, form):
        rID = form['rID'].encode('utf8')
        return self.genHtml(rID)

    def genHtml(self, rID):
        html = '<div class="ref">'
        for record in self.annotates[rID]:
            #html += '<iframe src="' + record.get_url().strip() + '" style="border: 0; width: 100%; height: 500px" ></iframe><br/>'
            html += '<p><a href="' + record.get_url().strip() + '" target="_blank">'+ record.get_title().strip() + '</a></p>'
        return html + '</div>'
    

    def check(self, form):
        fileName = form['fileName'].encode('utf8')
        if fileName.find('/') != -1:
            fileName = fileName[fileName.rfind('/') + 1 : ].strip()
        rID = form['rID'].encode('utf8')
        self.loadAnnotates(fileName, rID)
        return self.annotates.has_key(rID)

