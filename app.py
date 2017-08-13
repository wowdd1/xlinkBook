#!/usr/bin/env python
# -*- coding: utf-8-*-  

import os
from flask import Flask
from flask import request
import subprocess
import json
from extension_manager import ExtensionManager
from utils import Utils
from config import Config
import requests
import datetime

from flask import (Flask, flash, request, redirect,
    render_template, url_for, session)
from rauth.service import OAuth2Service
from record import Tag, Record
from knowledgegraph import KnowledgeGraph

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

extensionManager = ExtensionManager()
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
                      request.args.get('page', ''))
        
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
                      args_history['page'],)

    print '\ncmd  --->   '  + cmd + '   <---\n'
    html = subprocess.check_output(cmd, shell=True)
    return html


@app.route('/navigate', methods=['POST'])
def handleNavigate():
    #print request.form
    if request.form['rID'] == "":
        return ""
    return extensionManager.doWork(request.form)

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
    #print request.form
    data = request.form['data'].strip()
    fileName = request.form['fileName'].strip()
    enginArgs = request.form['enginArgs'].strip()
    crossrefPath = request.form['crossrefPath'].strip()
    newTab = request.form['newTab'].strip()
    resourceType = request.form['resourceType'].strip()
    originFilename = request.form['originFilename'].strip()
    lastRID = request.form['rID'].strip()
    kgraph = request.form['kgraph'].strip()

    rID = ''
    for d in data.strip().split(' '):
        rID += d[0 : 1].lower()

    targetPath = ' '.join(Config.exclusive_crossref_path)
    if crossrefPath != '':
        targetPath = ' ' +  crossrefPath
    desc = 'engintype:' + data + ' '
    desc += 'localdb:' + data
    desc += ' ' + kg.getCrossref(data, targetPath)
    if resourceType != '':
        desc += ' category:' + resourceType 

    kg_cache = kg.getKnowledgeGraphCache(data)
    if kg_cache != '':
        desc += ' ' + kg_cache
    elif kgraph == 'true':
        desc += ' description:' + resourceType + '#' + originFilename + '#' + lastRID
    url = ''
    if data.startswith('http'):
        url = data
    url = doExclusive(rID, data, url, desc)
    
    if enginArgs.find(':') != -1:
        enginType = enginArgs[enginArgs.find(':') + 1 :]
        if enginType != 'star':
            url += '&enginType=' + enginType
    if crossrefPath != '':
        url += '&crossrefPath=' + crossrefPath

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
        print urls
        return urls

    return ''

@app.route('/tolist', methods=['POST'])
def handleToList():
    rID = request.form['rID'].strip()
    fileName = request.form['originFilename'].strip()
    resourceType = request.form['resourceType'].strip()

    print request.form

    record = utils.getRecord(rID, path=fileName)
    records = []
    accountTag = utils.isAccountTag(resourceType, tag.tag_list_account)

    if record != None and record.get_id().strip() == rID:
        args = { 'tag' : resourceType + ':' } 
        #print '&&&' + record.line
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)
        url = ''
        for item in ret.split(','):
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
            elif Config.smart_engin_for_tag.has_key(resourceType):
                url = utils.toQueryUrl(utils.getEnginUrl(Config.smart_engin_for_tag[resourceType][0]), item.strip())
            else:
                url = utils.toQueryUrl(utils.getEnginUrl('glucky'), item.strip() + ' ' + resourceType)

            #print url
            records.append(Record(' | ' + item.strip() + ' | ' + url + ' | '))
    if len(records) > 0:
        return utils.output2Disk(records, 'tag', rID + '-' + resourceType, ignoreUrl=False)
    return ''

def toRecordFormat(data):
    if data.find('|') != -1:
        return data + '\n'
    else:
        rID = 'custom-'
        for item in data.split(' '):
            rID += item[0 : 1]
        return rID + ' | ' + data + ' | | \n'

@app.route('/exec', methods=['POST'])
def handleExec():
    command = request.form['command']
    fileName = request.form['fileName']
    print command + ' ' + fileName
    output = ''
    if command == 'open':
        cmd = 'open "' + fileName + '"'
        app = ''
        for k, v in Config.application_dict.items():
            if fileName.lower().strip().endswith(k):
                app = v
                break
        if app == '':
            app = Config.application_dict['*']
        if os.path.exists(app):
            cmd = app.replace(' ', '\ ') + ' "' + fileName + '"'
            print cmd
            output = subprocess.check_output(cmd, shell=True)
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

@app.route('/queryUrl', methods=['POST'])
def handleQueryUrl():
    result = ''
    #print '<<===handleQueryUrl:'
    #print request.form
    if request.form.has_key('isTag') and (request.form['isTag'] == True or request.form['isTag'] == 'True' or request.form['isTag'] == 'true'):
        record = utils.getRecord(request.form['rID'], path=request.form['fileName'])
        if record != None and record.get_id().strip() == request.form['rID']:
            args = { 'tag' : request.form['searchText'].strip() + ':' } 
            ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, args)
            print ret
            if ret != None:
                if ret.find(', ') != -1:
                    ret = ret.split(',')
                else:
                    ret = [ret]

                if request.form.has_key('type') and request.form['type'] == 'dialog':
                    resultDict = utils.clientQueryEnginUrl2(request.form['searchText'], resourceType=request.form['resourceType'])      
                    count = 0
                    #print  resultDict
                    result = ''
                    for k, v in resultDict.items():
                        count += 1

                        #if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                        #    v = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
                        script = ''
                        #if k == 'glucky':
                        #    print 'ccc: ' + utils.getValueOrText(q.strip(), returnType='value')
                        for q in ret:
                            script += "window.open('" + utils.toQueryUrl(utils.getEnginUrl(k.strip()), q.strip()).strip().replace('#', '') + "');"
                        result += '<a target="_blank" href="javascript:void(0);" onclick="' + script + '" style="color:#999966;font-size:10pt;">' + k + '</a>'+ '&nbsp;'
                        if count % 5 == 0 and count > 0 and len(resultDict) != 5:
                            result += '<br>'
                        if count >= Config.recommend_engin_num_dialog:
                            break
                    if len(Config.command_for_tag_dialog) > 0:
                        library = os.getcwd() + '/db/library/' + Config.default_library;
                        result += '<br>' + dialogCommand(library, request.form['searchText'], request.form['resourceType'], request.form['fileName'], request.form['rID'], tagCommand=True)
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
                            for q in ret:
                                url = tag.tag_list_account[request.form['searchText'] + ':'].replace('%s', q.strip())
                                urls += url + ' '
                        else:
                            for q in ret:
                                url = utils.toQueryUrl(utils.getEnginUrl('glucky'), q)
                                urls +=  url + ' '
                        print urls + '<<<<'
                        return urls
            else:
                return ''
        else:
            return ''

    #print request.form
    if request.form.has_key('type'):
        if request.form['type'] == 'dialog':
            #print request.form
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
                    script = "exclusive('exclusive', '" + request.form['searchText'] + "', '" + item + "', false, '', '" + request.form['fileName'] + "', '" + request.form['rID'] + "', engin_args, false);"

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
                #print request.form
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
                resultDict = utils.clientQueryEnginUrl2(request.form['searchText'], resourceType=request.form['resourceType'])
                
                count = 0
                #print  resultDict
                value = utils.getValueOrText(request.form['originText'], returnType='value')

                searchHtml = ''
                commandHtml = ''
                infoHtml = ''
                infoLen = 0
                infoBR = False

                for k, v in resultDict.items():
                    count += 1

                    if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                        v = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
                            
                    #if k == 'glucky':
                    #    print 'ccc1111: ' + request.form['searchText']
                    #    print 'ccc1111: ' + utils.getValueOrText(request.form['searchText'], returnType='value')
                    searchHtml += utils.enhancedLink(v, utils.formatEnginTitle(k), searchText=request.form['searchText'], style="color:#999966; font-size: 10pt;", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType']) + '&nbsp;'
                    if count % 5 == 0 and count > 0 and len(resultDict) != 5:
                        searchHtml += '<br>'
                    if count >= Config.recommend_engin_num_dialog:
                        break                    
                #print result
                if len(Config.command_for_dialog) > 0:
                    library = os.getcwd() + '/db/library/' + Config.default_library;
                    commandHtml += '<br>' + dialogCommand(library, request.form['searchText'], request.form['resourceType'], request.form['fileName'], request.form['rID'])
                #print request.form['originText']
                if utils.getValueOrTextCheck(request.form['originText']):
                    #print utils.getValueOrText(request.form['originText'], returnType='value')
                    valueList = [value]
                    text = utils.getValueOrText(request.form['searchText'], returnType='text')
                    if value.find('+') != -1:
                        valueList = value.split('+')
                    infoHtml += '<br>'
                    count = 0
                    for v in valueList:
                        count += 1
                        if utils.isUrlFormat(v):
                            if v.startswith('http') == False:
                                v = 'http://' + v
                            infoHtml += utils.enhancedLink(v, text, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                            infoLen += len(text)
                        elif utils.getValueOrTextCheck(v):
                            subValue = utils.getValueOrText(v, returnType='value')
                            subText = utils.getValueOrText(v, returnType='text')
                            if utils.isUrlFormat(subValue):
                                if subValue.startswith('http') == False:
                                    subValue = 'http://' + subValue
                                if Config.website_icons.has_key(subText.strip().lower()):
                                    iconHtml = utils.getIconHtml(subText)
                                    infoHtml += utils.enhancedLink(subValue, text, showText=iconHtml, module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                                    infoLen += 1

                                else:
                                    infoHtml += utils.enhancedLink(subValue, subText, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                                    infoLen += len(subText)
                            else:
                                if utils.isAccountTag(subText, tag.tag_list_account):
                                    url = tag.tag_list_account[subText + ':']
                                    if url.find('%s') != -1:
                                        url = url.replace('%s', subValue)
                                    else:
                                        url = url + subValue
                                    if Config.website_icons.has_key(subText.strip().lower()):
                                        iconHtml = utils.getIconHtml(subText)
                                        infoHtml += utils.enhancedLink(url, text, showText=iconHtml, module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                                        infoLen += 1

                                    else:
                                        infoHtml += utils.enhancedLink(url, subText, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                                        infoLen += len(subText)
                                else:
                                    infoHtml += utils.enhancedLink(utils.bestMatchEnginUrl(subValue, resourceType=request.form['resourceType']), subText, style="color:#339944; font-size: 9pt", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType'])
                                    infoLen += len(subText)


                        else:
                            infoHtml += '<font style="color:#002244; font-size: 9pt">' + v + '</font>'
                            infoLen += len(v)

                        if len(valueList) > 1 and count != len(valueList):
                            infoHtml += '&nbsp;'
                            infoLen += 1
                        if infoLen - 34 > 0:
                            infoHtml += '<br>'
                            infoBR = True
                            infoLen -= 34

                if infoBR:
                    result = infoHtml + commandHtml 
                else:
                    result = searchHtml + commandHtml + infoHtml

                result = str(count) + '#' + result
    else:
        resultDict = utils.clientQueryEnginUrl(request.form['url'], request.form['searchText'], request.form['resourceType'], request.form['module'])
        for k, v in resultDict.items():
            if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                resultDict[k] = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
        result = ' '.join(resultDict.values())

    return result

def dialogCommand(fileName, text, resourceType, originFilename, rID, tagCommand=False):
    result = ''
    if tagCommand:
        for command in Config.command_for_tag_dialog:
            if command == 'tolist':
                script = "tolist('" + rID + "', '" + resourceType + "','" + originFilename + "');"
                result += utils.enhancedLink('', '#tolist', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
    else:
        for command in Config.command_for_dialog:
            if command == 'add2library':
                script = "addRecord('" + fileName + "', '" + text + "');"
                result += utils.enhancedLink('', '#add2' + fileName[fileName.rfind('/') + 1 :].replace('-library', ''), script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
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

@app.route('/userlog', methods=['POST'])
def handleUserLog():
    dt = str(datetime.datetime.now())
    print 'handleUserLog--->  ' + dt[0 : dt.rfind('.')] + '  <---'
    print '     linktext: ' + request.form['text'].replace('%20', ' ')
    print '     searchText: ' + request.form['searchText'].replace('%20', ' ')
    print '     url: ' + request.form['url']
    print '     module: ' + request.form['module']
    library = request.form['library']
    if library.find('db/') != -1:
        library = library[library.find('db/') :]
    print '     library: ' + library
    print '     rid: ' + request.form['rid']
    print '     resourceType: ' + request.form['resourceType']
    print '     user: ' + request.form['user']
    print '     os: ' + request.form['os']
    print '     browser: ' + request.form['browser']
    print '     mac: ' + request.form['mac']
    print '     ip: ' + request.form['ip']
    print '     from: ' + request.form['from']

    module = request.form['module'].strip()
    if library != '' and request.form['rid'].strip() != '' and request.form['url'].strip() != '' and igonLog(module) == False:
        historyFile = 'extensions/history/data/' + library[library.rfind('/') + 1 :] + '-history'
        title = utils.getValueOrText(request.form['searchText'].replace('|', ''), returnType='text')

        if request.form['resourceType'] != '' and utils.isAccountTag(request.form['resourceType'].strip(), tag.tag_list_account) == False and utils.getValueOrTextCheck(request.form['searchText']):
            title += ' - ' + request.form['resourceType']
        line = request.form['rid'] + ' | ' + title + ' | ' + request.form['url'] + ' | '
        cmd = 'echo "' + line + '" >> ' + historyFile
        print cmd
        output = subprocess.check_output(cmd, shell=True)
        #utils.slack_message(request.form['url'], 'general')

    return ''

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

    if request.form['rID'] == "":
        return ""
    return extensionManager.doWork(request.form)

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
    return utils.gen_plugin_content(request.form['title'])

    

@app.route('/web_content/chrome/<page>', methods=['GET', 'POST'])
def web(page):
    print page
    f = open('web_content/chrome/output.html', 'rU')

    data = f.read()
    #print data
    f.close()
    return data

def genCmd(db, key, column_num, ft, style, desc, width, row, top, level, merger, border, engin, enginType, navigation, verify, alexa, track, loadmore, nosearchbox, page):
    print 'track:' + track
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
    html += ''.join(open('web/jquery-3.1.1.min.js', 'rU').readlines())
    html += 'function userlog(text, url, module, library, rid) {$.post("/userlog", {text : text , url : url, module : module, library : library, rid : rid}, function(data){});}'
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
           tds += '<td>' + utils.enhancedLink('http://' + Config.ip_adress + '/?db=' + db + '&key=' + f, f, module='file', library=db + f, newTab=False) + '</td>'
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
    html = ''
    html += '<ul style="margin:0; padding:0; list-sytle:none;">'
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

    html += '</ul>'
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
    if session['name'] == None or session['name'] == '':
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


