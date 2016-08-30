#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
import feedparser


class Rss(BaseExtension):


    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):

        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        url = form_dict['url']

        return self.genHtml(url, form_dict['divID'].encode('utf8'), rID)




    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')

        return fileName.find('rss/') != -1 and rID.startswith('loop') == False



    def genHtml(self, feed_url, ref_divID, rID):
        f = feedparser.parse( feed_url )
        print "Feed Title %s" % f.feed.title
        count = 0
        html = ''
        html += '<div class="ref"><ol>'
        for entry in f.entries:
            print "Title: %s" % entry.title
            print "link: %s" % entry.link

            count += 1
            html += '<li><span>' + str(count) + '.</span>'
            html += '<p><a target="_blank" href="' + entry.link + '"> '+ self.utils.formatTitle(entry.title, 60) + '</a>'

            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), entry.title, entry.link, '-')
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            html += '</p></li>'

        html += '</ol></div>'
        return html
