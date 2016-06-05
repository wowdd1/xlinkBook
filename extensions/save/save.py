#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record

class Save(BaseExtension):

    saved_records = {}

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def loadLibrary(self):
        if os.path.exists('db/library/library') and len(self.saved_records) == 0:
            f = open('db/library/library')
            for line in f.readlines():
                r = Record(line)
                self.saved_records[r.get_id().strip()] = r
            f.close()

    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        if self.saved_records.has_key(rID):
            return "already saved"

        record = self.utils.getRecord(rID, path=fileName)
        print record.get_title()
        if record != None and self.saved_records.has_key(record.get_id().strip()) == False:
            f = open('db/library/library', 'a')
            f.write(record.line)
            f.close()
            self.saved_records[record.get_id().strip()] = record
            print self.saved_records
            return "save sucess"
        return "save fail"
        
                
    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        self.loadLibrary()
        print self.saved_records
        return self.saved_records.has_key(rID) == False
        
    def needCache(self):
        return False
