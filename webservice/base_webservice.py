#!/usr/bin/env python

import sys
sys.path.append("..")
from utils import Utils
from record import Record

class BaseWebservice:

    webservice_dict = {'twitter' : 'twitter_webservice',\
                        'instructors' : 'instructors_webservice',\
                        'keyword' : 'keyword_webservice'}

    def __init__(self):
        self.name = 'base webservice' 
        self.utils = Utils()

    def getWebData(self, record, keyword, keywordResourceType):
        return []

    def tag2webservice(self, resourceType):
        if self.webservice_dict.has_key(resourceType):
            return self.webservice_dict[resourceType]
        else:
            return ''

    def callWebservice(self, resourceType, record, keyword, keywordResourceType):
        print 'callWebservice resourceType:' + resourceType 
        webservice = self.tag2webservice(resourceType)
        if webservice != '':
            className = resourceType[0 : 1].upper() + resourceType[1 :] + 'Webservice'
            print 'webservice:' + webservice + ' className:' + className
            result = self.utils.reflection_call('webservice.' + webservice, className, 'getWebData', record.line, {'record' : record, 'keyword' : keyword, 'keywordResourceType' : keywordResourceType})
            print result
            return result
        else:
            return ''
