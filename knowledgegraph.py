#!/bin/env python

import subprocess

class KnowledgeGraph(object):
  """docstring for KnowageGraph"""
  def __init__(self):
    super(KnowledgeGraph, self).__init__()


  def getKnowledgeGraph(self, keyword, path):
      crossref = self.getCrossref(keyword, path)

      return crossref
   
  def getCrossref(self, keyword, path):
      cmd = 'grep -riE "' + keyword + '" ' + path
      print cmd
      output = ''
      try:
          output = subprocess.check_output(cmd, shell=True)
      except Exception as e:
          return ''
      adict = {}
      for line in output.split('\n'):
          fileName = line[0 : line.find(':')].strip().replace('//', '/')
          firstIndex = line.find('|')
          rID = line[line.find(':') + 1 : firstIndex].strip().replace(' ', '%20')
          title = line[firstIndex + 1 : line.find('|', firstIndex + 1)].strip()
          if title != '':
              if title.find(',') != -1:
                  title = title[0 : title.find(',')]
              if adict.has_key(fileName):
                  adict[fileName].append(title)
              else:
                  adict[fileName] = [title]
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




