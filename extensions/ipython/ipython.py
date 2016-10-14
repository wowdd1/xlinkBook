#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Ipython(BaseExtension):

    def excute(self, form_dict):
        url = form_dict['url'].encode('utf8')
	src = 'http://www.tutorialspoint.com/ipython_terminal_online.php'
        #src = 'http://localhost:8888/tree#notebooks'
	column = form_dict['column']
	width = '660'
	height = '415'
	if column == '1':
	    width = '1300'
	    height = '700'
	elif column == '3':
	    width = '560'
	html = '<div class="ref"><br><iframe width="' + width + '" height="' + height + '" src="' + src + '" frameborder="0" allowfullscreen></iframe>'
	html += '</div>'
        return html
        

    def check(self, form_dict):
	return True
