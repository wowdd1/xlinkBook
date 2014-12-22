#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import getopt
import time
import os,sys
from utils import Utils

source = ""
align_course_name = True
filter_keyword = ""
column_num = "2"

cell_len=94  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=10
color_index=0
output_with_color = False

def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-k,--keyword: print suggest keyword in file.'
    print '\t-i,--input: filename or dirname'
    print '\t-c,--column: from 1 to 3'
    print '\t-f,--filter: keyword for filter course'
    print '\t-r,--raw: output raw data'
    print '\t-s,--style: print text with color'
    os.system("cat README.md")

def print_keyword(file_name):
    cmd = '\
        tr -sc "[A-Z][a-z]"  "[\012*]"  < ' + file_name + '|  \
        tr  "[A-Z]"  "[a-z]"  | \
        sort  | uniq -c |   \
        sort  -k1 -n -r  |  \
        head -50 | nl'
    os.system(cmd)

def alignCourseName(line):
    if align_course_name == False:
        return line   
    course_num = line[0 : line.find(" ")].strip()
    course_name = line[line.find(" ") + 1 : ].strip()
    if len(course_name) > course_name_len:
        course_name = course_name[0 : course_name_len - 3 ] + "..."

    if len(course_num) < course_num_len:
        space = ""
        for i in range(0, course_num_len - len(course_num)):
            space += " "
        return course_num + space + course_name
    return line.strip()

def print_with_color(text):
    global color_index
    utils = Utils()
    if color_index % 2 == 0:
        utils.print_colorful("brown", True, text)
    else:
        utils.print_colorful("darkcyan", True, text)
    color_index += 1

def print_list(file_name):
    current = 0
    old_line = ""
    old_line_2 = ""
    color_index = 0
    if os.path.exists(file_name):

        f = open(file_name,'rU')
        all_lines = f.readlines()
        if filter_keyword != "":
            filter_result = []
            for line in all_lines:
                line = line[0 : line.find("|", line.find("|") + 1)].replace("|","")
                if line.lower().find(filter_keyword.lower()) != -1:
                    filter_result.append(line)
            all_lines = filter_result
        
        line_count = len(all_lines)
        list_all = []
        line_half = 0
        if column_num == "3":
            list_all.append([])
            list_all.append([])
            list_all.append([])
            line_half = line_count / 3
        elif column_num == "2":
            list_all.append([])
            list_all.append([])
            line_half = line_count / 2
        
        for line in all_lines:
            if line.find('|') != -1:
                line = line[0 : line.find("|", line.find("|") + 1)].replace("|","")
            line = line.replace("\n", "")
            current += 1
            if column_num == "3":
                if current <= line_half + (line_count % 3):
                    list_all[0].append(alignCourseName(line))
                elif current <= 2 * line_half + (line_count % 3):
                    list_all[1].append(alignCourseName(line))
                else:
                    list_all[2].append(alignCourseName(line))

            elif column_num == "2":
                if current <= line_half + (line_count % 2):
                    list_all[0].append(alignCourseName(line))
                else:
                    list_all[1].append(alignCourseName(line))
            else:
                if output_with_color == True:
                    print_with_color(line)
                else:
                    print alignCourseName(line) 
        if column_num == "3":
            if len(list_all[0]) - len(list_all[1]) == 2:
                list_all[1].insert(0, list_all[0][len(list_all[0]) - 1])
                list_all[0].pop()

            for i in range(0, len(list_all[2])):
                space = ""
                for j in range(0, cell_len - len(list_all[0][i].decode('utf8'))):
                    space += " "
                tmp = list_all[0][i] + space + list_all[1][i]
                space = ""
                for j in range(0, cell_len - len(list_all[1][i].decode('utf8'))):
                    space += " "
                
                if output_with_color == True:
                    print_with_color(tmp + space + list_all[2][i])
                else:
                    print tmp + space + list_all[2][i]
            if len(list_all[0]) > len(list_all[2]):
                space = ""
                for j in range(0, cell_len - len(list_all[0][len(list_all[0]) - 1].decode('utf8'))):
                    space += " "
                if output_with_color == True:
                    print_with_color(list_all[0][len(list_all[0]) - 1] + space + list_all[1][len(list_all[1]) - 1])
                else:
                    print list_all[0][len(list_all[0]) - 1] + space + list_all[1][len(list_all[1]) - 1]

        elif column_num == "2":
            for i in range(0, len(list_all[1])):
                space = ""
                for j in range(0, cell_len - len(list_all[0][i].decode('utf8'))):
                    space += " "
                if output_with_color == True:
                    print_with_color(list_all[0][i] + space + list_all[1][i])
                else:
                    print list_all[0][i] + space + list_all[1][i]
            if len(list_all[0]) > len(list_all[1]):
                if output_with_color == True:
                    print_with_color(list_all[0][len(list_all[0]) - 1])
                else:
                    print list_all[0][len(list_all[0]) - 1]
        if current > 0:
            if filter_keyword != "":
                print "\nTotal " + str(current) + " records cotain " + filter_keyword + ", File: " + file_name + "\n\n"
            else:
                print "\nTotal " + str(current) + " records, File: " + file_name + "\n\n"
            

def print_dir(dir_name):
    cur_list = os.listdir(dir_name)
    for item in cur_list:
        if item.startswith("."):
            continue

        full_path = os.path.join(dir_name, item)
        if os.path.isfile(full_path):
            print_list(full_path)
        else:
            print_dir(full_path)


def main(argv):
    global source
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hk:i:c:f:rs', ["help", "keyword", "input=", "column=", "filter=", "raw", "style"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-k', '--keyword'):
            if os.path.isfile(a):
                print_keyword(a)
            else:
                print "please input file name"
            sys.exit(1)
        elif o in ('-i', '--input'):
            source = a
        elif o in ('-c', '--column_num'):
            global column_num
            column_num = a
        elif o in ('-f', '--filter'):
            global filter_keyword
            filter_keyword = str(a).strip()
        elif o in ('-r', '--raw'):
            global align_course_name
            align_course_name = False
        elif o in ('-s', '--style'):
            global output_with_color
            output_with_color = True
    if source == "":
        print "you must input the input file or dir"
        usage()
        return
    #if output_with_color == True:
    #    print "color"

    if os.path.isfile(source):
        print_list(source)
    else:
        print_dir(source)

if __name__ == '__main__':
    main(sys.argv)



