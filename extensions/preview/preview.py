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

    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        url = form_dict['url'].encode('utf8')
        screenWidth = form_dict['screenWidth'].encode('utf8')
        screenHeight = form_dict['screenHeight'].encode('utf8')
        print 'screenWidth: ' + screenWidth
        print 'screenHeight: ' + screenHeight
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

        html = '<div class="ref"><br><iframe width="' + width + '" height="' + height + '" src="' + src + '" frameborder="0" allowfullscreen></iframe>'
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
        

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != None and url != '' and url.startswith('http') and url.find(Config.ip_adress) == -1
