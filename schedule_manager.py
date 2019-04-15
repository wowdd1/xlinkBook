#!/usr/bin/env python

import os
import json
import sys
import datetime  
from record import Record
from utils import Utils
from config import Config


class ScheduleManager:
    
    def __init__(self):
        self.utils = Utils()
        self.schedulingHistory = {}
        self.jobResultDict = {}

        
    def runJob(self, classPath, param):
        #obj = r.get_class('extensions.code.code.Code')
        result = ''
        obj = param['record'].get_class(classPath)
        if obj != None:
            result = obj.excute(param)

        return result

    def schedulingJob(self, descList, args, parentJob, isRecursion=False):
        result = ''
        if len(descList) > 0:
            matchedText =  descList[0][0]
            desc = descList[0][1]
            crossref = descList[0][3]
            parentRecord = descList[0][5]
            path = crossref
            if path.find('#') != -1:
                path = path[0 : path.find('#')]

            line = ' | ' + matchedText + ' | | ' + desc
            record = Record(line)
            if path != '':
                parentRecord.set_path(path)
            if isRecursion == False:
                print 'scheduling:' + matchedText

            if desc.find('class:') != -1:
                classes = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'class:'})

                for acls in classes.split(','):
                    acls = acls.strip()
                    text = acls
                    value = acls
                    if self.utils.getValueOrTextCheck(acls):
                        text = self.utils.getValueOrText(acls, returnType='text')
                        value = self.utils.getValueOrText(acls, returnType='value')

                    parentJobResult = 0
                    
                    if self.jobResultDict.has_key(parentJob):
                        parentJobResult = self.jobResultDict[parentJob]['jobResult']
                        
                    param = {'record' : record, 'parentRecord' : parentRecord, 'from' : matchedText, 'class' : value[value.rfind('.') + 1 :], 'args' : args, 'parentJobResult' : parentJobResult, 'parentJob' : parentJob}
                    #value = value[0 : value.rfind('.')] + '.Main'
                    resultDict = self.runJob(value, param)

                    

                    jobTitle = resultDict['jobTitle']
                    if resultDict.has_key('jobEnd'):

                        if self.jobResultDict.has_key(matchedText):
                            self.jobResultDict[matchedText]['jobResult'] = self.jobResultDict[matchedText]['jobResult'] + resultDict['jobResult']

                            resultDict = self.jobResultDict[matchedText]
                         
                        else:
                           self.jobResultDict[matchedText] = resultDict 
                    else: 
                        self.jobResultDict[matchedText] = resultDict

                    result += resultDict['result']
                    result += '<br>'
                    result += 'jobResult:' + str(resultDict['jobResult'])
                    result += '<br>'
            else:
                return ''


            if desc.find('searchin:') != -1:
                
                searchin = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'searchin:'})

                for si in searchin.split(','):
                    si = si.strip()
                    if si.startswith('>'):
                        #if self.schedulingHistory.has_key(si.lower()):
                        #        continue
                        #else:
                        #    self.schedulingHistory[si.lower()] = ''

                        print 'scheduling:' + si
                        descList = self.utils.processCommand(si, '', style='', nojs=False, noFilterBox=True, unfoldSearchin=False, returnMatchedDesc=True)
                        result += self.schedulingJob(descList, args, matchedText, isRecursion=True)

        return result

    def scheduling(self, command):

        print 'scheduling'
        self.schedulingHistory = {}
        self.jobResultDict = {}
        args = command[command.find('/:run') + 5 :].strip()
        command = command[0 : command.find('/:run')]
        result = ''
        self.schedulingHistory[command.lower()] = ''

        descList = self.utils.processCommand(command, '', style='', nojs=False, noFilterBox=True, unfoldSearchin=False, returnMatchedDesc=True)

        result = self.schedulingJob(descList, args, '')


        return result
