#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os
import re

def find_file_by_pattern(pattern='.*', base=".", circle=True):
    re_file = re.compile(pattern)
    if base == ".":
        base = os.getcwd()

    final_file_list = []
    #print base  
    cur_list = os.listdir(base)
    for item in cur_list:
        if item == ".svn" or item == ".git" or item == ".DS_Store":
            continue

        full_path = os.path.join(base, item)
        if os.path.isfile(full_path):
            if re_file.search(full_path):
                final_file_list.append(full_path)
        else:
            final_file_list += find_file_by_pattern(pattern, full_path)
    return final_file_list

def print_inx(foreground, newline, *kw):    
    cc_map = {
        'black': '30',
        'darkred': '31',
        'darkgreen': '32',
        'brown': '33', #dark yellow  
        'darkblue': '34',
        'darkmagenta': '35',
        'darkcyan': '36',
        'darkwhite': '37',
        'red': '1;31',
        'green': '1;32',
        'yellow': '1;33',
        'blue': '1;34',
        'magenta': '1;35',
        'cyan': '1;36',
        'white': '1;37',
    }

    if foreground in cc_map:
        for t in kw:
            print '\033[' + cc_map[foreground] + 'm{0}\033[0m'.format(t),
    else:
        for t in kw: print t,
    
    if newline: print
   
def print_colorful(foreground, newline, *kw):    
    try:
        if foreground == 'darkyellow':
            foreground = 'brown'
  
        if os.name == 'nt':
            print_nt(foreground, newline, *kw)
        else:
            print_inx(foreground, newline, *kw)
    except:
        for t in kw: print t,
        if newline: print
