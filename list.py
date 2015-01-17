#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import getopt
import time
import os,sys
from record import Record
from utils import Utils
import copy
import re
import itertools
import unicodedata

source = ""
filter_keyword = ""
column_num = "2"

custom_cell_len = 0
custom_cell_row = 2
cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=10
color_index=0
output_with_color = False
output_with_describe = False

line_max_len_list = [0, 0, 0]
line_id_max_len_list = [0, 0, 0]

regex = re.compile("\033\[[0-9;]*m")
py3k = sys.version_info[0] >= 3
if py3k:
    unicode = str
    basestring = str
    itermap = map
    uni_chr = chr
else: 
    itermap = itertools.imap
    uni_chr = unichr

def usage():
    print 'usage:'
    print '\t-h,--help: print help message.'
    print '\t-k,--keyword: print suggest keyword in file.'
    print '\t-i,--input: filename or dirname'
    print '\t-c,--column: from 1 to 3'
    print '\t-f,--filter: keyword for filter course'
    print '\t-s,--style: print text with color'
    print '\t-d,--describe: output the describe of the item'
    print '\t-w,--width: the width of cell'
    print '\t-r,--row: the rows of the describe'
    os.system("cat README.md")

def print_keyword(file_name):
    cmd = '\
        tr -sc "[A-Z][a-z]"  "[\012*]"  < ' + file_name + '|  \
        tr  "[A-Z]"  "[a-z]"  | \
        sort  | uniq -c |   \
        sort  -k1 -n -r  |  \
        head -50 | nl'
    os.system(cmd)

def to_unicode(value):
    if not isinstance(value, basestring):
        value = str(value)
    if not isinstance(value, unicode):
        value = unicode(value, "UTF-8", "strict")
    return value

##############################
# UNICODE WIDTH FUNCTIONS    #
##############################

def char_block_width(char):
    # Basic Latin, which is probably the most common case
    #if char in xrange(0x0021, 0x007e):
    #if char >= 0x0021 and char <= 0x007e:
    if 0x0021 <= char <= 0x007e:
        return 1
    # Chinese, Japanese, Korean (common)
    if 0x4e00 <= char <= 0x9fff:
        return 2
    # Hangul
    if 0xac00 <= char <= 0xd7af:
        return 2
    # Combining?
    if unicodedata.combining(uni_chr(char)):
        return 0
    # Hiragana and Katakana
    if 0x3040 <= char <= 0x309f or 0x30a0 <= char <= 0x30ff:
        return 2
    # Full-width Latin characters
    if 0xff01 <= char <= 0xff60:
        return 2
    # CJK punctuation
    if 0x3000 <= char <= 0x303e:
        return 2
    # Backspace and delete
    if char in (0x0008, 0x007f):
        return -1
    # Other control characters
    elif char in (0x0000, 0x001f):
        return 0
    # Take a guess
    return 1

def str_block_width(val):

    return sum(itermap(char_block_width, itermap(ord, regex.sub("", val))))

def align_id_title(record):
    course_num = record.get_id()
    course_name = record.get_title()
    if str_block_width(course_name) > course_name_len:
        course_name = course_name[0 : course_name_len - 3 ] + "..."
    else:
        course_name = course_name + get_space(0, course_name_len - str_block_width(course_name))

    if len(course_num) < course_num_len:
        space = get_space(0, course_num_len - len(course_num))
        return course_num + space + "|"+ course_name
    else:
        return course_num + "|" + course_name

def align_describe(describe):
    if str_block_width(describe) > course_name_len - 1 and output_with_describe == False:
        describe = describe[0 : course_name_len - 3 ] + "..."
    else:
        describe += get_space(0, course_name_len - str_block_width(describe))
    return get_space(0, course_num_len) + "|" + describe

def align_black(text):
    if text == "":
        return get_space(0, course_num_len) + "|" + get_space(0, cell_len - course_num_len - 1)
    else:
        if str_block_width(text) > course_name_len:
            text = text[0 : course_name_len - 3] + "..."
        return get_space(0, course_num_len) + "|" + text + get_space(0, course_name_len - str_block_width(text))

def print_with_color(text):
    global color_index
    utils = Utils()
    if color_index % 2 == 0:
        utils.print_colorful("brown", True, text)
    else:
        utils.print_colorful("darkcyan", True, text)
    color_index += 1

def print_table_head(col, id_name='id', title='title'):
    if output_with_describe == True:
        title = "describe"
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
def get_id_and_title(record):
    return record.get_id() + "|" + record.get_title()

def update_max_len(record, col):
    if str_block_width(get_id_and_title(record)) > line_max_len_list[col - 1]:
        line_max_len_list[col - 1] = str_block_width(get_id_and_title(record))
    if str_block_width(record.get_id()) > line_id_max_len_list[col - 1]:
        line_id_max_len_list[col - 1] = str_block_width(record.get_id()) 


def update_cell_len(index):
    global cell_len, course_name_len, course_num_len
    cell_len = line_max_len_list[index]
    if custom_cell_len > 0:
        cell_len = custom_cell_len        
    course_num_len = line_id_max_len_list[index]
    if cell_len == 0 or course_num_len == 0:
        cell_len = line_max_len_list[0]
        course_num_len = line_id_max_len_list[0]
    course_name_len = cell_len - course_num_len - 1


def build_lines(list_all):
    id_title_lines = copy.deepcopy(list_all)
    describe_lines = []
    for i in range(0, custom_cell_row):
        describe_lines.append(copy.deepcopy(list_all))

    for i in range(0, len(list_all)):
        update_cell_len(i)

        if len(id_title_lines[i]) == 0:
            record = Record("");
            id_title_lines[i].append(align_id_title(record))
            for l in range(0, len(describe_lines)):
                describe_lines[l][i].append(align_describe(""))


        for j in range(0, len(list_all[i])):
            id_title_lines[i][j] = align_id_title(list_all[i][j])
            describe = str_block_width(list_all[i][j].get_describe())
            if describe > course_name_len and output_with_describe == True:
                for l in range(0, len(describe_lines)):
                    if l * course_name_len > describe:
                        describe_lines[l][i][j] = align_describe("")
                        continue
                    describe_lines[l][i][j] = align_describe(list_all[i][j].get_describe()[l * course_name_len : (l + 1) * course_name_len])
            else:
                describe_lines[0][i][j] = align_describe(list_all[i][j].get_describe())
                for l in range(1, len(describe_lines)):
                    describe_lines[l][i][j] = align_describe("")

    return id_title_lines, describe_lines


def get_line(lines, start, end, j):
    result = "|"
    for i in range(start, end):
        result += lines[i][j]+ "|"

    return result

def get_space_cell(num):
    result = ""
    for i in range(0, num):
        result += get_space(0, course_num_len) + "|" + get_space(0, course_name_len)

    return result
def reset_max_len_list():
    global line_max_len_list, line_id_max_len_list
    line_max_len_list = [0, 0, 0]
    line_id_max_len_list = [0, 0, 0]

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
                record = Record(line)
                data = record.get_id() + record.get_title() + record.get_describe()
                if data.lower().find(filter_keyword.lower()) != -1:
                    filter_result.append(line)
            all_lines = filter_result[:]
        if len(all_lines) == 0:
            return  
        line_count = len(all_lines)
        list_all = []
        reset_max_len_list()
 
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
            line = to_unicode(line)
            record = Record(line.replace("\n", ""))
            current += 1
            if column_num == "3":
                if current <= line_half + (line_count % 3):
                    update_max_len(record, 1)
                    list_all[0].append(record)
                elif current <= 2 * line_half + (line_count % 3):
                    update_max_len(record, 2)
                    list_all[1].append(record)
                else:
                    update_max_len(record, 3)
                    list_all[2].append(record)

            elif column_num == "2":
                if current <= line_half + (line_count % 2):
                    update_max_len(record, 1)
                    list_all[0].append(record)
                else:
                    update_max_len(record, 2)
                    list_all[1].append(record)
            else:
                update_max_len(record, 1)
                list_all[0].append(record)


        if column_num == "3":
            if len(list_all[0]) - len(list_all[1]) == 2:
                list_all[1].insert(0, list_all[0][len(list_all[0]) - 1])
                list_all[0].pop()

        id_title_lines, describe_lines = build_lines(list_all)

        if column_num == "3":
            print_table_head(3)
            for i in range(0, len(id_title_lines[2])):
                content = get_line(id_title_lines, 0, 3, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True: 
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 3, i)

            if len(id_title_lines[0]) > len(id_title_lines[2]):
                last = len(id_title_lines[0]) - 1
                content = ""
                if len(id_title_lines[0]) == len(id_title_lines[1]):
                    content = get_line(id_title_lines, 0, 2, last) + get_space_cell(1) + "|"
                else:
                    content = get_line(id_title_lines, 0, 1, last) + get_space_cell(2) + "|"

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        if len(id_title_lines[0]) == len(id_title_lines[1]):
                            print get_line(describe_lines[l], 0, 2, last) + get_space_cell(1) + "|"
                        else:
                            print get_line(describe_lines[l], 0, 1, last) + get_space_cell(2) + "|"

            print_table_separator(3)
        elif column_num == "2":
            print_table_head(2)
            for i in range(0, len(id_title_lines[1])):
                content = get_line(id_title_lines, 0, 2, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:    
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 2, i)

            if len(id_title_lines[0]) > len(id_title_lines[1]):
                last = len(id_title_lines[0]) - 1
                content = get_line(id_title_lines, 0, 1, last) + get_space_cell(1) + "|"
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 1, last) + get_space_cell(1) + "|"

            print_table_separator(2)
        elif column_num == '1':
            print_table_head(1)
            for i in range(0, len(id_title_lines[0])):
                content = get_line(id_title_lines, 0, 1, i)

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        print get_line(describe_lines[l], 0, 1, i)

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
        opts, args = getopt.getopt(sys.argv[1:], 'hk:i:c:f:sdw:r:', ["help", "keyword", "input=", "column=", "filter=", "style", "describe", "width", "row"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    global column_num,filter_keyword, output_with_color, output_with_describe, custom_cell_len, custom_cell_row
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
            column_num = a
        elif o in ('-f', '--filter'):
            filter_keyword = str(a).strip()
        elif o in ('-s', '--style'):
            output_with_color = True
        elif o in ('-d', '--describe'):
            output_with_describe = True
            if column_num == '2':
                custom_cell_len = cell_len + (cell_len / 14)
            elif column_num == '1':
                custom_cell_len = cell_len * 2
            output_with_color = True
        elif o in ('-w', '--width'):
            custom_cell_len = int(a) 
        elif o in ('-r', '--row'):
            if int(a) > 2 and int(a) < 30:
                custom_cell_row = int(a)
            else:
                print 'the row must between 2 and 30'
    if source == "":
        print "you must input the input file or dir"
        usage()
        return
    #if output_with_color == True:
    #    print "color"
    if source.lower().find(".pdf") != -1:
        os.system("open " + source)
        return

    if os.path.isfile(source):
        print_list(source)
    else:
        print_dir(source)

if __name__ == '__main__':
    main(sys.argv)



