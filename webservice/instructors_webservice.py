#!/usr/bin/env python

from webservice.base_webservice import BaseWebservice

class InstructorsWebservice(BaseWebservice):
    """docstring for InstructorsWebservice"""
    def __init__(self, arg):
      BaseWebservice.__init__(self)
      self.arg = arg


    def getWebData(self, record, keyword, keywordResourceType):
        #return record.get_title() + ' ' + keyword + ' ' + keywordResourceType

        return []
