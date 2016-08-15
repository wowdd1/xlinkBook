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

from flask import (Flask, flash, request, redirect,
    render_template, url_for, session)
from rauth.service import OAuth2Service

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
        args_history['row'] = request.args.get('row', '20')
        args_history['top'] = request.args.get('top', '')
        args_history['level'] = request.args.get('level', '')
        args_history['merger'] = request.args.get('merger', '')
        args_history['border'] = request.args.get('border', '')
        args_history['engin'] = request.args.get('engin', '')
        args_history['navigation'] = request.args.get('navigation', 'true')
        args_history['verify'] = request.args.get('verify', '')
        args_history['alexa'] = request.args.get('alexa', '')
        args_history['track'] = request.args.get('track', 'false')
        args_history['nosearchbox'] = request.args.get('nosearchbox', 'false')
        cmd = genCmd(db, key, 
                      request.args.get('column', Config.column_num),
                      request.args.get('filter', ''),
                      request.args.get('style', str(Config.css_style_type)),
                      request.args.get('desc', 'true'),
                      request.args.get('width', ''),
                      request.args.get('row', '20'),
                      request.args.get('top', ''),
                      request.args.get('level', ''),
                      request.args.get('merger', ''),
                      request.args.get('border', ''),
                      request.args.get('engin', ''),
                      request.args.get('navigation', 'true'),
                      request.args.get('verify', ''),
                      request.args.get('alexa', ''),
                      request.args.get('track', 'false'), '', request.args.get('nosearchbox', 'false'))
        
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
                      args_history['navigation'],
                      args_history['verify'],
                      args_history['alexa'],
                      args_history['track'], 'true', args_history['nosearchbox'])

    print '\ncmd  --->   '  + cmd + '   <---\n'
    html = subprocess.check_output(cmd, shell=True)
    return html


@app.route('/navigate', methods=['POST'])
def handleNavigate():
    if request.form['rID'] == "":
        return ""
    return extensionManager.doWork(request.form)

@app.route('/extensions', methods=['POST'])
def handleExtension():
    if request.args.get('verify', '') != '':
        request.form['fileName'] = request.args.get('verify', '')
    print request.form
    if request.form['rID'] == "":
        return ""
    return extensionManager.doWork(request.form)

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

def genCmd(db, key, column_num, ft, style, desc, width, row, top, level, merger, border, engin, navigation, verify, alexa, track, loadmore, nosearchbox):
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
        cmd += ' -f "' + ft.replace('-or-', '#or').replace('-and-', '#and').replace('-not-', '#not') + '"'
        if merger != 'false':
            cmd += ' -m '
    if merger == 'true':
        cmd += ' -m '
    if level != '':
        cmd += ' -l ' + level + ' '
    if engin != '':
        cmd += ' -e "' + engin + '" '
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



    return cmd.replace('?', '') 

def listDB():
    return genList(os.listdir('db/'))

def listAllFile(db):
    folder = 'db/' + db
    files = os.listdir(folder)
    html = ''
    html += '<head>'
    html += '<style type="text/css">a { font-weight:Normal;  text-decoration:none; } a:hover { text-decoration:underline; }</style>'
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
    for f in sorted(files,  cmp=lambda x,y : cmp(len(x), len(y))):
       count += 1
       if os.path.isfile(os.path.join(folder, f)):
           tds += '<td><a href="http://' + Config.ip_adress + '/?db=' + db+  '&key=' + f + '">' + f + '<a></td>'
       else:
           if db != '':
               tds += '<td><a href="http://' + Config.ip_adress + '/?db=' + db + f +  '/&key=?">' + f + '/</a></td>'
           else:
               tds += '<td><a href="http://' + Config.ip_adress + '/?db=' + f +  '/&key=?">' + f + '/</a></td>'
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
            html += '<li><a href="http://' + Config.ip_adress + '/?db=' + db+  '&key=' + f + '">' + f + '<a></li>'
        else:
            if db != '':
                html += '<li><a href="http://' + Config.ip_adress + '/?db=' + db + f +  '/&key=?">' + f + '/</a></li>'
            else:
                html += '<li><a href="http://' + Config.ip_adress + '/?db=' + f +  '/&key=?">' + f + '/</a></li>'

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
        f.write('none | no record, add some! | | \n')
        f.close()
    cmd = "./list.py -i db/library/" +  library + " -b 4 -u library/ -c 3  -n  -e 'd:star'  -d  -r 20 -w 77 -s 6 -y " + session['name']
    print cmd
    return subprocess.check_output(cmd, shell=True)

if __name__ == '__main__':
    print '__main__'
    app.run(debug=True)


