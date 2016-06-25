#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Share(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)

    def excute(self, form_dict):
        url= form_dict['url'].encode('utf-8')
        title = form_dict['rTitle']
        html = '<div class="ref"><ol>'
        html += '<li><p><a href="javascript:void(0);" onclick=share("facebook","' + url + '","' + title + '");>facebook</a></p></li>'
        html += '<li><p><a href="javascript:void(0);" onclick=share("twitter","' + url + '","' + title + '");>twitter</a></p></li>'
        html += '<li><p><a href="javascript:void(0);" onclick=share("linkedin","' + url + '","' + title + '");>linkedin</a></p></li>'
        html += '<li><p><a href="mailto:?subject=' + title + ' (' + url + ')&amp;body=' + title+ ' (' + url + ')" target="_self">mail</a></p></li>'
        html += '</ol></div>'
        print html
        return html

    def check(self, form_dict):
        url= form_dict['url']
        return url != None and url != ''
