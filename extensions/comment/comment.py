#!/usr/bin/env python

from extensions.bas_extension import BaseExtension
from utils import Utils

class Comment(BaseExtension):


    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')

        html = ''
        if rID.find('arxiv') != -1:
            arxiv_id = rID[rID.find('arxiv-') + 6 :].replace('-', '.')          
            utils = Utils()
            for e in utils.get_arxiv_entries(arxiv_id):
                j = utils.encode_feedparser_dict(e)
                if j.has_key('arxiv_comment'):
                    print j['arxiv_comment']
                    html += '<br/>' + j['arxiv_comment'] + '<br/>'
                    html += j['updated'][0 : j['published'].find('T')] + ' '
                    html += j['id'][j['id'].rfind('v') :] + '<br/>'

        rID = rID[rID.find('-') + 1 : ].replace('-', '.')
        url = "https://scirate.com/arxiv/" + rID 
        html += '<br/><iframe src="' + url + '" style="border: 0; width: 100%; height: 400px"></iframe><br/>'
        html += '<br/><a href="' + url + '" target="_blank" >scirate</a><br/>'

        url = 'http://www.shortscience.org/paper?bibtexKey=journals/corr/' + rID
        html += '<br/><iframe src="' + url + '" style="border: 0; width: 100%; height: 400px"></iframe><br/>'
        html += '<br/><a href="' + url + '" target="_blank" >shortscience</a><br/>'
   
        url = 'http://gitxiv.com/search/?q=' + form_dict['rTitle']
        html += '<br/><a href="' + url + '" target="_blank" >gitxiv</a><br/>'
        return html

    def check(self, form_dict):
        rID = form_dict['rID'].encode('utf8')
        fileName = form_dict['fileName'].encode('utf8')
        return fileName.find('arxiv') != -1
