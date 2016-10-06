#!/usr/bin/env python

import sys, os
from extensions.bas_extension import BaseExtension
import subprocess

class Script(BaseExtension):

    def __init__(self):
        BaseExtension.__init__(self)

    def mapToScript(self, fileName):
        fileName = fileName[fileName.rfind('/') + 1 : ]
        
        return fileName + '-script'

    def getScriptName(self, fileName):
        return 'extensions/script/code/' + self.mapToScript(fileName)

    def excuteScript(self, fileName, rID):
        scriptName = self.getScriptName(fileName)
        cmd = './' + scriptName + ' -i "' + rID + '" -f "' + fileName[fileName.find('db') :] + '"'
        if os.path.exists(scriptName):
            print 'excuteScript ' + cmd
            data = subprocess.check_output(cmd, shell=True)

            return data

        return 'no script found'

    def excute(self, form_dict):

        fileName = form_dict['fileName'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')

        return self.excuteScript(fileName, rID)


    def check(self, form_dict):
        fileName = form_dict['fileName'].encode('utf8')
        print self.getScriptName(fileName)
        return os.path.exists(self.getScriptName(fileName))
