#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Monitor(BaseExtension):

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
	#src = 'https://pomotodo.com/app/'
	src = 'https://trello.com/'
	column = form_dict['column']
	width = '560'
	height = '315'
	if column == '1':
	    width = '1200'
	    height = '550'
	html = '<div class="ref"><br><iframe width="' + width + '" height="' + height + '" src="' + src + '" frameborder="0" allowfullscreen></iframe>'
	html += '</div>'
        return html
        

    def check(self, form_dict):
	return True
