#!/usr/bin/env python

import os
import json
import sys

class ExtensionManager:

    def loadExtension(self, name):
        base_path = os.getcwd() + '/extensions'
        print '--->' + base_path
        dirList = os.listdir(base_path)
        print dirList
        for f in dirList:
            print f
            if os.path.isdir(base_path + '/'+ f):
                for f2 in os.listdir(base_path + '/'+ f):
                    if f2 == 'manifest':
                        jobj = json.loads(open(base_path + '/'+ f + '/' + f2, 'rU').read())
                        if jobj['name']  == name:
                            return self.newExtension('extensions.' + f + '.' + jobj['module'], jobj['class'])

    def newExtension(self, module, cls):
       print module
       __import__(module)
       m = sys.modules[module]
       print m
       for str in dir(m):
           if str == cls:
               att = getattr(m, str)
               return att()

       return None

    def doWork(self, form):
        extension = self.loadExtension(form['name'])
        if extension != None:
            print 'ok'
            return extension.excute(form) #'cs-stanford2016', form['rID'], form['rTitle'], form['divID'])
        else:
            print 'error'
            return 'xxx'

    '''

    def reflectionCall(self, module, cls, method, cls_arg=None, method_arg=None):
        __import__(module)
        m = sys.modules[module]
        for str in dir(m):
            if str == cls:
                att=getattr(m,str)
                obj = None
                if cls_arg != None:
                    obj = att(cls_arg)
                else:
                    obj = att()
                for att2 in dir(att):
                    if att2 == method:
                        func = getattr(obj, att2)
                        if method_arg != None:
                            return apply(func, method_arg)
                        else:
                            return apply(func)
    '''

#test = ExtensionManager()
#test.doWork('reference', '123', '34', '56')
