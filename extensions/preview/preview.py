#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
import requests
from bs4 import BeautifulSoup

class Preview(BaseExtension):

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
        html = '<div class="ref"><br><iframe width="560" height="315" src="https://www.youtube.com/embed/' + url[url.rfind('v=') + 2 :] + '" frameborder="0" allowfullscreen></iframe>'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        div = soup.find('div', id='watch-uploader-info')
        div2 = soup.find('div', id='watch-description-text')
        html += '<br><br><div style="background-color:#F8F8FF; border-radius: 5px 5px 5px 5px; width:auto;">' + div.text.strip() + '<br>' + div2.text.strip()  + '</div></div>'
        return html
        

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url.find('youtube') != -1 and url.find('watch') != -1
