#!/usr/bin/env python
# -*- coding: utf-8-*-  

import os
from flask import Flask
from flask import request
import subprocess
import json
from utils import Utils
from config import Config
import requests
import datetime
from flask import (Flask, flash, request, redirect,
    render_template, url_for, session)
from rauth.service import OAuth2Service
from record import Tag, Record
from knowledgegraph import KnowledgeGraph
import twitter
 
 
tag = Tag()
kg = KnowledgeGraph()
# Use your own values in your real application 
github = OAuth2Service(
    name='github',
    base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_id= '38f88bfb83a0908e0103',
    client_secret= '7f0c4c5d52972e1d767d0145c6e02ce54342ade3',
)
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
utils = Utils()
app = Flask(__name__)
app.secret_key = SECRET_KEY

args_history = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    print  request.args.get('column', '')
    key = request.args.get('key', '')
    db = request.args.get('db', '')
    print key
    if key == '':
        key = '?'
    if db.find('github') != -1:
	if key == 'c':
	    key += '#-github2016'
        key = key.replace('  ', '++')
    key = key.replace(' ', '+')

    if key.find('+') != -1 and key.find('++') == -1:
        key = '+' + key

    key = key.strip()
    if db == '':
        db = Config.default_subject + '/'   
    elif db == '?':
        return listDB()
 
    if key == '?' and request.args.get('filter', '') == '':
        return listAllFile(db)
    else:
        args_history['column'] = request.args.get('column', Config.column_num)

        #filter="keyword[and]keyword[or]keyword[not]keyword"
        args_history['filter'] = request.args.get('filter','')
        args_history['style'] = request.args.get('style', str(Config.css_style_type))
        args_history['desc'] = request.args.get('desc', 'true')
        args_history['width'] = request.args.get('width', '')
        args_history['row'] = request.args.get('row', '')
        args_history['top'] = request.args.get('top', '')
        args_history['level'] = request.args.get('level', '')
        args_history['merger'] = request.args.get('merger', '')
        args_history['border'] = request.args.get('border', '')
        args_history['engin'] = request.args.get('engin', '')
        args_history['enginType'] = request.args.get('enginType', '')
        args_history['navigation'] = request.args.get('navigation', 'true')
        args_history['verify'] = request.args.get('verify', '')
        args_history['alexa'] = request.args.get('alexa', '')
        args_history['track'] = request.args.get('track', 'false')
        args_history['nosearchbox'] = request.args.get('nosearchbox', 'false')
        args_history['page'] = request.args.get('page', '')
        args_history['extension'] = request.args.get('extension', '')

        # crossrefQuery="other/gdc-speakers2018/filter=description:%s"
        args_history['crossrefQuery'] = request.args.get('crossrefQuery', '')

        cmd = genCmd(db, key, 
                      request.args.get('column', Config.column_num),
                      request.args.get('filter', ''),
                      request.args.get('style', str(Config.css_style_type)),
                      request.args.get('desc', 'true'),
                      request.args.get('width', ''),
                      request.args.get('row', ''),
                      request.args.get('top', ''),
                      request.args.get('level', ''),
                      request.args.get('merger', ''),
                      request.args.get('border', ''),
                      request.args.get('engin', ''),
                      request.args.get('enginType', ''),
                      request.args.get('navigation', 'true'),
                      request.args.get('verify', ''),
                      request.args.get('alexa', ''),
                      request.args.get('track', 'false'), '', request.args.get('nosearchbox', 'false'),
                      request.args.get('page', ''), args_history['extension'], request.args.get('crossrefQuery', ''))
        
        print '\ncmd  --->   '  + cmd + '   <---\n'
        html = subprocess.check_output(cmd, shell=True)
        return html

@app.route('/loadmore', methods=['POST'])
def handleLoadmore():
    print 'handleLoadmore'
    cmd = genCmd(request.form['db'], request.form['key'],
                      args_history['column'],
                      args_history['filter'],
                      args_history['style'],
                      args_history['desc'],
                      args_history['width'],
                      args_history['row'],
                      args_history['top'],
                      args_history['level'],
                      args_history['merger'],
                      args_history['border'],
                      args_history['engin'],
                      args_history['enginType'],
                      args_history['navigation'],
                      args_history['verify'],
                      args_history['alexa'],
                      args_history['track'], 'true', args_history['nosearchbox'],
                      args_history['page'], args_history['extension'])

    print '\ncmd  --->   '  + cmd + '   <---\n'
    html = subprocess.check_output(cmd, shell=True)
    return html





@app.route('/updateSearchEngine', methods=['POST'])
def handleUpdateSearchEngine():

    print request.form

    engin = request.form['engin']
    fileName = request.form['fileName']
    rTitle = request.form['rTitle']
    rID = request.form['rID']

    engin_list = utils.getEnginList('d:' + engin.strip(), fileName, recommend=Config.recommend_engin)

    #print engin_list

    engin_list_dict = utils.getEnginListLinks(engin_list, rTitle, rID, engin.strip(), useQuote=False, module='star', library=fileName, pluginsMode=False, fontSize=10)  #, '#33EE22')


    #print engin_list_dict

    html = ''
    count = 0
    for k, v in engin_list_dict.items():
        count += 1
        html += v

        if count >= Config.max_links_row:
            html += '<br>'
            count = 0


    return html

@app.route('/navigate', methods=['POST'])
def handleNavigate():
    #print request.form
    if request.form['rID'] == "":
        return ""
    return utils.handleExtension(form)

@app.route('/addRecord', methods=['POST'])
def handleAddRecord():
    data = request.form['data'].strip()
    fileName = request.form['fileName'].strip()
    print fileName 
    print data

    if data != '' and os.path.exists(fileName):
        f = open(fileName, 'a')
        f.write(toRecordFormat(data))
        f.close()

    return ''

@app.route('/exclusive', methods=['POST'])
def handleExclusive():
    print 'handleExclusive:'
    print request.form
    data = request.form['data'].strip()
    fileName = request.form['fileName'].strip()
    enginArgs = request.form['enginArgs'].strip()
    crossrefPath = request.form['crossrefPath'].strip()
    crossrefQuery = request.form['crossrefQuery'].strip()
    newTab = request.form['newTab'].strip()
    resourceType = request.form['resourceType'].strip()
    originFilename = request.form['originFilename'].strip()
    lastRID = request.form['rID'].strip()
    kgraph = request.form['kgraph'].strip()

    record = None
    desc = ''
    rID = ''

    text = data
    value = data
    if utils.getValueOrTextCheck(data):
        text = utils.getValueOrText(data, returnType='text')
        value = utils.getValueOrText(data, returnType='value')

    for d in data.strip().split(' '):
        rID += d[0 : 1].lower()


    if resourceType != '' and lastRID != '' and fileName != '':
        record = utils.getRecord(lastRID, path=fileName)

    if record != None and record.get_id().strip() == lastRID:
        #print '--->' + record.line
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : resourceType})
        if ret != None:
            for v in ret.split(','):
                v = v.strip()
                print v
                if v.startswith(data):
                    desc = utils.valueText2Desc(v, prefix=False)
                    print desc
                    break
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'crossref'})
        crossref = ''

        if crossrefPath != '':
            crossref = kg.getCrossref(text, crossrefPath)
        if ret != None:
            if crossref != '':
                crossref += ', ' + ret
            else:
                crossref = 'crossref:' + ret



        if crossref != '':
            crossref = crossref.replace('crossref:', '')
            crossrefDict = {}
            for c in crossref.split(','):
                c = c.strip()
                if crossrefDict.has_key(c):
                    continue
                else:
                    crossrefDict[c] = True

            crossref = 'crossref:'
            for k in crossrefDict.keys():
                crossref += k + ', '

            crossref = crossref.strip()
            if crossref.endswith(','):
                crossref = crossref[0 : len(crossref) - 1]

            print 'crossref->>' + crossref

            desc += ' ' + crossref


        desc += ' localdb:' + text

    else:

        targetPath = ' '.join(Config.exclusive_crossref_path)
        if crossrefPath != '':
            targetPath = ' ' +  crossrefPath
        desc = 'engintype:' + text + ' '
        desc += 'localdb:' + text
        desc += ' ' + kg.getCrossref(text, targetPath)
        if resourceType != '':
            desc += ' category:' + resourceType 

        kg_cache = kg.getKnowledgeGraphCache(text)
        if kg_cache != '':
            desc += ' ' + kg_cache
        elif kgraph == 'true':
            desc += ' description:' + resourceType + '#' + originFilename + '#' + lastRID


    url = ''
    if data.startswith('http'):
        url = data
    elif utils.getValueOrTextCheck(data):
        data = text
        if value.startswith('http'):
            url = value 
        elif resourceType != '' and utils.isAccountTag(resourceType + ':', tag.tag_list_account):
            url = utils.toQueryUrl(tag.tag_list_account[resourceType + ':'], value)

    newUrl = doExclusive(rID, data, url, desc)

    #print desc  
    for k, v in Config.exclusive_default_tab.items():
        if url.find(k) != -1:
            newUrl += '&extension=' + v
            break

    newUrl = newUrl + '&crossrefQuery="' + crossrefQuery.strip() + '"'

    url = newUrl
    
    if enginArgs.find(':') != -1:
        enginType = enginArgs[enginArgs.find(':') + 1 :]
        if enginType != 'star':
            url += '&enginType=' + enginType
    if crossrefPath != '':
        url += '&crossrefPath=' + crossrefPath

    print url
    if newTab == 'false':
        return 'refresh#' + url
    else:
        return url

@app.route('/getKnowledgeGraph', methods=['POST'])
def handleKnowledgeGraph():
    url = request.form['url'].strip()
    fileName = request.form['fileName'].strip()
    if os.path.exists(fileName):
        f = open(fileName, 'rU')
        lines = f.readlines()
        f.close()
        if ''.join(lines).find('keyword:') == -1:
            new_lines_record = []
            for line in lines:
                if line.strip() != '':
                    record = Record(line)
                    description = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'description'})
                    if description == None or description.strip() == '':
                        return ''
                    description = description.strip()
                    description_list = description.split('#')
                    print description
                    kb_str = kg.getKnowledgeGraph(record.get_title().strip(), description_list[0], '', description_list[2], description_list[1])
                    print kb_str
                    new_lines_record.append(Record(line.replace('\n', '').replace('description:' + description, '') + ' ' + kb_str))
            if len(new_lines_record) == 1:
                url = utils.output2Disk(new_lines_record, 'main', 'exclusive')
                if url != '':
                    return url
                else:
                    return ''
    return ''

def doExclusive(rID, title, url, desc):
    record = Record('custom-exclusive-' + rID + ' | '+ title + ' | ' + url + ' | ' + desc)
    return utils.output2Disk([record], 'main', 'exclusive') 



@app.route('/add2Library', methods=['POST'])
def handleAdd2Library():
    rid = request.form['rid']
    text = request.form['text'].encode('utf-8')
    resourceType = request.form['resourceType']
    library = request.form['library']

    r = utils.getRecord(rid, path=library)
    if r != None:
        args = { 'tag' : resourceType + ':' } 
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, args)

        itemDescDict = {}
        for item in ret.split(','):
            item = item.strip().encode('utf-8')
            if item.startswith(text):
                itemDescDict = utils.toDescDict(utils.valueText2Desc(item), library)
                break

        url = ''
        if itemDescDict.has_key('website'):
            homepage = itemDescDict['website']
            if homepage.find(',') != -1:
                homepage = homepage[0 : homepage.find(',')]

            url = utils.getValueOrText(homepage, returnType='value')

        desc = utils.dict2Desc(itemDescDict).replace(text + ' - ', '')
        line = rid + '-' + resourceType + ' | ' + text + ' | ' + url + ' | ' + desc + ' \n'

        if os.path.exists(library):
            f = open(library, 'a')
            f.write(line)
            f.close()

    return ''

@app.route('/add2QuickAccess', methods=['POST'])
def handleAdd2QuickAccess():
    rid = request.form['rid']
    text = request.form['text'].encode('utf-8')
    value = request.form['value'].encode('utf-8')
    resourceType = request.form['resourceType'].strip()
    library = request.form['library']

    print 'handleAdd2QuickAccess:' + text
    #print request.form

    itemDescDict = {}
    qaDescDict = {}

    if value == '':

        r = utils.getRecord(rid, path=library)
        if r != None:
            args = { 'tag' : resourceType + ':' } 
            ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, args)


            for item in ret.split(','):
                item = item.strip().encode('utf-8')
                if item.startswith(text):
                    print item
                    itemDescDict = utils.toDescDict(utils.valueText2Desc(item), library)
                    break
    else:
        item = ''
        newText = ''
        if text.find('(') != -1:
            newText = utils.getValueOrText(text, returnType='text')
        else:
            newText = text.strip()

        if newText.find(' - ') != -1:
            newText = newText[0 : newText.find(' - ')].strip()

        if resourceType == '':
            resourceType = newText.strip()

        item = newText.strip() + '(' + resourceType + '(' + value + '))' 

        itemDescDict = utils.toDescDict(utils.valueText2Desc(item, prefix=True), library)

    if len(itemDescDict) > 0:

        qaRecord = utils.queryQuickAccess(rid)

        if qaRecord != None:
            qaDescDict = utils.toDescDict(qaRecord.get_describe(), library)

        desc = utils.dict2Desc(utils.mergerDescDict(itemDescDict, qaDescDict))

        #print desc
        url = ''
        if len(lastOpenUrls) > 0:
            url = lastOpenUrls[len(lastOpenUrls) - 1]
        
        if url == '':
            url = utils.toQueryUrl(utils.getEnginUrl(Config.smart_link_engin), text)

        line = rid + ' | ' + Config.history_quick_access_name + ' | ' + url + ' | '
        line += desc + ' clickcount:1000 \n'

        editQuickAccessHistoryfile(line)

        return 'ok'

    #print r.line
    return ''
    
@app.route('/batchOpen', methods=['POST'])
def handleBatchOpen():
    data = request.form['data'].strip()
    resourceType = request.form['resourceType'].strip()

    if len(Config.smart_engin_for_command_batch_open) > 0:
        engins = Config.smart_engin_for_command_batch_open
        urls = ''
        for e in engins:
            epEngins = utils.expandEngins(e)
            if len(epEngins) > 5:
                epEngins = epEngins[0 : 5]
            for e2 in epEngins:
                url = utils.toQueryUrl(utils.getEnginUrl(e2), data)
                urls += url + ' '
                print url
        return urls

    return ''

@app.route('/allInOnePage', methods=['POST'])
def handleAllInOnePage():
    text = request.form['text'].strip()
    urls = request.form['urls'].strip()
    module = request.form['module'].strip()
    print 'text:' +text
    print 'urls:' + urls

    html = ''
    suportLinkHtml = ''
    notSuportLinkHtml = ''
    suportLink = {}
    notSuportLink = {}

    textArray = text.split(',')
    urlArray = urls.split(',')


    style = '<style>body {width:100%; background-color:#E6E6FA;}</style>'
    head = '<html><head>' + style + '</head><body><table>'
    end = '</body></html>'
    count = 0
    for i in range(0, len(urlArray)):
        itemText = textArray[i].strip()
        itemUrl = urlArray[i].strip()
        space = ''

        if utils.suportFrame(itemUrl, 0.8):
        #if True:
    
            print itemUrl + ' suport'
            suportLink[itemText] = itemUrl
            suportLinkHtml += '<a target="_black" href="' + itemUrl + '"><font style="font-size:10pt;">' + itemText + '</font></a>&nbsp;'
        else:
            notSuportLink[itemText] = itemUrl
            notSuportLinkHtml += '<a target="_black" href="' + itemUrl + '"><font style="font-size:10pt;">' + itemText + '</font></a>&nbsp;'

    count = 0
    row = ''
    htmlList = []
    if Config.open_all_link_in_frameset_mode == False:
        for k, v in suportLink.items():
            row += '<td><iframe  id="iFrameLink" width="470" height="700" frameborder="0"  src="' + v +'" ></iframe></td><td width="60" ></td><td width="60" ></td><td width="60" ></td>'
            count = count + 1
            if count == 3:
                html += '<tr>' + row + '</tr>'
                count = 0
                row = ''

        if row != '':
            html += '<tr>' + row + '</tr>' 

            html = head + '<div style="width:100%; background-color:#E6E6FA"><div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto; ">' + suportLinkHtml + \
        '&nbsp;&nbsp;/&nbsp;&nbsp; ' + notSuportLinkHtml + '</div><div style="height: 21px; width: 100px"></div>' + html + '</div>' + end

            htmlList = [html]
    else:
        for k, v in suportLink.items():
            row += '<frame src="' + v +'" ></frame>'
            count = count + 1
            if count == 4:
                frameset = '<frameset cols="25%,*,25%, 25%">' + row + '</frameset>'
                html += frameset
                htmlList.append(frameset)
                count = 0
                row = ''

        if row != '':
            if count == 1:
                
                frameset = '<frameset cols="100%">' + row + '</frameset>' 
                html += frameset
            if count == 2:
                frameset = '<frameset cols="*,50%">' + row + '</frameset>' 
                html += frameset
            if count == 3:
                frameset = '<frameset cols="*,30%,30%">' + row + '</frameset>' 
                html += frameset
            htmlList.append(frameset)



    if len(htmlList) > 0:
        for html in htmlList:
            outputDir = Config.output_data_to_new_tab_path + module + '/'
            if os.path.exists(outputDir) == False:
                os.makedirs(outputDir)
            fileName = 'onepage.html'
            cmd = "echo '" + html + "' > " + outputDir + fileName
            #print cmd
            output = subprocess.check_output(cmd, shell=True)    



            url =  Config.one_page_path_root + outputDir + fileName

            #for k, v in notSuportLink.items():
            #    if k != Config.history_quick_access_name:
            #        localOpenFile(v, fileType='.html')

            localOpenFile(url)

    else:
        for k, v in notSuportLink.items():
            if k != Config.history_quick_access_name:
                localOpenFile(v, fileType='.html')
    return ''


@app.route('/merger', methods=['POST'])
def handleMerger():
    rID = request.form['rID'].strip()
    fileName = request.form['originFilename'].strip()
    resourceType = request.form['resourceType'].strip()

    record = utils.getRecord(rID, path=fileName)

    if record != None and record.get_id().strip() == rID:
        args = { 'tag' : resourceType + ':' } 

        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)
        tagDict = {}
        for originText in ret.split(','):
            originText = originText.strip()
            print 'originText:' + originText
            if utils.getValueOrTextCheck(originText):
                print originText 
                text = utils.getValueOrText(originText, returnType='text')
                value = utils.getValueOrText(originText, returnType='value')

                
                desc = utils.valueText2Desc(originText, text=text, value=value, form=request.form, record=record,tagSplit='%%')
                for item in desc.split('%%'):
                    if item.strip() == '':
                        continue
                    index = item.find(':')
                    if index != -1:
                        tagStr = item[0 : index + 1]
                        tagValue = item[index + 1 :]
                        if tagDict.has_key(tagStr):
                            tagDict[tagStr] = tagDict[tagStr] + ', ' + tagValue
                        else:
                            tagDict[tagStr] = tagValue
                    print 'item: ' + item 
                print desc
                print '---'

        recordDesc = ''
        if len(tagDict) > 0:
            for k, v in tagDict.items():
                print k
                print v
                if k == 'description:':
                    continue
                values = v.strip()
                #ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : k})
                #if ret != None and ret.strip() != '':
                #    values += ', ' + ret.replace('\n', '')
                #    print 'values: ' + values
                recordDesc += k.strip() + values + ' '


            url = utils.output2Disk([Record(rID + '-' + resourceType + '-merger' + ' | ' +  record.get_title() + ' | ' + record.get_url() + ' | ' + recordDesc)], 'tag', rID + '-' + resourceType, ignoreUrl=False)

            line = rID + ' | ' + record.get_title().strip() + '-' + resourceType + '-merger | ' + utils.toQueryUrl(utils.getEnginUrl('glucky'), record.get_title().strip()) + ' | ' +  recordDesc
            toHistoryfile(line, fileName)
            return url


    return ''



@app.route('/createlist', methods=['POST'])
def handleCreateList():
    print 'handleCreateList'
    rID = request.form['rID'].strip()
    fileName = request.form['originFilename'].strip()
    resourceType = request.form['resourceType'].strip()

    if resourceType == 'twitter':
        record = utils.getRecord(rID, path=fileName)


    if record != None and record.get_id().strip() == rID:

        listName = record.get_title().strip().replace(' ', '-') + '-' + resourceType
 
        args = { 'tag' : resourceType + ':' } 
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)

        #api = twitter.Api()
        # need fill the key 
        api = twitter.Api(consumer_key='',
              consumer_secret='',
              access_token_key='',
              access_token_secret='',
              sleep_on_rate_limit=True,
              proxies=Config.proxies3)

        allList = api.GetLists(screen_name='wowdd1')

        for item in allList:
            if item.name == listName:
                api.DestroyList(owner_screen_name='wowdd1', list_id=item.id)

                print 'DestroyList:' + item.name

        twitterList = api.CreateList(listName)
        print 'CreateList:' + listName


        for user in ret.split(','):
            user = user.strip()

            twitterUser = api.GetUser(screen_name=user)
            try:
                api.CreateListsMember(list_id=twitterList.id, screen_name=user, owner_screen_name='wowdd1') 
            except Exception as e:
                print 'user ' + user + ' can not be add to list'

        return 'https://twitter.com/wowdd1/lists/' + listName

        print ret  


    return ''


@app.route('/tolist', methods=['POST'])
def handleToList():
    rID = request.form['rID'].strip()
    fileName = request.form['originFilename'].strip()
    resourceType = request.form['resourceType'].strip()

    print request.form

    record = utils.getRecord(rID, path=fileName)
    records = []
    textList = []
    accountTag = utils.isAccountTag(resourceType, tag.tag_list_account)

    if record != None and record.get_id().strip() == rID:
        args = { 'tag' : resourceType + ':' } 
        #print '&&&' + record.line
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)
        url = ''
        originText = ''
        for item in ret.split(','):
            originText = item
            text = utils.getValueOrText(item, returnType='text')
            value = utils.getValueOrText(item, returnType='value')

            item = text

            if accountTag:
                url = tag.tag_list_account[resourceType + ':'].replace('%s', item.strip())
                if item.find('/') != -1:
                    item = item[item.rfind('/') + 1 :]
            elif resourceType == 'crossref':
                if item.find('#') != -1:
                    result = utils.getCrossrefUrls(item.strip())
                    #print '^^^ ' + item
                    itemRecord = None
                    for k, v in result.items():
                        #if itemRecord == None:
                        path = 'db/' + item[0 : item.find('#')].strip()
                        #print '^^^ ' + path
                        itemRecord = utils.getRecord(k.strip(), path=path, matchType=2)
                            #print 'itemRecord ' + itemRecord.line

                        v = ''
                        if itemRecord != None and itemRecord.line.strip() != '':
                            records.append(Record(itemRecord.get_id() + ' | ' + k.strip() + ' | ' + v + ' | ' + itemRecord.get_describe().replace('\n', '') + ' path:' + path))
                        else:
                            records.append(Record(' | ' + k.strip() + ' | ' + v + ' | '))

                    continue
                else:
                    k, url = utils.getCrossrefUrl(item)
            elif value.find('homepage(') != -1:
                url = value[value.find('homepage')+ 9 : value.find(')', value.find('homepage'))]
            elif Config.smart_engin_for_tag.has_key(resourceType):
                url = utils.toQueryUrl(utils.getEnginUrl(Config.smart_engin_for_tag[resourceType][0]), item.strip())
            elif resourceType == 'website':
                url = value
            else:
                #url = utils.toQueryUrl(utils.getEnginUrl('glucky'), item.strip() + ' ' + resourceType)
                url = ''
            if url.startswith('http') == False:
                url = ''

            print url
            textList.append(item.strip())
            records.append(Record(' | ' + item + ' | ' + url + ' | ' + utils.valueText2Desc(originText, text=text, value=value, form=request.form, record=record, prefix=False)))
    if request.form.has_key('returnText'):
        return ', '.join(textList)
    if len(records) > 0:
        outputUrl = utils.output2Disk(records, 'tag', rID + '-' + resourceType, ignoreUrl=False)

        if record != None:
            toHistoryfile(rID + ' | ' + record.get_title().strip() + ' - ' + resourceType.strip() + ' | ' + outputUrl + ' |', fileName)

        return outputUrl

    return ''


def toRecordFormat(data):
    if data.find('|') != -1:
        return data + '\n'
    else:
        rID = 'custom-'
        for item in data.split(' '):
            rID += item[0 : 1]
        return rID + ' | ' + data + ' | | \n'

def localOpenFile(fileName, fileType=''):
    cmd = 'open "' + fileName + '"'
    app = ''
    if fileType == '':
        fileType = fileName
    for k, v in Config.application_dict.items():
        if fileType.lower().strip().endswith(k):
            app = v
            break
    if app == '':
        app = Config.application_dict['*']
    if os.path.exists(app):
        cmd = app.replace(' ', '\ ') + ' "' + fileName + '"'
        print cmd
        output = subprocess.check_output(cmd, shell=True)

@app.route('/exec', methods=['POST'])
def handleExec():
    command = request.form['command']
    fileName = request.form['fileName']
    print command + ' ' + fileName
    output = ''
    if command == 'open':
        localOpenFile(fileName)
    elif command == 'edit':
        cmd = 'open "' + fileName + '"'
        sublime = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'
        if os.path.exists(sublime):
            cmd = sublime.replace(' ', '\ ') + ' "' + fileName.strip() + '"'
        print cmd
        output = subprocess.check_output(cmd, shell=True)
    elif command == 'deleteRow':
        if os.path.exists(fileName):
            f = open(fileName, 'rU')
            all_lines = []
            key = request.form['key'].strip()
            for line in f.readlines():
                r = Record(line)
                if key != r.get_url().strip():
                    all_lines.append(line)
                else:
                    print 'deleteRow'
                    print line
            f.close()
            
            f = open(fileName, 'w')
            if len(all_lines) > 0:
                for line in all_lines:
                    f.write(line)
            else:
                f.write('')
                f.close()
            

    return output

@app.route('/queryStarEngin', methods=['POST'])
def handlerQueryStarEngin():
    rID = request.form['rID']
    rTitle = request.form['rTitle']
    targetid = request.form['targetid']
    return ''

def getCrossrefUrls(content):
    urls = []
    if content.find('#') != -1:
        #print content + '<br>'
        data = content.strip().split('#')
        
        if len(data) != 2:
            return ''
        filters = []
        if data[1].find('+') != -1:
            filters = data[1].split('+')
        else:
            filters = [data[1]]

        db = data[0][0 : data[0].rfind('/') + 1].strip()
        key = data[0][data[0].rfind('/') + 1 :].strip()
        for ft in filters:
            #print ft + '<br>'
            link = 'http://localhost:5000/?db=' + db + '&key=' + key + '&filter=' + ft
            urls.append(link)
    return urls

@app.route('/queryNavTab', methods=['POST'])
def handleQueryNavTab():
    print '-queryNavTab-'
    print request.form
    url = request.form['url']
    targetid = request.form['targetid']
    title = request.form['rTitle']
    otherInfo = request.form['otherInfo']
    column = request.form['column']

    if request.form.has_key('crossrefQuery') and request.form['crossrefQuery'].strip() != '':
        return 'pathways,' + Config.default_tab

    if targetid.find('bookmark') != -1:
        return 'bookmark,' + Config.default_tab
    if url != None and url != '':
        if url.find(Config.ip_adress) != -1:
            return 'pathways,' + Config.default_tab
        if url.find('youtube') != -1:
            if url.find('watch') != -1:
                return 'preview,' + Config.default_tab
            if url.find('playlist') != -1:
                return Config.default_tab
                #return 'reference,' + Config.default_tab
            
        if url.startswith('/User') and url[url.rfind('/') :].find('.') == -1:
            return 'filefinder,' + Config.default_tab
        if url.find('weixin') != -1:
            return 'preview,' + Config.default_tab

        if otherInfo.find('website') != -1 or otherInfo.find('homepage') != -1:
            return 'preview,' + Config.default_tab

        #if url.startswith('http'):
        #    return Config.default_tab + ',preview'


    if targetid != None and targetid != '':
        if targetid.find('content-') != -1:
            return 'content,' + Config.default_tab
        if targetid.find('history-') != -1:
            return 'history,' + Config.default_tab


    return Config.default_tab + ',' + Config.second_default_tab


@app.route('/queryUrl', methods=['POST'])
def handleQueryUrl():
    result = ''
    aid = ''
    refreshID = ''
    print request.form
    if request.form.has_key('aid'):
        aid = request.form['aid'].strip()
    if request.form.has_key('refreshID'):
        refreshID = request.form['refreshID'].strip()

    if request.form.has_key('isTag') and (request.form['isTag'] == True or request.form['isTag'] == 'True' or request.form['isTag'] == 'true'):
        record = utils.getRecord(request.form['rID'], path=request.form['fileName'])
        #print record.line
        if record != None and record.get_id().strip() == request.form['rID']:
            args = { 'tag' : request.form['searchText'].strip() + ':' } 
            ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)
            #print 'ret ' + ret
            if ret != None:
                if ret.find(', ') != -1:
                    ret = ret.split(',')
                else:
                    ret = [ret]

                if request.form.has_key('type') and request.form['type'] == 'dialog':
                    resultDict = utils.clientQueryEnginUrl2(request.form['searchText'], resourceType=request.form['resourceType'], enginArgs=request.form['enginArgs'])      
                    count = 0
                    result = ''
                    for k, v in resultDict.items():
                        count += 1

                        script = ''
                        for q in ret:
                            script += "window.open('" + utils.toQueryUrl(utils.getEnginUrl(k.strip()), q.strip()).strip().replace('#', '') + "');"
                        result += '<a target="_blank" href="javascript:void(0);" onclick="' + script + '" style="color:#999966;font-size:10pt;">' + k + '</a>'+ '&nbsp;'
                        if count % Config.recommend_engin_num_dialog_row == 0 and count > 0 and len(resultDict) != Config.recommend_engin_num_dialog_row:
                            result += '<br>'
                        if count >= Config.recommend_engin_num_dialog:
                            break
                    if len(Config.command_for_tag_dialog) > 0:
                        #library = os.getcwd() + '/db/library/' + Config.default_library;
                        result += '<br>' + dialogCommand(request.form['fileName'], request.form['searchText'], request.form['resourceType'], request.form['fileName'], request.form['rID'], tagCommand=True, aid=aid)

                    if utils.isAccountTag(request.form['searchText'].strip(), tag.tag_list_account) and len(ret) > Config.max_account_for_tag_batch_open:
                        
                        if request.form['searchText'].strip() == 'twitter':
                            script = "createlist('" + request.form['rID'].strip() + "', 'twitter','" + request.form['fileName'].strip() + "');"
                            result += utils.enhancedLink('', '#createlist', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
                        count = 0
                        base = 0
                        for i in range(0, len(ret)):
                            count += 1
                            if count >= Config.max_account_for_tag_batch_open:
                                text = request.form['searchText'].strip() + '(' + str(base * Config.max_account_for_tag_batch_open + 1) + '-' + str(base * Config.max_account_for_tag_batch_open + count) + ')'
                                base += 1
                                count = 0

                                result += ' ' + utils.genTagLink(text, 'dialog', request.form['library'], request.form['rID'], request.form['resourceType'].strip(), False, '', suffix='', searchText=request.form['searchText'].strip(), fileName=request.form['fileName'])

                                #print result

                        if count != 0:
                            text = request.form['searchText'].strip() +'(' + str(base * Config.max_account_for_tag_batch_open + 1) + '-' + str(base * Config.max_account_for_tag_batch_open + count) + ')'
                            result += ' ' + utils.genTagLink(text, 'dialog', request.form['library'], request.form['rID'], request.form['resourceType'].strip(), False, '', suffix='', searchText=request.form['searchText'].strip(), fileName=request.form['fileName'])
                            base += 1

                            count = 0

                    #print result
                    return result
                else:
                    urls = ''
                    if request.form['resourceType'] == 'crossref':
                        for q in ret:
                            urlList = getCrossrefUrls(q.strip())
                            urls += ' '.join(urlList) + ' '
                        return urls
                    else:
                        if utils.isAccountTag(request.form['searchText'] + ':', tag.tag_list_account):
                            print 'request.form:' + request.form['text']
                            count = 0
                            start = 1
                            end = len(ret)
                            if request.form['text'] != request.form['searchText'] and utils.getValueOrTextCheck(request.form['text']):
                                value = utils.getValueOrText(request.form['text'], returnType='value')
                                start = int(value[0 : value.find('-')].strip())
                                end = int(value[value.find('-') + 1 :].strip())
                            
                            for q in ret:
                                count += 1
                                if count >= start and count <= end:
                                    url = tag.tag_list_account[request.form['searchText'] + ':'].replace('%s', q.strip())
                                    urls += url + ' '
                                    print url
      
                        else:
                            for q in ret:
                                url = utils.toQueryUrl(utils.getEnginUrl('glucky'), q)
                                urls +=  url + ' '
                                print url
                        #print urls + '<<<<'
                        #return ''
                        return urls
            else:
                return ''
        else:
            return ''

    if request.form.has_key('type'):
        if request.form['type'] == 'dialog':
            engin_args = request.form['enginArgs']

            if request.form['resourceType'] == 'localdb':
                print request.form['library']
                print request.form['rID']
                count = 0
                dirs = utils.clientQueryDirs(Config.exclusive_local_db_path, rID=request.form['rID'], fileName=request.form['library'])
                dirs += [Config.exclusive_local_db_path, 'db/library']
                for item in dirs:
                    count += 1

                    link = 'http://' + Config.ip_adress + '/?db=other/main/&key=exclusive2016&crossrefPath=' + item 
                    title = item[item.rfind('/') + 1: ]
                    script = "exclusive('" + request.form['fileName'] + "', '" + request.form['searchText'] + "', '" + item + "', false, '" + request.form['resourceType'] + "', '" + request.form['fileName'] + "', '" + request.form['rID'] + "', engin_args, false);"

                    result += utils.enhancedLink('', title, searchText=request.form['searchText'], style="color:#999966; font-size:10pt;", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], script=script, ignoreUrl=True) + '&nbsp;'
                    
                    if count % 5 == 0 and count > 0:
                        result += '<br>'

                return str(count) + '#' + result
            elif request.form['resourceType'] == 'engintype':
                enginTypes = utils.getNavLinkList('', searchEnginOnly=True)
                count = 0
                for et in enginTypes:
                    count += 1
                    script = "exclusive('exclusive', '" + request.form['searchText'] + "', '', false, '', '" + request.form['fileName'] + "', '" + request.form['rID'] + "', 'd:" + et + "', false);"
                    
                    result += '<a target="_blank" href="javascript:void(0);" onclick="' + script + '"style="color:#999966;font-size:10pt;">' + et + '</a>'+ '&nbsp;'
                
                    if count % 9 == 0 and count > 0:
                        result += '<br>'
                return result
            elif request.form['searchText'] == 'more' and request.form['resourceType'] == '':
                html = utils.gen_libary2('', '', libraryList=Config.menu_library_list, inLibary=False).replace('#', '')
                html = html.split('&nbsp;')
                count = 0
                for item in html:
                    count += 1
                    result += item + '&nbsp;'
                    if count % 4 == 0 and count > 0:
                        result += '<br>'
                return result
            else:
                resultDict = utils.clientQueryEnginUrl2(request.form['searchText'], resourceType=request.form['resourceType'], enginArgs=request.form['enginArgs'])
                
                count = 0
                value = utils.getValueOrText(request.form['originText'], returnType='value')

                searchHtml = ''
                commandHtml = ''
                infoHtml = ''
                infoLen = 0
                infoBR = False
                infoBRCount = 0
                textList = []
                linkList = []

                for k, v in resultDict.items():
                    count += 1

                    if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                        v = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
                            
                    searchHtml += utils.enhancedLink(v, utils.formatEnginTitle(k), searchText=request.form['searchText'], style="color:#999966; font-size: 10pt;", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], refreshID=refreshID) + '&nbsp;'
                    if count % Config.recommend_engin_num_dialog_row == 0 and count > 0 and len(resultDict) != Config.recommend_engin_num_dialog_row:
                        searchHtml += '<br>'
                    if count >= Config.recommend_engin_num_dialog:
                        break                    
                if len(Config.command_for_dialog) > 0:
                    #library = os.getcwd() + '/db/library/' + Config.default_library;
                    commandHtml += '<br>' + dialogCommand(request.form['fileName'], request.form['searchText'], request.form['resourceType'], request.form['fileName'], request.form['rID'], aid=aid)
                if utils.getValueOrTextCheck(request.form['originText']):
                    valueList = [value]
                    text = utils.getValueOrText(request.form['searchText'], returnType='text')
                    if value.find('+') != -1:
                        valueList = value.split('+')
                    infoHtml += '<br>'
                    count = 0
                    dialogAID = ''
                    for v in valueList:
                        count += 1
                        if aid != '':
                            dialogAID = aid + '-' + str(count)
                        if utils.search_engin_dict.has_key(v):
                            v = utils.toQueryUrl(utils.getEnginUrl(v), text)
                        if utils.isUrlFormat(v):
                            if utils.isShortUrl(v) == False and v.startswith('http') == False:
                                v = 'http://' + v
                            infoHtml += utils.enhancedLink(v, text, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], aid=dialogAID, refreshID=refreshID)
                            infoLen += len(text)
                            textList.append(text)
                            linkList.append(v)

                        elif utils.getValueOrTextCheck(v):
                            subValue = utils.getValueOrText(v, returnType='value')
                            subText = utils.getValueOrText(v, returnType='text')
                            originSubValue = subValue
                            subValueIsEngin = False
                            if utils.search_engin_dict.has_key(subValue):
                                subValue = utils.getEnginUrl(subValue)
                                subValueIsEngin = True

                            elif tag.tag_list_account.has_key(subValue + ':'):
                                subValue = tag.tag_list_account[subValue + ':']
                                subValueIsEngin = True

                            if Config.smart_engin_for_tag.has_key(originSubValue):
                                subValue = 'http://_blank'
                                subValueIsEngin = True

                            if utils.isUrlFormat(subValue):
                                if utils.isShortUrl(subValue) == False and subValue.startswith('http') == False:
                                    subValue = 'http://' + subValue
                                subTextList = [subText]
                                if subText.startswith('[') and subText.endswith(']'):
                                    subText = subText[1 : len(subText) - 1]
                                    subTextList = subText.split('*')

                                count = 0
                                for st in subTextList:
                                    sv = subValue
                                    count += 1
                                    rt = request.form['resourceType']
                                    urlFromServer = False
                                    linkText = text + ' - ' + st
                                    log = True

                                    if subValueIsEngin:
                                        if Config.smart_engin_for_tag.has_key(originSubValue):
                                            rt = originSubValue
                                            urlFromServer = True
                                            linkText = st
                                            log = False
                                        else:
                                            sv = utils.toQueryUrl(subValue, st)
                                    else:
                                        if subValue.find('%s') != -1:
                                            sv = subValue.replace('%s', st)
                                    if Config.website_icons.has_key(st.strip().lower()):
                                        iconHtml = utils.getIconHtml(st)
                                        infoHtml += utils.enhancedLink(sv, linkText, showText=iconHtml, module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=rt, aid=dialogAID, refreshID=refreshID, urlFromServer=urlFromServer, log=log)
                                        infoLen += 1

                                    else:
                                        infoHtml += utils.enhancedLink(sv, linkText, showText=st, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=rt, aid=dialogAID, refreshID=refreshID, urlFromServer=urlFromServer, log=log)
                                        iconHtml = utils.getIconHtml(sv)
                                        if iconHtml != '':
                                            infoHtml = infoHtml.strip() + iconHtml.strip()
                                        infoLen += len(st) + 1

                                    if count > 15:
                                        infoHtml += '<br>'
                                        count = 0
                                    else:
                                        infoHtml += '&nbsp;'
                                    textList.append(st)
                                    linkList.append(sv)

                            else:
                                oldSubText = subText
                                if utils.getValueOrTextCheck(subValue):
                                    subText = utils.getValueOrText(subValue, returnType='text')
                                    subValue = utils.getValueOrText(subValue, returnType='value')
                                    if utils.search_engin_dict.has_key(subValue):
                                        subValue = utils.toQueryUrl(utils.getEnginUrl(subValue), subText)
                                        subText = oldSubText
                                        
                                if utils.isAccountTag(subText, tag.tag_list_account):
                                    subValueList = [subValue]
                                    if subValue.find('*') != -1:
                                        subValueList = subValue.split('*')
                                    for sv in subValueList:
                                        url = tag.tag_list_account[subText + ':']

                                        if url.find('%s') != -1:
                                            url = url.replace('%s', sv)
                                        else:
                                            url = url + sv
                                        if oldSubText != sv:
                                            subText = oldSubText

                                        if Config.website_icons.has_key(subText.strip().lower()):
                                            iconHtml = utils.getIconHtml(subText)
                                            infoHtml += utils.enhancedLink(url, text, showText=iconHtml, module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], aid=dialogAID, refreshID=refreshID)
                                            infoLen += 1

                                        else:
                                            infoHtml += utils.enhancedLink(url, text + ' - ' + subText, showText=subText, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], aid=dialogAID, refreshID=refreshID)
                                            infoLen += len(subText)
                                        textList.append(subText)
                                        linkList.append(url)
                                elif subText == 'crossref':
                                    values = []
                                    if subValue.find('*') != -1:
                                        values = subValue.split('*')
                                    else:
                                        values = [subValue]
                                    count = 0
                                    for v in values:
                                        count += 1
                                        key, url = utils.getCrossrefUrl(v)
                                        vtext = v
                                        if v.find('/') != -1:
                                            vtext = v[v.rfind('/') + 1 :]
                                        infoHtml += utils.enhancedLink(url, vtext, showText=vtext, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], aid=dialogAID, refreshID=refreshID)
                                        infoLen += len(vtext)
                                        textList.append(vtext)
                                        linkList.append(url)
                                        if count != len(values):
                                            infoHtml += ' '
                                else:
                                    url = utils.bestMatchEnginUrl(subValue, resourceType=request.form['resourceType'])
                                    infoHtml += utils.enhancedLink(url, text + ' - ' + subText, showText=subText, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'], aid=dialogAID, refreshID=refreshID)
                                    infoLen += len(subText)
                                    textList.append(subText)
                                    linkList.append(url)



                        else:
                            infoHtml += '<font style="color:#002244; font-size: 9pt">' + v + '</font>'
                            infoLen += len(v)

                        if len(valueList) > 1 and count != len(valueList):
                            infoHtml += ' / '
                            infoLen += 3
                        if infoLen - 40 > 0:
                            if count != len(valueList):
                                infoHtml += '<br>'
                                infoLen -= 40
                                infoBRCount += 1
                            if infoBRCount >= 2:
                                infoBR = True
 

                if len(linkList) > 1:
                    print textList
                    print '\n'.join(linkList)
                    script = utils.getBatchOpenScript(textList, linkList, 'dialog')
                    infoHtml += ' /&nbsp;' + utils.enhancedLink('', '#all', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;")

                if infoBR:
                    result = infoHtml[4:] + commandHtml 
                else:
                    result = searchHtml + commandHtml + infoHtml
                    result = result.replace('<br><br>', '<br>')

                result = str(count) + '#' + result
    else:
        resultDict = utils.clientQueryEnginUrl(request.form['url'], request.form['searchText'], request.form['resourceType'], request.form['module'])
        for k, v in resultDict.items():
            if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                resultDict[k] = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
        result = ' '.join(resultDict.values())

    return result

def dialogCommand(fileName, text, resourceType, originFilename, rID, tagCommand=False, aid=''):
    result = ''
    if tagCommand:
        for command in Config.command_for_tag_dialog:
            if command == 'tolist':
                script = "tolist('" + rID + "', '" + resourceType + "','" + originFilename + "');"
                result += utils.enhancedLink('', '#tolist', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
            if command == 'merger':
                script = "merger('" + rID + "', '" + resourceType + "','" + originFilename + "');"
                result += utils.enhancedLink('', '#merger', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
    else:
        for command in Config.command_for_dialog:
            if command == 'add2library':
                script = "add2Library('" + rID + "', '" + aid + "', '" + text + "', '" + resourceType + "', '" + fileName + "');"
                result += utils.enhancedLink('', '#add2' + fileName[fileName.rfind('/') + 1 :].replace('-library', ''), script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
            elif command == 'add2qa':
                script = "add2QuickAccess('" + rID + "', '" + aid + "', '" + text + "', '', '" + resourceType + "', '" + fileName + "');"
                result += utils.enhancedLink('', '#add2qa', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
                print result
            elif command == 'exclusive':
                script = "exclusive('" + fileName + "', '" + text + "', '', true, '" + resourceType + "', '" + originFilename + "', '" + rID + "', engin_args, false);"
                result += utils.enhancedLink('', '#exclusive', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
            elif command == 'trace':
                script = "batchOpen('" + text + "', '" + resourceType + "');"
                result += utils.enhancedLink('', '#trace', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
            elif command == 'kgraph':
                script = "exclusive('" + fileName + "', '" + text + "', '', true, '" + resourceType + "', '" + originFilename + "', '" + rID + "', engin_args, true);"
                result += utils.enhancedLink('', '#kgraph', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'

    return result

lastOpenUrls = []
lastOpenUrlsDict = {}
autoGenHistory = {}

@app.route('/syncQuickAccess', methods=['POST'])
def handleSyncQuickAccess():
    rid = request.form['rid'].strip()
    fileName = request.form['fileName'].strip()
    print 'handleSyncQuickAccess:' + rid + ' ' + fileName
    if rid != '' and autoGenHistory.has_key(rid) and fileName!= '':
        values = autoGenHistory[rid]
        if values != '':
            desc =  getQuickAccessDesc(values)
            print 'handleSyncQuickAccess:' + desc

            url = ''
            if len(lastOpenUrls) > 0:
                url = lastOpenUrls[len(lastOpenUrls) - 1]
            line = rid + ' | ' + Config.history_quick_access_name + ' | ' + url + ' | '
            line += desc + ' clickcount:1000 \n'

            editQuickAccessHistoryfile(line)
            autoGenHistory[rid]= ''
    return ''

def getQuickAccessDesc(values):
    itemDict = {}
    itemDesc = ''
    if values == '':
        return ''
    if values.find(',') != -1:
        for item in values.split(','):
            item = item.strip()
            if item == '':
                continue
            itemKey = item[0 : item.find(':')]
            itemValue = item[item.find(':') + 1 :].strip()
            if itemDict.has_key(itemKey):
                itemDict[itemKey] = itemDict[itemKey] + ', ' + itemValue
            else:
                itemDict[itemKey] = itemValue
    else:
        itemDict[values[0 : values.find(':')]] = values[values.find(':') + 1 :].strip()


    for ik, iv in itemDict.items():
        itemDesc += ik + ':' + iv + ' ' 

    return itemDesc

 
@app.route('/toSlack', methods=['POST'])
def handleToSlack():
    title = request.form['title'].strip().replace('%20', ' ')
    url = request.form['url'].strip()

    toSlack(title, url)


def toSlack(title, url):
    if url != '':
        message = ''
        if title != '':
            if utils.getValueOrTextCheck(title):
                title = utils.getValueOrText(title, returnType='text')
            message += title + ' '
        message += url
        utils.slack_message(message)

 
@app.route('/getPluginInfo', methods=['POST'])
def handlePluginInfo():
    
    title = request.form['title'].strip().replace('%20', ' ')
    url = request.form['url'].strip()

    if utils.getValueOrTextCheck(title):
        url = utils.getValueOrText(title, returnType='value')
        title = utils.getValueOrText(title, returnType='text')

    print 'handlePluginInfo'
    print request.form


    if title == '':
        toSlack(title, url)

    if title != '':
        crossref = kg.getCrossref(title)

        if crossref != '':
            crossrefList = []
            if crossref.find(',') != -1:
                crossrefList = crossref.split(',')
            else:
                crossrefList = [crossref]

            html = ''
            resultDict = {}
            for cr in crossrefList:
                cr = cr.replace('crossref:', '')
                if cr.find('#') != -1:
                    #print cr
                    result = utils.getCrossrefUrls(cr)
                    #print result
                    for k, v in result.items():
                        resultDict[k] = v
                else:
                    #print cr
                    k, v = utils.getCrossrefUrl(cr)
                    resultDict[k] = v
                    #print k + ' ' + v

 
            linkDict = genPluginInfo(resultDict, returnDict=True)


            for k, v in resultDict.items():
                #print v
                path = ''
                rTitle = ''
                for sv in v.split('&'):
                    if sv.find('db') != -1:
                        path += 'db/' + sv[sv.find('db') + 3:]
                    if sv.startswith('key'):
                        path += sv[sv.find('key') + 4:]
                    if sv.startswith('filter'):
                        rTitle = sv[sv.find('filter') + 7:]
                print path + ' ' + rTitle

                r = utils.getRecord(rTitle, path=path, matchType=2)
                if r != None and r.get_id().strip() != '':
                    library = path[path.rfind('/') + 1 :]
                    print library
                    #desc = r.get_desc_field2(utils, title, tag.get_tag_list(library), toDesc=True, prefix=False)
                    descList = r.get_desc_field3(utils, title, tag.get_tag_list(library), toDesc=True, prefix=False)

                    for desc in descList:
                        if desc != None and desc != '':
                            #print k
                            #print desc

                            descHtml = utils.genDescHtml(desc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=1)

                            if linkDict.has_key(k):
                                html += linkDict[k]  + descHtml + '<br>'
                                linkDict[k] = ''
                            else:
                                html += descHtml + '<br>'

                path = ''

            html2 = ''
            for k, v in linkDict.items():
                if v != '':
                    html2 += v + '  '

            if html2 != '':
                html = html + '<br>' + html2

            style = ''

            if request.form.has_key('style'):
                style = 'style="' + request.form['style'] + '" '

            if html != '':
                html = '<div align="left" ' + style + '>' + html + '</div>'
            return html

    elif request.form.has_key('url') and request.form['url'].find(Config.ip_adress) == -1:
        form = utils.getExtensionCommandArgs('plugin', '', request.form['url'], 'plugin', 'social', 'getPluginInfo', '')
        print form
        return utils.handleExtension(form)

    else:
        return genPluginInfo(lastOpenUrlsDict)

def genPluginInfo(dataDict, returnDict=False):
    html = ''
    lens = 0
    linkDict = {}
    for k, v in dataDict.items():
        lens += len(k)
        link = '<a target="_blank" href="' + v + '" style="font-family:San Francisco;"><font style="font-size:9pt; font-family:San Francisco;">' + k + '</font></a>'
        icon = utils.getIconHtml(v)
        if returnDict:
            linkDict[k] = link + icon
        else:
            html += link + icon + '  '
        if lens > 70:
            lens = 0
            html += '<br>'
    if returnDict:
        return linkDict
    else:
        return html   

@app.route('/userlog', methods=['POST'])
def handleUserLog():
    dt = str(datetime.datetime.now())
    linktext = request.form['text'].replace('%20', ' ').strip()
    searchText = request.form['searchText'].replace('%20', ' ')
    resourceType = request.form['resourceType'].strip()
    url = request.form['url'].strip()
    aid  = ''
    refreshID = ''
    if request.form.has_key('aid'):
        aid = request.form['aid'].strip()
    if request.form.has_key('refreshID'):
        refreshID = request.form['refreshID'].strip()
    print 'handleUserLog--->  ' + dt[0 : dt.rfind('.')] + '  <---'
    print '     aid: ' + aid
    print '     refreshID: ' + refreshID 
    print '     linktext: ' + linktext
    print '     searchText: ' + searchText
    print '     url: ' + url
    print '     module: ' + request.form['module']
    library = request.form['library']
    if library.find('db/') != -1:
        library = library[library.find('db/') :]
    print '     library: ' + library
    print '     rid: ' + request.form['rid']
    print '     resourceType: ' + resourceType
    print '     user: ' + request.form['user']
    print '     os: ' + request.form['os']
    print '     browser: ' + request.form['browser']
    print '     mac: ' + request.form['mac']
    print '     ip: ' + request.form['ip']
    print '     from: ' + request.form['from']


    if url != '':

        lastOpenUrls.append(url)

        if utils.getValueOrTextCheck(searchText):
            key = utils.getValueOrText(searchText, returnType='text') 
            lastOpenUrlsDict[key] = url
        else:
            lastOpenUrlsDict[linktext] = url
        if len(lastOpenUrls) > Config.max_last_open_urls:
            lastOpenUrls.remove(lastOpenUrls[0])
        if len(lastOpenUrls) > 0:
            print "lastOpenUrls:"
            for url in lastOpenUrls:
                print url
            print ''
    
    module = request.form['module'].strip()

    if Config.history_enable_quick_access:
        autoGenLine = ''
        if autoGenHistory.has_key(request.form['rid']):
            autoGenLine = autoGenHistory[request.form['rid']]
        if library == '' and module == 'history' and linktext != '' and linktext.lower() != Config.history_quick_access_name.lower():
            desc = ''
            if resourceType == 'website':
                desc = 'website:' + linktext
            else:
                desc = resourceType + ':' + linktext

            print desc

            if autoGenLine.find(desc) == -1:
                if autoGenLine == '':
                    autoGenLine += desc
                else:
                    autoGenLine += ', ' + desc

            autoGenHistory[request.form['rid']] = autoGenLine

        if len(autoGenHistory.items()) > 0:
            for k, v in autoGenHistory.items():
                print k + ' ' + v
                itemCount = 0
                if v.find(',') != -1:
                    itemCount = len(v.split(','))

                if itemCount > Config.history_quick_access_item_count:
                    itemDesc = getQuickAccessDesc(v)
                    #print itemDesc

                    if request.form['rid'].strip() != '':
                        line = request.form['rid'] + ' | ' + Config.history_quick_access_name + ' | ' + request.form['url'] + ' | '
                        line += itemDesc + ' clickcount:1000 \n'

                        editQuickAccessHistoryfile(line)
                        autoGenHistory[request.form['rid']] = ''

                    print line
                else:
                    if request.form['rid'].strip() != '' and request.form['url'].strip() != '':
                        line = request.form['rid'].strip() + ' | ' + Config.history_quick_access_name + ' | ' + request.form['url'].strip() + ' | \n'
                        editQuickAccessHistoryfile(line, onlyEditUrl=True)
        else:
            if request.form['rid'].strip() != '' and request.form['url'].strip() != '':
                line = request.form['rid'].strip() + ' | ' + Config.history_quick_access_name + ' | ' + request.form['url'].strip() + ' | \n'
                editQuickAccessHistoryfile(line, onlyEditUrl=True)

        print autoGenHistory

    if library != '' and request.form['rid'].strip() != '' and request.form['url'].strip() != '' and igonLog(module) == False:
        title = utils.getValueOrText(request.form['searchText'].replace('|', ''), returnType='text').strip()

        if resourceType != '' and \
            utils.isAccountTag(resourceType, tag.tag_list_account) == False and\
            utils.getValueOrTextCheck(request.form['searchText']):
            
            title += ' - ' + resourceType

        line = request.form['rid'] + ' | ' + title + ' | ' + request.form['url'] + ' | '

        desc = ''
        if module == 'dialog' and resourceType != '':
            record = utils.getRecord(request.form['rid'].strip(), path=library, use_cache=False)
            #if record != None:
            #    print record.line
            if title.find(' - ') != -1:
                title = title[0 : title.find(' - ')].strip()
            if record != None:
                desc = record.get_desc_field(utils, resourceType, title, toDesc=True)

        if resourceType != '':

            desc = desc.strip() + ' category:' + resourceType

        line += desc.strip() + ' '

        toHistoryfile(line, library)
        #utils.slack_message(request.form['url'], 'general')

    return ''

def toHistoryfile(line, library):
    if library.find('/') != -1:
        library = library[library.rfind('/') + 1 :]
    historyFile = 'extensions/history/data/' + library + '-history'

    
    cmd = 'echo "' + line + '" >> ' + historyFile
    print cmd
    output = subprocess.check_output(cmd, shell=True) 

def editQuickAccessHistoryfile(line, onlyEditUrl=False):

    historyFile = utils.getQuickAccessHistoryFileName()

    if os.path.exists(historyFile):
        f = open(historyFile, 'r+')
        r = Record(line)
        allLine = []
        found = False
        for qline in f.readlines():
            record = Record(qline)
            if record.get_id().strip() == r.get_id().strip():
                if onlyEditUrl:
                    allLine.append(record.get_id().strip() + ' | ' + record.get_title().strip() + ' | ' + r.get_url().strip() + ' | ' + record.get_describe().strip() + '\n')
                else:
                    allLine.append(line)
                found = True
            else:
                allLine.append(qline)
        f.close()

        f = open(historyFile, 'w')

        if found == False and onlyEditUrl == False:
            allLine.append(line)
        for qline in allLine:
            f.write(qline)



        f.close()


def igonLog(module):
    for md in Config.igon_log_for_modules:
        if module.strip() == md:
            return True
    return False

@app.route('/agent', methods=['POST'])
def handleAgent():
    print 'handleAgent'
    agentName = request.form['agentName']
    rid = request.form['rid']
    path = request.form['path']
    print agentName + ' ' + rid + ' ' + path
    return ''

@app.route('/extensions', methods=['POST'])
def handleExtension():
    if request.args.get('verify', '') != '':
        request.form['fileName'] = request.args.get('verify', '')

    return utils.handleExtension(request.form)


@app.route('/extensionJobDone', methods=['POST'])
def handleExtensionJobDone():
    print 'handleExtensionJobDone:'
    print '    rID:' + request.form['rID']
    print '    rTitle:' + request.form['rTitle'].replace('%20', ' ')
    print '    name:' + request.form['name']
    return 'ok'

@app.route('/thumb', methods=['POST'])
def handleThumb():
    url = request.form['url']
    if request.form['fileName'].find('papers') != -1:
        return ''
    if url != '':
        try:
            output = subprocess.check_output("curl --max-time 1 --head " + 'https://api.thumbalizr.com/?url=' + url + '&width=1280&quality=100', shell=True)
        except Exception as e:
            print e
    return url


@app.route('/chrome', methods=['GET', 'POST'])
def chrome():
    return utils.gen_plugin_content(request.form['title'], request.form['url'])

    

@app.route('/web_content/chrome/<page>', methods=['GET', 'POST'])
def web(page):
    print page
    f = open('web_content/chrome/output.html', 'rU')

    data = f.read()
    #print data
    f.close()
    return data

def genCmd(db, key, column_num, ft, style, desc, width, row, top, level, merger, border, engin, enginType, navigation, verify, alexa, track, loadmore, nosearchbox, page, extension, crossrefQuery):
    print 'track:' + track
    print 'nosearchbox:' + str(nosearchbox)
    if db.endswith('/') == False:
        db += '/'
    cmd = "./list.py -i " + Config.default_db + "/" + db + key + " -b 4"
    if db != '':
        cmd += ' -u ' + db + ' ' #+ db.replace('/', '') + ' '
        #cmd += ' -u ' + db.replace('/', '') + ' '
    if column_num != '':
        #if ft != '':
        #    column_num = '1'
        cmd += " -c " + column_num + " "
    if navigation != "false":
        cmd += " -n "    
    if ft != '':
        ft = ft.replace('"', '')
        cmd += ' -f "' + ft.replace('[or]', '#or').replace('[and]', '#and').replace('[not]', '#not') + '"'
        if merger != 'false':
            cmd += ' -m '
    if merger == 'true':
        cmd += ' -m '
    if level != '':
        cmd += ' -l ' + level + ' '
    if engin != '':
        cmd += ' -e "' + engin + '" '
    elif enginType != '':
        cmd += " -e 'd:" + enginType + "' "
    elif Config.disable_star_engin == False:
        cmd += " -e 'd:" + Config.recommend_engin_type + "' "
    if top != '':
        cmd += ' -t ' + top + ' '
    if desc == 'true':
        cmd += ' -d '
    if row != '':
        cmd += ' -r ' + row + ' '
    if style != '':
        cmd += ' -s ' + style + ' '
    if verify != '':
        cmd += ' -v ' + verify + ' '
    if alexa == 'true':
        cmd += ' -a '
    if width != '':
        cmd += ' -w ' + width + ' '
    if track != 'false':
        cmd += ' -q ' + track + ' '

    if nosearchbox == 'true':
        cmd += ' -x '

    if loadmore != '':
        cmd += ' -z true '
    if session.has_key('name'):
        cmd += ' -y ' + session['name'] + ' '

    if page != '':
        cmd += ' -o ' + page + ' '

    if extension != '':
        cmd += ' -j ' + extension + ' '

    #if crossrefQuery != '':
    cmd += ' -g "' + crossrefQuery.replace('"', '') + '" '


    

    return cmd.replace('?', '') 

def listDB():
    return genList(sorted(os.listdir(Config.default_db + '/')))

def listAllFile(db):
    folder = Config.default_db + '/' + db
    files = sorted(os.listdir(folder))
    html = ''
    html += '<head>'
    html += '<style type="text/css">a { font-weight:Normal;  text-decoration:none; } a:hover { text-decoration:underline; }</style>'
    html += '<script language="JavaScript" type="text/JavaScript">'
    #html += ''.join(open('web/jquery-3.1.1.min.js', 'rU').readlines())
    #html += 'function userlog(text, url, module, library, rid) {$.post("/userlog", {text : text , url : url, module : module, library : library, rid : rid}, function(data){});}'
    html += utils.loadFiles('web', '.js')
    html +='</script>'
    html += '</head>'
    #return genList(files, folder, db)
    name = ''
    image = ''
    if session.has_key('name'):
        name = session['name']
    if session.has_key('avatar_url'):
        image = session['avatar_url']
    image = ''
    if Config.default_library != '':
        name = Config.default_library
        if name.endswith('-library'):
            name = name[0 : name.rfind('-')]
        libary = utils.gen_libary(True, name, '')
    else:
        libary = utils.gen_libary(True, name, image)
    if len(files) > 37:
        if Config.center_content:
            html += '<body style="text-align:center;">'
        else:
            html += "<body>"
        html += libary + genTable(files, folder, db)
    else:
        html += "<body>"
        html += libary + genList(files, folder, db)
    html += '</body>'
    return html


def genTable(files, folder= '', db=''):
    html = ''
    if Config.center_content:
        html = '<table style="margin:0px auto">'
    else:
        html = '<table>'

    count = 0
    column_num = int(request.args.get('column', '3'));
    tds = ''
    #for f in sorted(files,  cmp=lambda x,y : cmp(len(x), len(y))):
    for f in sorted(files):
       count += 1
       if os.path.isfile(os.path.join(folder, f)):
           url = 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + f 
           url += '&nosearchbox=true'
           tds += '<td>' + utils.enhancedLink(url, f, module='file', library=db + f, newTab=False) + '</td>'
       else:
           if db != '':
               tds += '<td>' + utils.enhancedLink('http://' + Config.ip_adress + '/?db=' + db + f +  '/&key=?', f, module='file', library=db + f, newTab=False) + '</td>'
           else:
               tds += '<td>' + utils.enhancedLink('http://' + Config.ip_adress + '/?db=' + f +  '/&key=?', f, module='file', library=db + f, newTab=False) + '</td>'
       if count % column_num == 0:
           html += '<tr>' + tds + '</tr>'
           tds = ''
    if tds != '':
        html += '<tr>' + tds + '</tr>' 
    html += '</table>'
    return html

def genList(files, folder='', db=''):
    html = '<head><script>' + utils.loadFiles('web', '.js') + '</script></head>'
    html += '<body><ul style="margin:0; padding:0; list-sytle:none;">'
    count = 0
    for f in sorted(files):
        count += 1
        
        if os.path.isfile(os.path.join(folder, f)):
            url = 'http://' + Config.ip_adress + '/?db=' + db+  '&key=' + f
            html += '<li>' + utils.enhancedLink(url, f, module='file', library=db + f, newTab=False)  + '</li>'
        else:
            if db != '':
                url = 'http://' + Config.ip_adress + '/?db=' + db + f +  '/&key=?'
                html += '<li>' + utils.enhancedLink(url, f, module='file', library=db + f, newTab=False) + '</li>'
            else:
                url = 'http://' + Config.ip_adress + '/?db=' + f +  '/&key=?'
                html += '<li>' + utils.enhancedLink(url, f, module='file', library=f, newTab=False)  + '</li>'

    html += '</ul></body>'
    return html


@app.route('/login')
def login():
    redirect_uri = url_for('authorized', next=request.args.get('next') or
        request.referrer or None, _external=True)
    print(redirect_uri)
    if Config.igon_authorized:
        session['name'] = 'wowdd1'
        return redirect(url_for('library'))
    # More scopes http://developer.github.com/v3/oauth/#scopes
    params = {'redirect_uri': redirect_uri, 'scope': 'user:email'}
    print(github.get_authorize_url(**params))
    return redirect(github.get_authorize_url(**params))

# same path as on application settings page
@app.route('/github/callback')
def authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    # make a request for the access token credentials using code
    redirect_uri = url_for('authorized', _external=True)

    data = dict(code=request.args['code'],
        redirect_uri=redirect_uri,
        scope='user:email,public_repo')

    auth = github.get_auth_session(data=data)

    # the "me" response
    me = auth.get('user').json()
    print me
    #user = User.get_or_create(me['login'], me['name'])

    session['token'] = auth.access_token
    #session['user_id'] = user.id
    session['name'] = me['name']
    session['avatar_url'] = me['avatar_url']
    session['id'] = me['id']

    flash('Logged in as ' + me['name'])
    print me['name']
    return redirect(url_for('library'))

@app.route('/library', methods=['GET', 'POST'])
def library():
    if session.has_key('name') == False or session['name'] == None or session['name'] == '':
        return redirect(url_for('index'))
    library = session['name'] + "-library"
    if Config.default_library != '':
        library = Config.default_library
        if library.endswith('-library') == False:
            library += '-library'
    if os.path.exists('db/library/' + library) == False:
        f = open('db/library/' + library, 'a')
        f.write('none | ' + Config.start_library_title+ ' | ' + Config.start_library_url + '| \n')
        f.close()
    engin = 'star'
    if Config.recommend_engin_type != '':
        engin = Config.recommend_engin_type
    cmd = "./list.py -i db/library/" +  library + " -b 4 -u library/ -c 3  -n  -e 'd:" + engin + "'  -d  -w " + Config.default_width + " -s " + str(Config.css_style_type) + " -y " + session['name']
    print cmd
    return subprocess.check_output(cmd, shell=True)

if __name__ == '__main__':
    print '__main__'
    app.run(debug=True)


