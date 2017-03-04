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

  def toListHtml(self, titleList, urlList, splitNumber=0, moreHtml=True):
      return self.utils.toListHtml(titleList, urlList, None, splitNumber, moreHtml, True)



