#!/usr/bin/env python

import os
import json
import sys
import datetime  

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

    def doWork(self, form):
        self.loadExtensions()
        check = form['check']

        if check == 'true':
            if form['name'] == "*":
                rID = form['rID'].encode('utf-8')
                if self.extensions_check_cache.has_key(rID):
                    print 'return cache for ' + rID
                    return self.extensions_check_cache[rID]
                else:
                    self.extensions_check_cache[rID] = self.checkAll(form)
                    return self.extensions_check_cache[rID]
            else:
                extension = self.loadExtension(form['name'])
                if extension != None:
                    if extension.check(form):
                        return form['name']
                    else:
                        return 'false'
                else:
                    print 'error'
                    return ''
        else:
            extension = self.loadExtension(form['name'])
            return extension.excute(form) #'cs-stanford2016', form['rID'], form['rTitle'], form['divID'])

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
        
