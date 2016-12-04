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

tag = Tag()
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
    data = request.form['data'].strip()
    fileName = request.form['fileName'].strip()
    rID = ''
    for d in data.strip().split(' '):
        rID += d[0 : 1].lower()
    record = Record('custom-exclusive-' + rID + ' | '+ data + ' | | ')
    return utils.output2Disk([record], 'main', 'exclusive')

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
        chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome):
            cmd = chrome.replace(' ', '\ ') + ' "' + fileName + '"'
        print cmd
        output = subprocess.check_output(cmd, shell=True)
    elif command == 'edit':
        cmd = 'open "' + fileName + '"'
        sublime = '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text'
        if os.path.exists(sublime):
            cmd = sublime.replace(' ', '\ ') + ' "' + fileName.strip() + '"'
        print cmd
        output = subprocess.check_output(cmd, shell=True)

    return output

@app.route('/queryStarEngin', methods=['POST'])
def handlerQueryStarEngin():
    rID = request.form['rID']
    rTitle = request.form['rTitle']
    targetid = request.form['targetid']
    print 'handlerQueryStarEngin--> rID:' + rID + ' rTitle:' + rTitle + ' taggetid:' + targetid
    return ''

@app.route('/queryUrl', methods=['POST'])
def handleQueryUrl():
    result = ''
    if request.form.has_key('type'):
        if request.form['type'] == 'dialog':
            print request.form
            resultDict = utils.clientQueryEnginUrl2(request.form['searchText'], resourceType=request.form['resourceType'])
            
            count = 0
            for k, v in resultDict.items():
                count += 1
                '''
                script = ''
                if request.form['aid'] != '':
                    script = "chanageLinkColorByID('" + request.form['aid'] + "','" + Config.background_after_click + "', '');"
                    print '------\n'
                    print script
                '''

                if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                    v = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
                    print k + '--->' + v
                        
                result += utils.enhancedLink(v, utils.formatEnginTitle(k), searchText=request.form['searchText'], style="color:#999966; font-size: 10pt;", module='dialog', library=request.form['fileName'], rid=request.form['rID'], resourceType=request.form['resourceType']) + '&nbsp;'
                if count % 5 == 0 and count > 0:
                    result += '<br>'
            if len(Config.command_for_dialog) > 0:
                library = os.getcwd() + '/db/library/' + Config.default_library;
                result += '<br>' + dialogCommand(library, request.form['searchText'])
            result = str(count) + '#' + result
    else:
        resultDict = utils.clientQueryEnginUrl(request.form['url'], request.form['searchText'], request.form['resourceType'], request.form['module'])
        for k, v in resultDict.items():
            if utils.accountMode(tag.tag_list_account, tag.tag_list_account_mode, k, request.form['resourceType']):
                resultDict[k] = utils.toQueryUrl(utils.getEnginUrl('glucky'), request.form['searchText'] + '%20' + k)
        result = ' '.join(resultDict.values())
    #print 'handleQueryUrl: ' + result
    return result

def dialogCommand(fileName, text):
    result = ''
    for command in Config.command_for_dialog:
        if command == 'add2library':
            script = "addRecord('" + fileName + "', '" + text + "');"
            result += utils.enhancedLink('', '#add2' + fileName[fileName.rfind('/') + 1 :].replace('-library', ''), script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
        elif command == 'exclusive':
            script = "exclusive('" + fileName + "', '" + text + "');"
            result += utils.enhancedLink('', '#exclusive', script=script, style="color: rgb(136, 136, 136); font-size: 10pt;") + '&nbsp;'
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
        #requests.get('https://api.thumbalizr.com/?url=' + url + '&width=800')
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
    if db.endswith('/') == False:
        db += '/'
    cmd = "./list.py -i db/" + db + key + " -b 4"
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
        cmd += " -e 'd:star' "
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
    if track == 'true':
        Config.track_mode = True
    else:
        Config.track_mode = False
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
    return genList(sorted(os.listdir('db/')))

def listAllFile(db):
    folder = 'db/' + db
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


