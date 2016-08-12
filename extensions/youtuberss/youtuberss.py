#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from extensions.youtuberss.youtube_helper import YoutubeHelper 
from utils import Utils

class YoutubeRss(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.helper = YoutubeHelper()
        self.utils = Utils()

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
        rid = form_dict['rID'].encode('utf8')
        divid = form_dict['divID'].encode('utf8')
        if url.find('playlist') != -1:
            return self.genHtml(self.helper.getPlaylists(url), rid, divid)
        elif url.find('video') != -1:
            videos = self.helper.getVideos(url)
            return self.genHtml(videos, rid, divid)
        return ''


    def genHtml(self, data, key, ref_divID):
        html = '<div class="ref"><ol>'

        count = 0
        for item in data:
            count += 1
            html += '<li><span>' + str(count) + '.</span>'
            html += '<p><a target="_blank" href="' + item[1] + '"> '+ item[0] + '</a>'

            ref_divID += '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + key.replace(' ', '-') + '-' + str(appendID), item[0], item[1], '-')
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);

            html += '</p></li>'


        html += "</ol></div>"
        return html


    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url.find('youtube') != -1 and url.find('watch') == -1
