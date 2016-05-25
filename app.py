#!/usr/bin/env python
# -*- coding: utf-8-*-  

import os
from flask import Flask
from flask import request
import subprocess
from extension_manager import ExtensionManager
app = Flask(__name__)




extensionManager = ExtensionManager()
@app.route('/', methods=['GET', 'POST'])
def index():
    print  request.args.get('column', '')
    key = request.args.get('key', '')
    if key == '':
        key = '?'

    db = request.args.get('db', '')
    if db == '':
        db = 'eecs/'   
    elif db == '?':
        return listDB()
 
    if key == '?' and request.args.get('filter', '') == '':
        return listAllFile(db)
    else:
        cmd = genCmd(db, key, 
                      request.args.get('column', '2'),
                      request.args.get('filter', ''),
                      request.args.get('style', ''),
                      request.args.get('desc', 'true'),
                      request.args.get('width', ''),
                      request.args.get('row', ''),
                      request.args.get('top', ''),
                      request.args.get('level', ''),
                      request.args.get('merger', 'false'),
                      request.args.get('border', ''),
                      request.args.get('engin', ''),
                      request.args.get('navigation', 'true'),
                      request.args.get('verify', ''),
                      request.args.get('alexa', ''))
        
        print '\ncmd  --->   '  + cmd + '   <---\n'
        html = subprocess.check_output(cmd, shell=True)
        return html

@app.route('/extensions', methods=['POST'])
def handleExtension():
    if request.args.get('verify', '') != '':
        form['fileName'] = request.args.get('verify', '')
    return extensionManager.doWork(request.form)

@app.route('/temp/<page>', methods=['GET', 'POST'])
def temp(page):
    print page
    f = open('temp/test.html', 'rU')
    data = f.read()
    print data
    f.close()
    return data

def genCmd(db, key, column_num, ft, style, desc, width, row, top, level, merger, border, engin, navigation, verify, alexa):
    if db.endswith('/') == False:
        db += '/'
    cmd = "./list.py -i db/" + db + key + " -b 4"
    if db != '':
        cmd += ' -u ' + db + ' ' #+ db.replace('/', '') + ' '
        #cmd += ' -u ' + db.replace('/', '') + ' '
    if column_num != '':
        cmd += " -c " + column_num + " "
    if navigation != "false":
        cmd += " -n "    
    if ft != '':
        ft = ft.replace('"', '')
        #cmd += ' -f ' + ft + ' '
        cmd += ' -f "' + ft.replace('-or-', '#or').replace('-and-', '#and').replace('-not-', '#not') + '" '
    if merger == 'true':
        cmd += ' -m '
    if level != '':
        cmd += ' -l ' + level + ' '
    if engin != '':
        cmd += ' -e "' + engin + '" '
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

    return cmd.replace('?', '') 

def listDB():
    return genList(os.listdir('db/'))

def listAllFile(db):
    folder = 'db/' + db + '/'
    files = os.listdir(folder)
    #return genList(files, folder, db)
    if len(files) > 40:
        return genTable(files, folder, db)
    else:
        return genList(files, folder, db)


def genTable(files, folder= '', db=''):
    html = '<table>'
    count = 0
    column_num = int(request.args.get('column', '3'));
    tds = ''
    for f in sorted(files,  cmp=lambda x,y : cmp(len(x), len(y))):
       count += 1
       if os.path.isfile(os.path.join(folder, f)):
           tds += '<td><a href="http://localhost:5000/?db=' + db+  '&key=' + f + '">' + str(count) + '. ' + f + '<a></td>'
       else:
           if db != '':
               tds += '<td><a href="http://localhost:5000/?db=' + db + f +  '/&key=?">' + str(count) + '. ' + f + '/</a></td>'
           else:
               tds += '<td><a href="http://localhost:5000/?db=' + f +  '/&key=?">' + str(count) + '. ' + f + '/</a></td>'
       if count % column_num == 0:
           html += '<tr>' + tds + '</tr>'
           tds = ''
    if tds != '':
        html += '<tr>' + tds + '</tr>' 
    html += '</table>'
    return html

def genList(files, folder='', db=''):
    html = '<ol>'
    for f in sorted(files):
        if os.path.isfile(os.path.join(folder, f)):
            html += '<li><a href="http://localhost:5000/?db=' + db+  '&key=' + f + '">' + f + '<a></li>'
        else:
            if db != '':
                html += '<li><a href="http://localhost:5000/?db=' + db + f +  '/&key=?">' + f + '/</a></li>'
            else:
                html += '<li><a href="http://localhost:5000/?db=' + f +  '/&key=?">' + f + '/</a></li>'

    html += '<ol>'
    return html


if __name__ == '__main__':
    app.run(debug=True)


