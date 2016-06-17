#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Comment(BaseExtension):

    def excute(self, form_dict):
        rID = form_dict['rID'].encode('utf8')

        html = ''
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
        return rID.find('arxiv') != -1
