#!/usr/bin/env python

import os
import json
import sys
import datetime  
from record import Record
from record import LibraryRecord
from utils import Utils
from config import Config


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

    def loadExtension(self, name):
        if len(self.extensions) == 0:
            self.loadExtensions()
        print 'load ' + name + ' module'
        for k, manifest in self.extensions.items():
            jobj = json.loads(open(manifest, 'rU').read())
            if jobj['name']  == name:
                return self.newExtension('extensions.' + name + '.' + jobj['module'], jobj['class'])

    def newExtension(self, module, cls):
       print module
       __import__(module)
       m = sys.modules[module]
      # print m
       for str in dir(m):
           if str == cls:
               att = getattr(m, str)
               return att()

       return None

    def findRecordInLib(self, rID, fileName):
        utils = Utils()
	while True:
            r = utils.getRecord(rID, path=fileName, use_cache=False)
	    if r.get_id().strip() != '':
		return r
	    else:
		if rID.find('-') != -1:
		    rID = rID[0 : rID.rfind('-')]
		else:
		    return None


    def doWork(self, form_dict):
        form = form_dict.copy()
        self.loadExtensions()
        check = form['check']
        rID = form['rID'].encode('utf-8')
        fileName = form['fileName'].encode('utf-8')
        if fileName.endswith('library'):
            r = self.findRecordInLib(rID, fileName)
            if r != None and r.get_id().strip() != '':
                lr = LibraryRecord(r.line)
                if lr.get_path() != None and lr.get_path().strip() != '':
                    print lr.get_path()
                    form['fileName'] = os.getcwd() + '/' + lr.get_path().strip()
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
            return extension.excute(form) #'cs-stanford2016', form['rID'], form['rTitle'], form['divID'])
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
            starttime = datetime.datetime.now().microsecond
            if self.loadExtension(k).check(form):
                result += k + " "
            endtime = datetime.datetime.now().microsecond
            print k + " check cost --> " + str((endtime - starttime) / 1000.0) + "ms"
        print result
        return result.strip()
        
