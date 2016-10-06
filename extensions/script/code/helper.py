#!/usr/bin/env python

import getopt
import sys
sys.path.append(sys.path[0][0 : sys.path[0].find('/extensions')])
from utils import Utils
from config import Config

class Helper:

  def __init__(self):
    self.utils = Utils()

  def getArgs(self, argv):
      opts, args = getopt.getopt(argv, 'i:f:', ['id', 'file'])
      id_arg = ''
      file_arg = ''
      for o, a in opts:
        if o in ('-i', '--id'):
            id_arg = a
        elif o in ('-f', '--file'):
            file_arg = a
      return id_arg, file_arg

  def toListHtml(self, titleList, urlList, splitNumber=0):
      html = ''
      start = False 
      if splitNumber == 0:
          html = '<div class="ref"><ol>'
          start = True
      count = 0
      
      for i in range(0, len(titleList)):
          title = titleList[i]
          if title == '':
              continue
          count += 1
          if splitNumber > 0 and (count == 1 or count > splitNumber):
              if start:
                  html += '</ol></div>'
                  count = 1
                
              html += '<div style="float:left;"><ol>'
              start = True

          url = urlList[i]
          html += '<li><span>' + str(i + 1) + '.</span>'
          if url != '':
              html += '<p><a target="_blank" href="' + url + '">' + title + '</a>'
          else:
              html += '<p>' + self.utils.toSmartLink(title, Config.smart_link_br_len)

          divID = 'div-' + str(i)
          linkID = 'a-' + str(i)
          appendID = str(i + 1)
          script = self.utils.genMoreEnginScript(linkID, divID, "loop-" + str(appendID), title, url, '-')
          html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', divID, '', False);

          html += '</p></li>'

      if start:
          html += '</ol></div>'
      return html



