#!/usr/bin/env python

from webservice.base_webservice import BaseWebservice

class TwitterWebservice(BaseWebservice):
    """docstring for TwitterWebservice"""
    def __init__(self, arg):
        BaseWebservice.__init__(self)
        self.arg = arg


    def getWebData(self, record, keyword, keywordResourceType):
        return []