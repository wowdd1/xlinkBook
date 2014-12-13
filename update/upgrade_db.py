#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *
import subprocess 
import os.path

INTERPRETER = "/usr/bin/python"
  

def runPy(processor):
    args = [INTERPRETER, processor] 
    proc = subprocess.Popen(args)
    while 1:  
        ret1 = subprocess.Popen.poll(proc)  
        if ret1 == 0:  
            break

  
    
for parent,dirnames,filenames in os.walk("."):
    for filename in filenames:
        if filename.startswith("update"):
            runPy(filename)

#runPy("update_coursera.py")
