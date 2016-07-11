#!/usr/bin/env python

from extensions.bas_extension import BaseExtension

class Share(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)

    def excute(self, form_dict):
        url= form_dict['url'].encode('utf-8')
        title = form_dict['rTitle']
        html = '<div class="ref">'
        html += '<a href="javascript:void(0);" onclick=share("facebook","' + url + '","' + title + '");><img src="http://mycroftproject.com/updateos.php/id0/facebookvideomirror.ico"></a>&nbsp;'
        html += '<a href="javascript:void(0);" onclick=share("twitter","' + url + '","' + title + '");><img src="http://mycroftproject.com/updateos.php/id0/twitter-music.png"></a>&nbsp;'
        html += '<a href="javascript:void(0);" onclick=share("google+","' + url + '","' + title + '");><img src="http://mycroftproject.com/updateos.php/id0/plusgoogle.ico"></a>&nbsp;'
        html += '<a href="javascript:void(0);" onclick=share("linkedin","' + url + '","' + title + '");><img src="http://mycroftproject.com/updateos.php/id0/linkedin_googfr.ico"></a>&nbsp;'
        html += '<a href="mailto:?subject=' + title + ' (' + url + ')&amp;body=' + title+ ' (' + url + ')" target="_self"><img src="http://mycroftproject.com/updateos.php/id0/gmail.ico"></a>&nbsp;'
        html += '<a href="javascript:void(0);" onclick=share("weibo","' + url + '","' + title + '");><img src="http://mycroftproject.com/updateos.php/id0/sina_weibo_free.png"></a>&nbsp;'
        html += '</div>'
        print html
        return html

    def check(self, form_dict):
        url= form_dict['url']
        return url != None and url != ''
