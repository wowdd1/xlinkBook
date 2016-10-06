#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record
from config import Config

class Save(BaseExtension):

    saved_records = {}

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def loadLibrary(self, username):
        if os.path.exists('db/library/' + self.getLibrary(username)) and len(self.saved_records) == 0:
            f = open('db/library/' + self.getLibrary(username))
            for line in f.readlines():
                r = Record(line)
                self.saved_records[r.get_id().strip()] = r
            f.close()

    def getLibrary(self, username):
        library = username + '-library'
        if Config.default_library != '':
            library = Config.default_library
            if library.endswith('-library') == False:
                library += '-library'
        return library


    def excute(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        user_name = form_dict['user_name'].encode('utf8')
        if self.saved_records.has_key(rID):
            return "already saved"

        record = self.utils.getRecord(rID, path=fileName)
        print record.get_title()
        if record != None and self.saved_records.has_key(record.get_id().strip()) == False:
            f = open('db/library/' + self.getLibrary(user_name), 'a')
            #f.write(record.line.replace('\n', '').strip() + " path:" + fileName[fileName.find('db/') : ] + "\n")
            f.write(record.line.replace('\n', '').strip() + " path:" + record.get_path() + "\n")
            f.close()
            self.saved_records[record.get_id().strip()] = record
            print self.saved_records
            return "saved to " + self.getLibrary(user_name)
        return "save fail"
        
                
    def check(self, form_dict):
        originFileName = form_dict['originFileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        user_name = form_dict['user_name'].encode('utf8')
        print rID
        if user_name != '' and originFileName.endswith('library') == False:
            self.loadLibrary(user_name)
            print self.saved_records
            return self.saved_records.has_key(rID) == False and rID.startswith('loop') == False
        return False
        
    def needCache(self):
        return False
