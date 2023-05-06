#!/usr/bin/env python

import os
import json
import sys
import datetime  
from record import Record
from record import LibraryRecord
from config import Config
import urllib
import re


class ExtensionManager:
    
    extensions = {}
    extensions_check_cache = {}
 
    def loadExtensions(self):
        if len(self.extensions) > 0:
            return
        base_path = os.getcwd() + '/extensions'
        #print '--->' + base_path
        dirList = os.listdir(base_path)
        #print dirList
        for f in dirList:
            #print f
            if os.path.isdir(base_path + '/'+ f):
                for f2 in os.listdir(base_path + '/'+ f):
                    if f2 == 'manifest':
                        self.extensions[f] = base_path + '/'+ f + '/' + f2
                        break

    def loadExtensionEx(self, module, className):
        
        return self.newExtension(module, className)

    def loadExtension(self, name):
        if len(self.extensions) == 0:
            self.loadExtensions()
        print 'load ' + name + ' module'
        for k, manifest in self.extensions.items():
            jobj = json.loads(open(manifest, 'rU').read())
            if jobj['name']  == name:
                return self.newExtension('extensions.' + name + '.' + jobj['module'], jobj['class'])

    def newExtension(self, module, cls):
       print 'newExtension:' + module + ' ' + cls
       __import__(module)
       m = sys.modules[module]
      # print m
       for str in dir(m):
           if str == cls:
               att = getattr(m, str)
               return att()

       return None

    def findRecordInLib(self, utils, rID, fileName):
	while True:
            r = utils.getRecord(rID, path=fileName, use_cache=False)
	    if r.get_id().strip() != '':
		return r
	    else:
		if rID.find('-') != -1:
		    rID = rID[0 : rID.rfind('-')]
		else:
		    return None


    def doWork(self, form_dict, utils):
        form = form_dict.copy()
        self.loadExtensions()
        check = form['check']
        rID = form['rID'].encode('utf-8')
        fileName = form['fileName'].encode('utf-8')
        #print form
        if fileName.endswith('library') or fileName.find('exclusive') != -1:
            r = self.findRecordInLib(utils, rID, fileName)
            if r != None and r.get_id().strip() != '':
                lr = LibraryRecord(r.line)
                if lr.get_path() != None and lr.get_path().strip() != '':
                    print lr.get_path()
                    form['originFileName'] = os.getcwd() + '/' + lr.get_path().strip()

                if form.has_key('resourceType') == False and r.line.find('category:') != -1:
                    resourceType = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : 'category'})
                    if resourceType != None:
                        form['resourceType'] = resourceType


        if check == 'true':
            if form['name'] == "*":
                if fileName.find('db/library/') != -1:
                    form['delete'] = True
                    
                if self.extensions_check_cache.has_key(rID) and (form.has_key('nocache') and form['nocache'] == "false"):
                    print 'return cache for ' + rID
                    return self.checkCache(self.extensions_check_cache[rID].split(' '), form)
                else:
                    self.extensions_check_cache[rID] = self.checkAll(form)
                    return self.extensions_check_cache[rID]
            else:
                extension = self.loadExtension(form['name'])
                if extension != None:
                    if extension.check(form):
                        return form['name']
                    else:
                        if form['url'] != '':
                            return 'reference'
                        return 'false'
                else:
                    print 'error'
                    return ''
        else:
            name = form['name']
            if form.has_key('navigate'):
                name = 'track'
                if form['navigate'].strip() == '':
                    form['name'] = 'star'
                else: 
                    form['name'] = form['navigate'].strip()
            
            extension = self.loadExtension(name)

            starttime = 0
            endtime = 0
            starttime = datetime.datetime.now().microsecond
            result = extension.excute(form) #'cs-stanford2016', form['rID'], form['rTitle'], form['divID'])
            endtime = datetime.datetime.now().microsecond
            print name + " excute cost --> " + str((endtime - starttime) / 1000.0) + "ms"
            return result
    def checkCache(self, names, form):
        result = ''
        for name in names:
            extension = self.loadExtension(name)
            if extension != None:
                if extension.needCache():
                    result += name + ' '
                elif extension.check(form):
                    result += name + ' '
        return result

    def checkAll(self, form):
        result = ''
        for k, v in self.extensions.items():
            starttime = 0
            endtime = 0
            starttime = datetime.datetime.now().microsecond
            if self.loadExtension(k).check(form):
                result += k + " "
            endtime = datetime.datetime.now().microsecond
            print k + " check cost --> " + str((endtime - starttime) / 1000.0) + "ms"
        print result
        return result.strip()

    def genIconLinkHtml(self, linkUrl, iconUrl, radius=0, width=12, height=10, batchOpen=False, title='', highLightText=''):
        clickJS = ''
        if linkUrl.find("*") != -1:

            if batchOpen:
                for url in linkUrl.split("*"):
                    clickJS += "window.open('" + url + "');"
            else:
                clickJS += "tabsPreview(this, '" + title + "', '" + linkUrl + "', '" + highLightText + "');"
        else:
            clickJS = "window.open('" + linkUrl + "');"
        html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(iconUrl, radius, width, height) + '</a>'
        return html


    def genJsIconLinkHtml(self, clickJS, iconUrl, radius=0, width=12, height=10):
        html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(iconUrl, radius, width, height) + '</a>'
        return html

    def genIconHtml(self, src, radius, width, height):
        if src != '':
            if radius:
                return ' <img src="' + src + '" width="' + str(width) + '" height="' + str(height) + '" style="border-radius:10px 10px 10px 10px; opacity:0.7;">'
            else:
                return ' <img src="' + src + '" width="' + str(width) + '" height="' + str(height) + '">'
        return ''

    def genJsIconLinkHtml(self, clickJS, iconUrl, radius=0, width=12, height=10):
        html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(iconUrl, radius, width, height) + '</a>'
        return html

    def clearHtmlTag(self, htmlstr):
        if htmlstr.find('<') == -1:
            return htmlstr

        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
        re_br=re.compile('<br\s*?/?>')
        re_h=re.compile('</?\w+[^>]*>')
        re_comment=re.compile('<!--[^>]*-->')
        s=re_cdata.sub('',htmlstr)
        s=re_script.sub('',s)
        s=re_style.sub('',s)
        s=re_br.sub('\n',s)
        s=re_h.sub('',s)
        s=re_comment.sub('',s)
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=self.replaceCharEntity(s)
        return s.strip()

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"','34':'"',}

        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(htmlstr)
        while sz:
            entity=sz.group()
            key=sz.group('name')
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        return htmlstr

    #for domain process 
    def getExtensionHtml(self, website, title, link, group=False, parent=''):
        html = ''
        if group:
            if website == "github" or website == "keyword" or website == 'website':
                js = "getExtensionHtml('" + website + "', '" + title + "', '" + link + "');"
                html =  '<a href="javascript:void(0);" onclick="' + js + '">' + self.genIconHtml(Config.website_icons['extension'], 0, 12, 10) + '</a>'
                return html

        if website == "github" or link.find("github.com") != -1:
            repo = link[link.find("com/") + 4 :]
            user = ''
            if repo.endswith("/"):
                repo = repo[0 : len(repo) -1]
            if repo.find("/") != -1:
                user = repo[0 : repo.find("/")]
            else:
                user = repo

            #if repo.find("/") != -1:
            #    html += '<img src="https://flat.badgen.net/github/stars/' + repo + '" style="max-width: 100%;"/>'
            js = "getEngineHtml('d:project', '" + repo.replace("/", " ") + "');"
            #js = "typeKeyword('?>" + parent + "/" + website + ":/:combine" + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
            html += self.genIconLinkHtml("https://metrics.lecoq.io/insights/" + user + "*" + \
                                         "https://octoprofile.vercel.app/user?id=" + user + "*" + \
                                         "https://www.githubtrends.io/wrapped/" + user + "*" + \
                                         "https://coderstats.net/github/#" + user + "*" + \
                                         "https://ossinsight.io/analyze/" + repo, \
                                         Config.website_icons['analyze'], title=repo, highLightText="github:")
            html += self.genIconLinkHtml("https://useful-forks.github.io/?repo=" + repo + "*" + \
                                         "https://techgaun.github.io/active-forks/#" + repo + "*" +\
                                         "http://gitpop2.herokuapp.com/" + repo + "*" +\
                                         "https://github.com/" + repo + "/network/dependents", \
                                         Config.website_icons['fork'], title=repo, highLightText="github:")
            html += self.genIconLinkHtml("https://github.com/" + repo +  "/commits" + "*" + \
                                         "https://releaseeye.info/" + repo, \
                                         Config.website_icons['release'], title=repo, highLightText="github:")
            html += self.genIconLinkHtml("https://github1s.com/" + repo + "*" + \
                                         "https://replit.com/github/" + repo + "*" + \
                                         "https://mango-dune-07a8b7110.1.azurestaticapps.net/?repo=" + repo + "*" + \
                                         "https://github.dev/" + repo + "*" + \
                                         "https://vscode.dev/github/" + repo + "*" + \
                                         "https://codesandbox.io/s/github/" + repo + "*" + \
                                         "https://gitpod.io/#https://github.com/" + repo + "*" + \
                                         "https://glitch.com/edit/#!/import/github/" + repo + "*" + \
                                         "https://sourcegraph.com/github.com/" + repo, \
                                         Config.website_icons['ide'], title=repo, highLightText="github:")
            html += self.genIconLinkHtml("https://metaphor.systems/search?q=" + urllib.quote(link).replace("/", "%2F") + "*" + \
                                         "https://github.com/" + repo + "/network/dependents" + "*" + \
                                         "https://gitplanet.com/" + repo + "*" + \
                                         "https://similarrepos.com/" + repo + "*" + \
                                         "https://github.com/" + user + "?tab=repositories&sort=stargazers" + "*" + \
                                         "https://github.com/" + user + "?tab=stars" + "*" + \
                                         "https://github.com/orgs/" + user + "/repositories?sort=stargazers" + "*" + \
                                         "https://www.yasiv.com/github/#/costars?q=" + repo, \
                                         Config.website_icons['similar'], title=repo, highLightText="github:")
            #html += self.genIconLinkHtml("https://gitter.im/" + repo, \
            #                             Config.website_icons['talk'])
        elif website == "reddit" or link.find("reddit.com") != -1:
            subreddit = link[link.find("r/") + 2 :]
            if subreddit.endswith("/"):
                subreddit = subreddit[0 : len(subreddit) -1]
            js = "getEngineHtml('d:social', '" + subreddit + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
            html += self.genIconLinkHtml("https://www.troddit.com/r/" + subreddit + "*" + \
                                         "https://megacomments.com/r/" + subreddit + "*" + \
                                         "https://www.popular.pics/reddit/subreddits/posts?r=" + subreddit + "*" + \
                                         "https://axorsium.vercel.app/r/" + subreddit + "*" + \
                                         "https://3dforreddit.com/r/" + subreddit + "*" + \
                                         "https://anvaka.github.io/redsim/#!?q=" + subreddit, \
                                         Config.website_icons['alternative'])
            html += self.genIconLinkHtml("https://anvaka.github.io/sayit/?query=" + subreddit + "*" + \
                                         "https://anvaka.github.io/map-of-reddit/?q=" + subreddit + "*" + \
                                         "https://anvaka.github.io/redsim/#!?q=" + subreddit, \
                                         Config.website_icons['similar'])
        elif website == "y-channel" or link.find("youtube.com/channel") != -1:
            channel = link[link.find("channel/") + 8 :]
            if channel.find("/") != -1:
                channel = channel[0 : channel.find("/")]
            js = "getEngineHtml('d:video', '" + title + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
            html += self.genIconLinkHtml("https://piped.kavin.rocks/channel/" + channel, \
                                         Config.website_icons['alternative'])
            html += self.genIconLinkHtml("https://playboard.co/en/channel/" + channel, \
                                         Config.website_icons['analyze'])
            html += self.genIconLinkHtml("https://playboard.co/en/channel/" + channel, \
                                         Config.website_icons['similar'])
        elif website == "telegram" or link.find("t.me") != -1:
            channel = link[link.find("s/") + 2 :]
            html += self.genIconLinkHtml("https://web.telegram.org/k/#@" + channel + "*" + \
                                         "tg://resolve?domain=" + channel  + "*" + \
                                         "https://app.shokichan.com/c/tg/" + channel + "*" + \
                                         "https://meow.tg/private/" + channel,
                                         Config.website_icons['alternative'])
        elif website == "twitter" or link.find("twitter.com") != -1:
            user = link[link.find("com/") + 4 :]
            html += self.genIconLinkHtml("https://www.sotwe.com/" + user + "*" + \
                                         "https://mobile.twitter.com/" + user,\
                                         Config.website_icons['alternative'])
            html += self.genIconLinkHtml("https://en.whotwi.com/" + user, \
                                         Config.website_icons['analyze'])
        elif website == 'keyword' or website == 'website':
            js = "getEngineHtml('d:star', '" + title + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
            js = "getEngineHtml('d:list', '" + title + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
        elif website == "":
            js = "getEngineHtml('d:star', '" + title + "');"
            html += self.genJsIconLinkHtml(js, \
                                         Config.website_icons['search'])
        if title != '':
            title = self.clearHtmlTag(title)
            if title.find("/") != -1:
                title = title[title.rfind("/") + 1 :]
            js = "typeKeyword('??" + website + ":" + title + "');"
            html += self.genJsIconLinkHtml(js, Config.website_icons["similar"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + '</font>'

            html += self.genIconLinkHtml("https://keywords.groundedai.company/?q=" + title.replace("-", " ") + "*" + \
                                         "https://www.connectedpapers.com/search?q=" + title.replace("-", " ") + "*" + \
                                         "https://www.music-map.com/map-search.php?f=" + title.replace("-", " "),\
                                         Config.website_icons['graph'])
        return html

