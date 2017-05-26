#!/bin/env python

import subprocess
from webservice.base_webservice import BaseWebservice
from record import Record
import os
from utils import Utils

class KnowledgeGraph(object):

  kg_cache = {}
  """docstring for KnowageGraph"""
  def __init__(self):
    super(KnowledgeGraph, self).__init__()
    self.webservice = BaseWebservice()
    self.utils = Utils()

  
  def getKnowledgeGraphCache(self, keyword):
    if self.kg_cache.has_key(keyword):
        return self.kg_cache[keyword]
    else:
        return ''
        
  def getKnowledgeGraph(self, keyword, resourceType, path, rID, fileName):
      if self.kg_cache.has_key(keyword):
          return self.kg_cache[keyword]
      knowledgeGraph = ''
      #crossref = self.getCrossref(keyword, path)

      #if crossref != '':
      #    knowledgeGraph += crossref + ' '

      print rID + ' ' + fileName
      record = Record('')
      if os.path.exists(fileName) and rID != '':
          record = self.utils.getRecord(rID, path=fileName)
      if record != None and record.get_id().strip() == rID:
          for tag in ['instructors', 'keyword']:
              result = self.webservice.callWebservice(tag, record, keyword, resourceType)
              #print instructors
              if result != None and len(result) > 0:
                  knowledgeGraph += tag +':' + ', '.join(result).strip() + ' '
      self.kg_cache[keyword] = knowledgeGraph
      print knowledgeGraph
      return knowledgeGraph
   
  def getCrossref(self, keyword, path):
      cmd = 'grep -riE "' + keyword + '" ' + path
      print cmd
      output = ''
      try:
          output = subprocess.check_output(cmd, shell=True)
      except Exception as e:
          return ''
      adict = {}
      titleDict = {}
      for line in output.split('\n'):
          fileName = line[0 : line.find(':')].strip().replace('//', '/')
          firstIndex = line.find('|')
          rID = line[line.find(':') + 1 : firstIndex].strip().replace(' ', '%20')
          title = line[firstIndex + 1 : line.find('|', firstIndex + 1)].strip()
          if title != '':
              if title.find(',') != -1:
                  title = title.replace(',', '')
              if title.find('+') != -1:
                  title = title[0 : title.find('+')]
              if title.find('#') != -1:
                  title = title[0 : title.find('#')]
              if titleDict.has_key(title):
                  continue
              if adict.has_key(fileName):
                  adict[fileName].append(title)
              else:
                  adict[fileName] = [title]
              titleDict[title] = title
      result = ''
      print '---getCrossref---'
      for k, v in adict.items():
          #print k + ' #' + '#'.join(v)
          prefix = ''
          if k.startswith('db/'):
              prefix = k[3:]
          ft = '+'.join(v).strip()
          if ft.endswith('+'):
              ft = ft[0 : len(ft) - 2]
          result += prefix + '#' + ft
          if k != adict.items()[len(adict) - 1][0]:
              result += ', '

      print result
      if result != '':
          result = 'crossref:' + result
      return result




