#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
import requests
from bs4 import BeautifulSoup
from utils import Utils
import subprocess
from config import Config
import os

class Preview(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.preview_url_args = '' #'?start=' #'?start=0&tag='
        self.preview_next_page = ''
        self.preview_page_step = 1
        self.preview_page_start = 1
        self.preview_page_max = 10
        self.preview_frame_width = 471
        self.preview_frame_height = 700
        self.preview_frame_check = True


    def initArgs(self, url, resourceType):
        if url.startswith('http') == False and url.find('[') != -1:
            url = url[url.find('(') + 1 : url.find(')')]
        self.preview_url_args = Config.preview_url_args #'?start=' #'?start=0&tag='
        self.preview_page_step = Config.preview_page_step
        self.preview_page_start = Config.preview_page_start
        self.preview_page_max = Config.preview_page_max
        self.preview_frame_width = Config.preview_frame_width
        self.preview_frame_height = Config.preview_frame_height
        self.preview_frame_check = Config.preview_frame_check

        for k, v in Config.preview_dict.items():
            if url.lower().find(k.lower()) != -1 or (resourceType != '' and k.lower() == resourceType.lower()):
                print 'matched:' + k 
                print v
                if v.has_key('url_args'):
                    self.preview_url_args = v['url_args']
                if v.has_key('next_page'):
                    self.preview_next_page = v['next_page']
                if v.has_key('page_step'):
                    self.preview_page_step = v['page_step']
                if v.has_key('page_start'):
                    self.preview_page_start = v['page_start']                
                if v.has_key('page_max'):
                    self.preview_page_max = v['page_max']
                if v.has_key('frame_width'):
                    self.preview_frame_width = v['frame_width']
                if v.has_key('frame_height'):
                    self.preview_frame_height = v['frame_height']
                if v.has_key('frame_check'):
                    self.preview_frame_check = v['frame_check']
                #if self.preview_smart_engine == '' and self.utils.search_engin_dict.has_key(k):
                #    self.preview_smart_engine = k
                break

    def previewPages(self, texts, urls):

        htmlList, notSuportLink = self.utils.genAllInOnePage(texts, urls, frameWidth=self.preview_frame_width, frameHeight=self.preview_frame_height, frameCheck=self.preview_frame_check, changeBG=False)
        if len(htmlList) > 0:
            print htmlList[0]
            return htmlList[0]
        return ''

    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        url = form_dict['url'].encode('utf8')
        screenWidth = form_dict['screenWidth'].encode('utf8')
        screenHeight = form_dict['screenHeight'].encode('utf8')
        print 'screenWidth: ' + screenWidth
        print 'screenHeight: ' + screenHeight
        self.initArgs(url, '')
        texts = []
        urls = []
        if self.preview_url_args != '' or self.preview_next_page != '':
            if self.preview_url_args != '':
    
                for page in range(self.preview_page_start, self.preview_page_max + 1, self.preview_page_step):
                    texts.append(str(page))
                    urls.append(url + self.preview_url_args + str(page))

            return self.previewPages(texts, urls)


        if url.find('[') != -1 and url.find(']') != -1:
            keys = []
            value = ''

            if url.startswith('['):
                keys = url[1:url.find(']')].split('*')
                value = url[url.find('(') + 1 : url.find(')')]
            else:
                part1 = url[0 : url.find('[')]
                part2 = url[url.find(']') + 1 : ]
                keys = url[url.find('[') + 1 : url.find(']')].split('*')
                value = part1 + '%s' + part2

            for k in keys:
                texts.append(k.replace('%20', ' '))
                if value.startswith('http'):
                    urls.append(value.replace('%s', k))
                else:
                    urls.append(self.utils.toQueryUrl(self.utils.getEnginUrl(value), k))

            return self.previewPages(texts, urls)



        if url == '':
            url = self.utils.toSmartLink(form_dict['rTitle'].encode('utf8'))
	src = ''
	width = str(int(screenWidth) / 3 + 50)
	height = str(int(screenHeight) / 3 + 50)
	column = form_dict['column']
        if url.startswith('file') or url.startswith('/User'):
            subprocess.check_output("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome " + url, shell=True)
            return 'ok'
    
        if column == '1':
            width = str(int(screenWidth) - 70)
            height = str(int(screenHeight) - 150)
        elif column == '2':
            width = str(int(screenWidth) / 2 - 20)
            height = str(int(screenHeight) / 2 - 50)


	if url.find('youtube') != -1 and url.find('watch') != -1:
	    src = "https://www.youtube.com/embed/" + url[url.rfind('v=') + 2 :]
	    if column == '1':
	        width = str(int(screenWidth) / 3 + 200)
	        height = str(int(screenHeight) / 2)
        elif url.find('163') != -1:
            src = url.replace('open', 'v')
        elif rID.find('arxiv') != -1:
            arxiv_id = rID[rID.find('arxiv-') + 6 :].replace('-', '.')
            version = self.utils.get_last_arxiv_version(arxiv_id)
            src = 'http://arxiv.org/pdf/' + arxiv_id + version
	else:
	    src = url
	    if self.utils.suportFrame(url, 5) == False:
		return url

        html = '<div class="ref"><br><iframe width="' + width + '" height="' + height + '" src="' + self.getUrl(src) + '" frameborder="0" allowfullscreen></iframe>'
	if url.find('youtube') != -1 and url.find('watch') != -1:
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            div = soup.find('div', id='watch-uploader-info')
            div2 = soup.find('div', id='watch-description-text')
	    div_watch = soup.find('div', class_='watch-view-count')
	    div_user = soup.find('div', class_='yt-user-info')

	    text = div_user.text.strip()
            html += '<br><br><div style="background-color:#F8F8FF; border-radius: 5px 5px 5px 5px; width:auto;">'
	    html += '<a target="_blank" href="' + 'https://www.youtube.com' + div_user.a['href'] + '">' + text+ '</a>'
	    count = 0
	    html +=  ' ' + div_watch.text.strip() + '<br>' +\
		     div.text.strip() + '<br>' + div2.text.strip() + '<br><br>'
	    for type in ['videos', 'playlists']:

                ref_divID = form_dict['divID'].encode('utf8')
	        rID = form_dict['rID']
                ref_divID += '-' + type
                linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
	        appendID = count
		count += 1
	        link = 'https://www.youtube.com' + div_user.a['href'] + '/' + type
	        script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), text, link, '-')
						
	        if script != "":
		    html += '<div>'
	        html += '<a target="_blank" href="' + link + '">' + text + '</a>' + " 's " + type
	        if script != "":
	            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False);
		    html += '</div>'
	    html += '</div>'

        return html + '</div>'
        

    def getUrl(self, url):
        '''
        if 'weixin' in url:
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            p = soup.find('p', class_='tit')

            url = p.a['href']

        print 'getUrl:' + url
        '''
        return url

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != None and url != '' and url.startswith('http') and url.find(Config.ip_adress) == -1 or url.find('[') != -1
