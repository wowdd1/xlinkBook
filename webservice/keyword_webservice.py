#!/usr/bin/env python

from webservice.base_webservice import BaseWebservice
import requests
import json

class KeywordWebservice(BaseWebservice):
    """docstring for KeywordWebService"""
    def __init__(self, arg):
      BaseWebservice.__init__(self)
      self.arg = arg

    def getWebData(self, record, keyword, keywordResourceType):
     
        keywords = []
        r = requests.get('http://tools.seochat.com/components/com_seotools/tools/suggest-tool/googleall.php?q=' + keyword)
        jobj = json.loads(r.text)
        for item in jobj:
           if type(item) != type([]) and item.find('fieldset>') == -1:
                keywords.append(item.strip())
        return keywords