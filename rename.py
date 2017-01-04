#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 程序功能：遍历指定文件夹下的所有文件（包括子文件夹），删除文件名中的中的指定字符串
import os
import sys

def TraverseFolder(path):
    no = 0
    for (path, dirs, files) in os.walk(path):
        no += 1
        print '\n', "No.", no
        print u"路径为:", path

        if len(dirs) != 0:    
            subfolders = ''
            # 将子文件夹名依次加入到字符串subfolders中来
            for dir in dirs:
                subfolders += dir+';'   
            subfolders = '[' + subfolders + ']'
            print u"子文件夹名为：", subfolders

        if len(files)!=0:
            filenames = ''
            for filename in files:
                filenames += filename+';'
            filenames = '[' + filenames + ']'
            # print "files=", filenames
   

def RenameFile():
    # path = raw_input(str.encode('gbk'))
    path = '/Users/zd/dev/python/course_env/xlinkBook/db'
    #path = '/Users/zd/dev/python/course_env/xlinkBook/extensions'
    
    # character = raw_input(str.encode('gbk'))
    character = '2016'
    year = '2017'
    
    TraverseFolder(path)
    
    
    print '\n', u'开始批量更名:'
    print '-------------------------------------------------------'
    changedCount = 0          
    for (path,dirs,files) in os.walk(path):
        for filename in files:
            srcfilename = os.path.splitext(filename)[0]   
            #print filename,'\n'
            # scharacter = character - '.'    
            if (character in srcfilename):
                #print srcfilename
                '''
                print changedCount
                changedCount += 1
                '''
                newname = filename.replace(character, '2017')
                #print newname
                
                oldpath = path + "/" + filename      
                newpath = path + "/" + newname
                print oldpath
                print newpath
                #'''
                try:
                    os.rename(oldpath, newpath)
                    #print 'No.%d'%changedCount, 'change', oldpath, 'to', newpath
                except BaseException, e:  
                    print(str(e))
                #'''
                
    print '-------------------------------------------------------'
                                                                               
    
if __name__ == '__main__':
    RenameFile() 