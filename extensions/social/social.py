#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from config import Config
from utils import Utils
from record import Record, Tag
from bs4 import BeautifulSoup
import requests
import os

class Social(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.tag = Tag()
        self.form_dict = None

    def excute(self, form_dict):
        self.form_dict = form_dict
        rID = form_dict['rID'].strip()
        rTitle = form_dict['rTitle'].strip()
        originFileName = form_dict['originFileName'].strip()
        url = form_dict['url'].strip()

        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        links = soup.find_all("a")
        socialDict = {}
        linkKey = self.getLinkKey(url)
        desc = ''

        for link in links:
   
            if link.has_attr(linkKey):
                #print link

                key = self.socialKey(link[linkKey])
                if key != '':
                    linkUrl = link[linkKey]
                    if socialDict.has_key(key) and socialDict[key] != linkUrl:
                        desc += self.genDesc(key, linkUrl) + ' '
                    else:
                        socialDict[key] = linkUrl
        print socialDict

        html = ''
        
        if len(socialDict) > 0:
            for k, v in socialDict.items():

                desc += self.genDesc(k, v) + ' '

            print ''

            print desc.strip().replace(':', '(').replace(' ', ')+').strip() + ')'

            print ''
            splitChar = '<br>'

            if self.form_dict.has_key('client') and self.form_dict['client'] == 'plugin':
                splitChar = ' '

            descHtml = self.utils.genDescHtml(desc, Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, splitChar=splitChar)
     
            html = '<br>' + descHtml

            script = self.utils.getBatchOpenScript(socialDict.keys(), socialDict.values(), 'social', onePage=False)

            html += '<a target="_blank" href="javascript:void(0);" onclick="' + script + '">#all</a>'

            html += '<br>'

        return html


    def genDesc(self, k, v):
        v = self.preUrl(v)
        if v.endswith('/'):
            v = v[0 : len(v) - 1]
        socialUrl = self.preUrl(self.tag.tag_list_account[k])

        #print v + ' ' + socialUrl
        print v
        print k + v.replace(socialUrl, '')
        return k +v.replace(socialUrl, '')      

    def getLinkKey(self, url):
        #if url.find('google') != -1:
        #    return 'data-href'

        return 'href'

    def socialKey(self, url):
        result = ''
        preurl = self.preUrl(url)
        if preurl.find('/') != -1:
            preurl = preurl[0 : preurl.find('/')]
        for key in self.tag.tag_list_account.keys():

            if preurl.find(key.replace(':', '')) != -1:
                result = key
            else:

                url1 = self.preUrl(url)
                url2 = self.preUrl(self.tag.tag_list_account[key])

                if url1 != '' and url2 != '' and url1.find(url2) != -1:
                    print url1 + ' ()()() ' + url2
                    result = key


        return result

    def preUrl(self, url):
        if url.find('%s') != -1:
            url = url[0 : url.find('%')]
        url = url.replace('http:', '')
        url = url.replace('https:', '')
        url = url.replace('//', '')
        url = url.replace('www.', '')

        return url

    def check(self, form_dict):
        url = form_dict['url'].strip()
        return url != '' and url.find(Config.ip_adress) == -1
