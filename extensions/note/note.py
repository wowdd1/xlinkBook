#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Note(BaseExtension):

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
	src = 'https://app.yinxiang.com/Home.action'
	column = form_dict['column']
	width = '660'
	height = '550'
	if column == '1':
	    width = '1300'
	    height = '600'
	elif column == '3':
	    width = '560'
	html = '<div class="ref"><br><iframe width="' + width + '" height="' + height + '" src="' + src + '" frameborder="0" allowfullscreen></iframe>'
	html += '</div>'
        return html
        

    def check(self, form_dict):
	return form_dict['rID'].startswith('loop') == False
