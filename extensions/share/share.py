#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Share(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)

    def excute(self, form_dict):
        url= form_dict['url'].encode('utf-8')
        title = form_dict['rTitle']
        html = '<ul>'
        html += '<li><a href="javascript:void(0);" onclick=share("facebook","' + url + '","' + title + '");>facebook</a></li>'
        html += '<li><a href="javascript:void(0);" onclick=share("twitter","' + url + '","' + title + '");>twitter</a></li>'
        html += '<li><a href="javascript:void(0);" onclick=share("linkedin","' + url + '","' + title + '");>linkedin</a></li>'
        html += '<li><a href="mailto:?subject=' + title + ' (' + url + ')&amp;body=' + title+ ' (' + url + ')" target="_self">mail</a></li>'
        html += '</ul>'
        print html
        return html

    def check(self, form_dict):
        url= form_dict['url']
        return url != None and url != ''
