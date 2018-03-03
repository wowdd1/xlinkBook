#!/usr/bin/env python

from config import Config
import requests

class BaseExtension:
    name = ''
    basePath = 'extensions/'
    def __init__(self):
        self.name = ''


    def requests(self, url):
        return requests.get(url, proxies=Config.proxies3, verify=False)

    def excute(form_dict):
        return    

    def check(self, form_dict):
        return True

    def formatFileName(self, fileName):
        while (fileName.find('/') != -1) :
            fileName = fileName[fileName.find('/') + 1 :].strip()
        return fileName

    def needCache(self):
        return True
