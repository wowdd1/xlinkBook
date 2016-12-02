#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from update.all_subject import default_subject
from record import CategoryRecord, Category
from semanticscholar import Semanticscholar


class Citation(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.semanticscholar = Semanticscholar()
        self.category_obj = Category()
        self.utils = Utils()


    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        url = form_dict['url'].encode('utf8')
        return fileName.find('papers') != -1 and url != ''

    def excute(self, form_dict):

        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        return self.genReferenceHtml2(self.semanticscholar.getCitations(form_dict['rTitle']), form_dict['divID'].encode('utf8'),
                                          form_dict['defaultLinks'], form_dict['rID'])

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
                script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID + '-' + str(appendID), r[0], '-')
                if r[1] != '':
                    self.html += '<p>' + '<a target="_blank" href="' + r[1] + '">' + r[0] + '</a>'
                else:
                    self.html += '<p>' + r[0]
                #self.html += self.utils.getDefaultEnginHtml(r[0], defaultLinks)
                if script != "":
                    self.html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
                self.html += '</p></li>'
            return self.html + "</div>"
