#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record

class Milestone(BaseExtension):

    record_milestone = {}
    html = ''

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def loadMilestone(self, filename, rID):
        print 'loadMilestone ' + filename
        #if len(self.record_milestone) != 0 and self.record_milestone.has_key(rID):
        #    return
        name = 'extensions/milestone/data/' + filename + '-milestone'
        record_milestone_back = {}
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

                if record_milestone_back.has_key(key):
                    record_milestone_back[key].append(record)
                else:
                    record_milestone_back[key] = [record]

        if record_milestone_back.has_key(rID) and len(record_milestone_back[rID]) > 0:
            #if len(record_milestone_back[rID]) > 20:
            record_milestone_back[rID] = reversed(record_milestone_back[rID])

            self.record_milestone[rID] = record_milestone_back[rID]
        

        #for (k, v) in self.record_milestone.items():
        #    print k

    def excute(self, form_dict):
      
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')

        self.loadMilestone(self.formatFileName(fileName), rID)
        #print self.record_milestone
        if self.record_milestone.has_key(rID):
            return self.genMilestoneHtml(rID, form_dict['divID'].encode('utf8'))

        return 'not found'


    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadMilestone(self.formatFileName(fileName), rID)
        return self.record_milestone.has_key(rID)
                

    def genMilestoneHtml(self, rID, ref_divID):
        return self.genMetadataHtml(rID, ref_divID)

    def genMetadataHtml(self, key, ref_divID):
        if self.record_milestone.has_key(key):
            self.html = '<div class="ref"><ol>'
            count = 0
            print 'sdsd'
            for r in self.record_milestone[key]:
                count += 1
                ref_divID += '-' + str(count)
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
                appendID = str(count)
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key.replace(' ', '-') + '-' + str(appendID), self.utils.clearHtmlTag(r.get_title().strip()), r.get_url().strip(), '-')

                title = r.get_title().strip()
                id = title[0 : title.find(' ')].strip()
                self.html += '<li><span>' + id + '.</span>'
                if len(id) > 4:
                    self.html += '<br>'

                if script != "" and len(title[title.find(' ') + 1 :].strip()) < 20:
                    self.html += '<p>' + self.utils.toSmartLink(title[title.find(' ') + 1 :].strip())
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                else:
                    self.html += '<p>' + title[title.find(' ') + 1 :].strip()
                self.html += '</p></li>'
            return self.html + "</ol></div>"
        else:
            return ''

