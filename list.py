#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import getopt
import time
import os,sys
from utils import Utils

source = ""
filter_keyword = ""
column_num = "2"

cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=10
color_index=0
output_with_color = False

line_max_len_list = [0, 0, 0]
line_id_max_len_list = [0, 0, 0]
def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-k,--keyword: print suggest keyword in file.'
    print '\t-i,--input: filename or dirname'
    print '\t-c,--column: from 1 to 3'
    print '\t-f,--filter: keyword for filter course'
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
    course_num = line[0 : line.find("|")]
    course_name = line[line.find("|") + 1 : ]
    if len(course_name.decode('utf8')) > course_name_len:
        course_name = course_name[0 : course_name_len - 3 ] + "..."
    else:
        course_name = course_name + get_space(0, course_name_len - len(course_name.decode('utf8')))

    if len(course_num) < course_num_len:
        space = ""
        for i in range(0, course_num_len - len(course_num)):
            space += " "
        return course_num + space + "|"+ course_name
    else:
        return course_num + "|" + course_name

def print_with_color(text):
    global color_index
    utils = Utils()
    if color_index % 2 == 0:
        utils.print_colorful("brown", True, text)
    else:
        utils.print_colorful("darkcyan", True, text)
    color_index += 1

def print_table_head(id_name, title, col):
    table_head_mid = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        space = ''
        table_head_mid += '|'
        for sp in range(0, course_num_len - len(id_name)):
            space += ' '
        table_head_mid += id_name + space + '|'
        space = ''
        for sp in range(0, course_name_len - len(title)):
            space += " "
        table_head_mid = table_head_mid + title + space

    table_head_mid += '|'
    print_table_separator(col)
    print table_head_mid
    print_table_separator(col)

def print_table_separator(col):
    table_separator = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        table_separator += "+"
        for sp in range(0, course_num_len):
            table_separator += "-"
        table_separator += "+"
        for sp in range(0, course_name_len):
            table_separator += "-"
    table_separator += "+"
    print table_separator

def get_space(start, end):
    space = ""
    for j in range(start, end):
        space += " "
    return space

def get_max_line_len(list_data):
    length = 0
    for line in list_data:
        if len(line) > length:
            length = len(line)
    return length

def update_max_len(line, col):
    if len(line) > line_max_len_list[col - 1]:
        line_max_len_list[col - 1] = len(line)
    if len(line[0 : line.find('|')]) > line_id_max_len_list[col - 1]:
        line_id_max_len_list[col - 1] = len(line[0 : line.find('|')]) 


def update_cell_len(index):
    max_len = line_max_len_list[index]
    global cell_len, course_name_len, course_num_len
    cell_len = line_max_len_list[index]
    course_num_len = line_id_max_len_list[index]
    course_name_len = cell_len - course_num_len - 1


def format_lines(list_all):
    for i in range(0, len(list_all)):
        update_cell_len(i)

        for j in range(0, len(list_all[i])):
            list_all[i][j] = alignCourseName(list_all[i][j])

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
                line = line[0 : line.find("|", line.find("|") + 1)]
                if line.lower().find(filter_keyword.lower()) != -1:
                    filter_result.append(line)
            all_lines = filter_result
        if len(all_lines) == 0:
            return  
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
        elif column_num == "1":
            list_all.append([])
         
        for line in all_lines:
            if line.find('|') != -1:
                line = line[0 : line.find("|", line.find("|") + 1)]
            line = line.replace("\n", "")
            current += 1
            if column_num == "3":
                if current <= line_half + (line_count % 3):
                    update_max_len(line, 1)
                    list_all[0].append(line)
                elif current <= 2 * line_half + (line_count % 3):
                    update_max_len(line, 2)
                    list_all[1].append(line)
                else:
                    update_max_len(line, 3)
                    list_all[2].append(line)

            elif column_num == "2":
                if current <= line_half + (line_count % 2):
                    update_max_len(line, 1)
                    list_all[0].append(line)
                else:
                    update_max_len(line, 2)
                    list_all[1].append(line)
            else:
                update_max_len(line, 1)
                list_all[0].append(line)


        if column_num == "3":
            if len(list_all[0]) - len(list_all[1]) == 2:
                list_all[1].insert(0, list_all[0][len(list_all[0]) - 1])
                list_all[0].pop()
            format_lines(list_all)
            print_table_head('id', 'title', 3)
            for i in range(0, len(list_all[2])):
                tmp = "|" + list_all[0][i] + "|" + list_all[1][i] + "|"
                content = tmp + list_all[2][i] + "|"
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
            if len(list_all[0]) > len(list_all[2]):
                last = len(list_all[0]) - 1
                content = ""
                if len(list_all[0]) == len(list_all[1]):
                    content = "|" + list_all[0][last] + "|" + list_all[1][last] + "|"
                else:
                    content = "|" + list_all[0][last] + "|" + get_space(0, line_id_max_len_list[1]) + '|' + get_space(0, line_max_len_list[1] - line_id_max_len_list[1] - 1) + '|' \
                                                            + get_space(0, line_id_max_len_list[2]) + '|' + get_space(0, line_max_len_list[2] - line_id_max_len_list[2] - 1) + '|'

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
            print_table_separator(3)
        elif column_num == "2":
            format_lines(list_all)
            print_table_head('id', 'title', 2)
            for i in range(0, len(list_all[1])):
                content = '|' + list_all[0][i] + "|" + list_all[1][i] + '|'

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
            if len(list_all[0]) > len(list_all[1]):
                last = len(list_all[0]) - 1
                content = '|' + list_all[0][last] + "|" + get_space(0, line_id_max_len_list[1]) + '|' + get_space(0, line_max_len_list[1] - line_id_max_len_list[1] - 1) + '|'
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
            print_table_separator(2)
        elif column_num == '1':
            format_lines(list_all)
            print_table_head('id', 'title', 1)
            for i in range(0, len(list_all[0])):
                content = "|" + list_all[0][i] + "|"
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
            print_table_separator(1)

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



