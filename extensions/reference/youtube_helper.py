#!/usr/bin/env python

import requests
import json
from bs4 import BeautifulSoup

class YoutubeHelper():
    
    def __init__(self):
        self.playlists = []
        self.videos = []

    def getPlaylist(self, html):
        soup = BeautifulSoup(html)
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'].startswith('/playlist?list='):
                key = a.text.strip()
                self.playlists.append([key, 'https://www.youtube.com' + a['href']])

    def getLoadMoreHref(self, html):
        if html.strip() == '':
            return ''
        soup = BeautifulSoup(html)
        button = soup.find('button', class_='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button')
        if button != None:
            return button['data-uix-load-more-href']
        return ''

    def getVideo(self, html):
        soup = BeautifulSoup(html)
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'].startswith('/watch?v='):
                key = a.text.strip()
                if key == '':
                    continue
                url = 'https://www.youtube.com' + a['href']
                self.videos.append([key, url])

    def getVideos(self, url):
        self.videos = []
        print url
        r = requests.get(url)
        self.getVideo(r.text)
        
        load_more_href = self.getLoadMoreHref(r.text)

        while (load_more_href != ''):

            r = requests.get('https://www.youtube.com' + load_more_href)
            jobj = json.loads(r.text)
            load_more_href = self.getLoadMoreHref(jobj['load_more_widget_html'].strip())

            self.getVideo(jobj['content_html']) 

        return self.videos

    def getPlaylists(self, url):
        self.playlists = []
        r = requests.get(url)
        self.getPlaylist(r.text)

        load_more_href = self.getLoadMoreHref(r.text)

        while (load_more_href != ''):

            r = requests.get('https://www.youtube.com' + load_more_href)
            jobj = json.loads(r.text)
            load_more_href = self.getLoadMoreHref(jobj['load_more_widget_html'].strip())

            self.getPlaylist(jobj['content_html'])

        return self.playlists

