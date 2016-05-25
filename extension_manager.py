#!/usr/bin/env python

import os
import json
import sys

class ExtensionManager:
    
    extensions = {}

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
                return self.checkAll(form)
            else:
                extension = self.loadExtension(form['name'])
                if extension != None:
                    if extension.check(form):
                        return 'true'
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
            if self.loadExtension(k).check(form):
                result += k + " "
        print result
        return result.strip()
        
