#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record

class Delete(BaseExtension):


    def __init__(self):
        BaseExtension.__init__(self)


    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        library = 'db/library/library'
        if os.path.exists(library):
            f = open(library, 'rU')
            all_lines = []
            for line in f.readlines():
                if rID != line[0 : line.find('|')].strip():
                    all_lines.append(line)
            f.close()
            if len(all_lines) > 0:
                f = open(library, 'w')
                for line in all_lines:
                    f.write(line)
                f.close()
                return 'http://localhost:5000/?db=library/&key=library'
        return 'error'

    def check(self, form_dict):
        return form_dict.has_key('delete') and form_dict['delete']

    def needCache(self):
        return False
