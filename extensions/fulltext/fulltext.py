#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils

class Fulltext(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()

    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        if rID.find('arxiv') != -1:
            arxiv_id = rID[rID.find('arxiv-') + 6 :].replace('-', '.')
            version = self.utils.get_last_arxiv_version(arxiv_id)
            return 'http://arxiv.org/pdf/' + arxiv_id + version
        return 'http://scholar.google.com.secure.sci-hub.io/scholar?q=' + form_dict['rTitle']

    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        return fileName.find('arxiv') != -1
