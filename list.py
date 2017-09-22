#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08
# -*- coding: utf-8 -*-

import getopt
import time
import re
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from record import Record, Tag
from utils import Utils
import copy
from config import Config
from flask import session
import datetime

source = ""
filter_keyword = ""
column_num = Config.column_num

custom_cell_len = Config.custom_cell_len
split_length = Config.split_length
custom_cell_row = Config.custom_cell_row_list[2]
cell_len = Config.cell_len  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len = Config.course_name_len
course_num_len = Config.course_num_len
color_index = Config.color_index
output_with_color = Config.output_with_color
output_with_style = Config.output_with_style
output_with_describe = Config.output_with_describe
output_navigation_links = Config.output_navigation_links
merger_result = Config.merger_result
top_row = Config.top_row
old_top_row = Config.old_top_row
max_links_row = Config.max_links_row
max_nav_link_row = Config.max_nav_link_row
max_nav_links_row = Config.max_nav_links_row
default_links_row = Config.default_links_row

verify = ''
database = ''
dir_mode = False
username = ''

utils = Utils()
line_max_len_list = [0, 0, 0]
line_id_max_len_list = [0, 0, 0]

tag = Tag()
keyword_list = tag.tag_list

plus = '+'
subtraction = '-'
vertical = '|'
html_style = False
css_style_type = Config.css_style_type

engin = ''
loadmore_mode = False
loadmore_count = 0
plugins_mode = Config.plugins_mode

div_content_list = []
div_content_extension_list = []
div_reference_dict = {}
div_content_dict = {}

gen_html_done = False
search_box_displayed = False

search_box_hiden = False
library_hiden = False
gened_libary = False
trackmode = Config.track_mode
trackmode_engin_type = ''

script_head = '<script language="JavaScript" type="text/JavaScript">';
script_end = '</script>'
css_head = '<style type="text/css">'
css_end = '</style>'

css_style_0 = ''
css_style_1 = '\
<link rel="stylesheet" href="http://web.stanford.edu/class/cs231a/assets/css/bootstrap-rev0.min.css">\
<link href="http://fonts.googleapis.com/css?family=Roboto:400,300" rel="stylesheet" type="text/css">'

css_table_overwrite = '\
<style type="text/css">\
.table>thead>tr>th,.table>tbody>tr>th,.table>tfoot>tr>th,.table>thead>tr>td,.table>tbody>tr>td,.table>tfoot>tr>td {\
	padding:1px;\
	line-height:1.42857143;\
	vertical-align:top;\
	border-top:0px solid #ddd\
}\
</style>'


css_style_2 = css_style_1 + css_table_overwrite

css_style_3 = '\
<link rel="stylesheet" id="easy_table_style-css" href="http://ai.stanford.edu/wp-content/plugins/easy-table/themes/default/style.css?ver=1.5.3" type="text/css" media="all">\
<link rel="stylesheet" type="text/css" media="all" href="http://ai.stanford.edu/wp-content/themes/theme47542/style.css">\
'

css_style_4 = '\
<link rel="stylesheet" id="easy_table_style-css" href="http://ai.stanford.edu/wp-content/plugins/easy-table/themes/default/style.css?ver=1.5.3" type="text/css" media="all">\
' + css_table_overwrite


css_style_5 = '\
<link rel="stylesheet" type="text/css" media="all" href="http://ai.stanford.edu/wp-content/themes/theme47542/bootstrap/css/bootstrap.css">\
'  + css_style_3

css_style_6 = '\
<link href="http://vision.stanford.edu/css/style.css" rel="stylesheet">\
'


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
    print '\t-t,--top: the top number rows for display'
    print '\t-l,--level: the max search level that the file is in'
    print '\t-m,--merger: merger the results'
    print '\t-b,--border: border style'
    print '\t-n,--navigation: gen navigation links'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    os.system("cat README.md")


def border_style_one():
    global plus, subtraction, vertical
    plus = ' '
    subtraction = ' '
    vertical = ' '

def border_style_two():
    global plus, subtraction, vertical
    plus = '+'
    subtraction = '-'
    vertical = '|'

def border_style_three():
    global plus, subtraction, vertical
    plus = ' '
    subtraction = '.'
    vertical = '.'

def border_style_four():
    global plus, subtraction, vertical, html_style
    plus = '+'
    subtraction = '-'
    vertical = '|'
    html_style = True

def border_style_five(row = 1):
    border_style_four()
    global custom_cell_row, output_with_describe
    #custom_cell_row = row
    #output_with_describe = True

def border_style_custom(style):
    global plus, subtraction, vertical
    plus = ' '
    subtraction = style
    vertical = style

def chanage_border(style):
    if style == '1':
        border_style_one()
    elif style == '2':
        border_style_two()
    elif style == '3':
        border_style_three()
    elif style == '4': #html style
        border_style_four()
    elif style == '5': #html style
        border_style_five()
    else:
        border_style_custom(style)

def print_keyword(file_name):
    cmd = '\
        tr -sc "[A-Z][a-z]"  "[\012*]"  < ' + file_name + '|  \
        tr  "[A-Z]"  "[a-z]"  | \
        sort  | uniq -c |   \
        sort  -k1 -n -r  |  \
        head -50 | nl'
    os.system(cmd)


def contain_keyword(text):
    for k in keyword_list:
        if text.find(k) != -1 or text.find(k.replace(':', '')) != -1:
            return True
    return False

def contain_desc_keyword(content):
    return content.find('description:') != -1 or content.find('summary:') != -1


def align_id_title(record):
    course_num = record.get_id()
    course_name = utils.caseLine(record.get_title())
    if html_style == False:
        if utils.str_block_width(course_name) > course_name_len:
            course_name = course_name[0 : course_name_len - 3 ] + "..."
        else:
            course_name = course_name + get_space(0, course_name_len - utils.str_block_width(course_name))
    else:
        if column_num == '3':
            if utils.str_block_width(course_name) > course_name_len:
                course_name = course_name[0 : course_name_len - 5 ] + "..."
        else:
            if utils.str_block_width(course_name) > course_name_len + 15:
                course_name = course_name[0 : course_name_len - 3 ] + "..."

    if len(course_num) < course_num_len:
        space = get_space(0, course_num_len - len(course_num))
        return course_num + space + vertical + course_name
    else:
        return course_num + vertical + course_name


last_need_smart_link = False
def align_describe(describe, record=None, containID=''):
    if html_style == False:
        if utils.str_block_width(describe) > course_name_len - 1 and output_with_describe == False:
            describe = describe[0 : course_name_len - 3 ] + "..."
        else:
            describe += get_space(0, course_name_len - utils.str_block_width(describe))
        return get_space(0, course_num_len) + vertical + describe
    else:
        global last_need_smart_link
        need_smart_link2 = needSmartLink(describe)
        if last_need_smart_link and need_smart_link2 == False:

            if last_content.strip().find(describe.strip()) != -1:
                return vertical 
            else:
                last_need_smart_link = need_smart_link2
                return vertical + describe


        last_need_smart_link = need_smart_link2
        if need_smart_link2:
            return  vertical + smartLink(describe, record, containID=containID)
        else:
            return vertical + describe

def needSmartLink(describe):
    if describe.find(':') == -1:
        return False
    else:
        prefix = describe[0 : describe.find(':') + 1].strip()

        if isSmartLinkTag(prefix) or isAccountTag(prefix):
            return True
        else:
            return False

def print_with_color(text):
    global color_index
    if color_index % 2 == 0:
        utils.print_colorful("brown", True, text)
    else:
        utils.print_colorful("darkcyan", True, text)
    color_index += 1

def print_table_head(col, id_name='id', title='topic'):
    if subtraction.strip() == '':
        return
    if output_with_describe == True:
        title = "detail"
    table_head_mid = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        table_head_mid += vertical
        len_1 = course_num_len - len(id_name)
        len_2 = course_name_len - len(title)
        space_1 = get_space(0, len_1)[0 : len_1 / 2]
        space_2 = get_space(0, len_2)[0 : len_2 / 2]
        if len_1 % 2 == 0 and len_2 % 2 == 0:
            table_head_mid += space_1 + id_name + space_1 + vertical + space_2 + title + space_2
        else:
            if len_1 % 2 == 0:
                table_head_mid += space_1 + id_name + space_1
            else:
                table_head_mid += space_1 + id_name + space_1 + ' '

            if len_2 % 2 == 0:
                table_head_mid += vertical + space_2 + title + space_2
            else: 
                table_head_mid += vertical + space_2 + title + space_2 + ' '

    table_head_mid += vertical
    print_table_separator(col)
    print table_head_mid
    print_table_separator(col)

def print_table_separator(col):
    table_separator = ''
    for i_i in range(0, col):
        update_cell_len(i_i)
        table_separator += plus
        for sp in range(0, course_num_len):
            table_separator += subtraction
        table_separator += plus
        for sp in range(0, course_name_len):
            table_separator += subtraction
    table_separator += plus
    print table_separator

def get_space(start, end):
    if html_style:
        return ""
    else:
        return (end - start) * " "

def get_id_and_title(record):
    return record.get_id() + vertical + record.get_title()

def update_max_len(record, col):
    id_title_len = utils.str_block_width(get_id_and_title(record))
    if id_title_len > line_max_len_list[col - 1]:
        line_max_len_list[col - 1] = utils.str_block_width(get_id_and_title(record))

    if utils.str_block_width(record.get_id()) > line_id_max_len_list[col - 1]:
        line_id_max_len_list[col - 1] = utils.str_block_width(record.get_id()) 



def update_cell_len(index):
    global cell_len, course_name_len, course_num_len
    cell_len = line_max_len_list[index]
    if custom_cell_len > 0:
        cell_len = custom_cell_len

    course_num_len = line_id_max_len_list[index]
    if cell_len == 0 or course_num_len == 0:
        cell_len = line_max_len_list[0]
        course_num_len = line_id_max_len_list[0]

    if Config.hiden_record_id and html_style:
        course_name_len = cell_len
    else:
        course_name_len = cell_len - course_num_len - 1


def genEnginOption(selectid, defaultEngin=Config.smart_link_engin):

    option = ''
    engin_list = utils.getAllEnginList()
    option = '<select id="' + selectid +'">'

    if plugins_mode == False:
        if defaultEngin != '':
            option += '<option value ="' + utils.getEnginUrl(defaultEngin) + '">' + defaultEngin + '</option>'
        option += '<option value ="exclusive">exclusive</option>'
    else:
        option += '<option value ="exclusive">exclusive</option>'
        if defaultEngin != '':
            option += '<option value ="' + utils.getEnginUrl(defaultEngin) + '">' + defaultEngin + '</option>'
            
    #if plugins_mode == False:
        #option += '<option value ="exclusive">exclusive</option>'
        #option += '<option value ="add">add (operate)</option>'
    #option += '<option value ="' + utils.getEnginUrl("google") + '">google</option>'
    for e in engin_list:
        if e == "google" or e == defaultEngin:
            continue
        option += '<option value ="' + utils.getEnginUrl(e) + '">' + e + '</option>'
    option += '</select>'
    return option

output_script_already = False


def loadJSScript():
    result = ''
    result += script_head
    result += loadFiles('web', '.js')
    result += script_end
    return result
    
def loadCSS():
    result = ''
    result += css_head
    result += loadFiles('web', '.css')
    result += css_end
    return result

def loadFiles(folder, fileType):
    cur_list = os.listdir(folder + '/')
    result = ''
    f_list = []
    f_list_2 = []
    for f in cur_list:
        if f.startswith('jquery'):
            f_list.append(f)
        else:
            f_list_2.append(f)
    cur_list = f_list + f_list_2
    for f in cur_list:
        if f.endswith(fileType):
            result += ''.join(open(folder + '/' + f, 'rU').readlines())
    return result

def getScript(file_name, first_record, total_records):
    if loadmore_mode:
        return 
    global output_script_already
    if output_script_already == True:
        return
    output_script_already = True
    global script
    print "<head>"
    #print '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'

    if Config.distribution == False:
        print script_head
        print "var default_tab = '" + Config.default_tab + "';"
        print "var second_default_tab = '" + Config.second_default_tab + "';"
        if Config.hiden_record_id:
            Config.disable_thumb = 'true'
        print "var disable_thumb = " + Config.disable_thumb + ";"
        if trackmode:
            print "var track_mode = true;";
            print "var trackmode_engin_type = '" + trackmode_engin_type + "';"
        else:
            print "var track_mode = false;";

        print "var array = []; "
        print "var extension_array = [];" 
        print "var reference = new Array();"
        print "var content = new Array();"
        print "var engin_args = '" + engin + "';" 
        if len(div_content_list) > 0:
            for content in div_content_list:
                print "array.push('" + content + "');" 
        if len(div_content_extension_list) > 0:
            for content in div_content_extension_list:
                print "extension_array.push('" + content + "');" 


        print 'var user_name = "' + username + '";'
        print 'var fileName = "' + os.getcwd() + '/' + source + '";'
        print 'var library = "' + os.getcwd() + '/db/library/' + Config.default_library + '";'
        print 'var column = "' + column_num + '";'
        print 'var database = "' + database + '";'
        print 'var key = "";'
        print 'var starDivCount = ' + str(starDivCount) + ';'
        print 'var hidenMoreCount = ' + str(custom_cell_row) + ';' 
        if plugins_mode == False:
            if len(Config.smart_engin_for_dialog) > 0:
                print 'var dialog_engin_count = ' + str(len(Config.smart_engin_for_dialog)) + ';'
            else:
                print 'var dialog_engin_count = ' + str(len(utils.getEnginList('d:' + Config.recommend_engin_type_for_dialog))) + ';'
            if len(Config.command_for_dialog) > 0 and source.find('-library') != -1:
                print 'var dialog_command_count = ' + str(len(Config.command_for_dialog)) + ';'
            else:
                print 'var dialog_command_count = 0;'
        if source.endswith('/') == False:
            print 'key = "' + source[source.rfind('/') + 1 :] + '";'
        extensions = utils.getExtensions()
        if len(extensions) > 0:
            print 'var extensions = [];'
            for e in extensions:
                print "extensions.push('" + e + "');"

        print script_end

        if plugins_mode or total_records == 1:
            title = first_record.get_title().strip().replace(' ', '%20')
            if plugins_mode:
                click_more = "document.addEventListener('DOMContentLoaded', function () {\
        	        setText('a-0-0-0');\
        	        showdiv('div-000','a-0-0-0');\
        	        appendContent('div-0-0-0','','" + title + "','','',false);\
                        navTopic(document.getElementById('div-0-0-0-nav-all'),'div-0-0-0','div-0-0-0-nav-',4);\
                        var search_txt = document.getElementById('search_txt');\
                        search_txt.focus();\
                        search_txt.onchange=function(){\
                            var search_a = document.getElementById('a-0-0-0');\
                            if (search_a.text == 'less' && this.value.length > 0) {\
                                setText('a-0-0-0');\
                                showdiv('div-0-0-0','a-0-0-0');\
                                setText('searchbox-a');showdiv('searchbox_div', 'searchbox-a');appendContentBox('searchbox_div', 'search_txt');\
                            }\
                        };\
        	    });";
            elif total_records == 1:
                click_more = "document.addEventListener('DOMContentLoaded', function () {\
                    setText('a-0-0-0');\
                    showdiv('div-000','a-0-0-0');\
                    appendContent('div-0-0-0','" + first_record.get_id().strip() + "','" + title + "','" + first_record.get_url().strip() + "','',false);"
                for i in range(0, custom_cell_row):
                    click_more += "showdiv('td-div-0-0-" + str(i) + "', 'a-0-0-0');showdiv('tr-0-" + str(i) + "', 'a-0-0-0');"
                click_more +="});";
            print script_head + click_more + script_end

        if plugins_mode == False:
            mathjs = '<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>'
            print mathjs
        print loadJSScript()

        if plugins_mode == False:
            print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'

    print loadCSS()
    ref_class = css_head
    ref_class += '.ref { margin: 5px;'
    if column_num == "3":
        ref_class += "width: 485px;"
    if column_num == "2":
        ref_class += "width: 575px;"
    if column_num == "1":
        ref_class += "width: 900px;"
    ref_class += "}" 
    ref_class += css_end
    print ref_class
    if output_with_style and plugins_mode == False:
        if css_style_type == 0:
            print css_style_0
        elif css_style_type == 1:
            print css_style_1
        elif css_style_type == 2:
            print css_style_2
        elif css_style_type == 3:
            print css_style_3
        elif css_style_type == 4:
            print css_style_4
        elif css_style_type == 5:
            print css_style_5
        elif css_style_type == 6:
            print css_style_6



    print "</head>"

starDivCount = 0
def build_lines(list_all, file_name):
    #print 'build_lines start:' + str(datetime.datetime.now())
    global div_link_content, gen_html_done, max_links_row, starDivCount;
    id_title_lines = copy.deepcopy(list_all)
    describe_lines = []
    engin_list = []
    if engin != '':
        engin_list = utils.getEnginList(engin.strip(), file_name, recommend=Config.recommend_engin)
        #print engin
        #print engin_list
        if len(engin_list) > Config.recommend_engin_num:
            engin_list = engin_list[0 : Config.recommend_engin_num]

    global loadmore_count
    if source.find('arxiv') != -1 and filter_keyword == '':
        loadmore_count = source[source.find('arxiv') + 11 : source.find('-')]
        loadmore_count = int(loadmore_count) - 300

    #print engin_list
    if plugins_mode:
        max_links_row = 9
    if len(engin_list) > default_links_row:
        row = len(engin_list) / max_links_row
        if len(engin_list) % max_links_row > 0:
            row += 1
        if row == 0:
            row = 1
        
        border_style_five(row)
    if output_navigation_links or len(engin_list) > 0:
        border_style_five() 
    title = ''
    id = ''
    url = ''
    #print custom_cell_row
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
            engin_list_dict = {}
            title = ''
            id_title = align_id_title(list_all[i][j])
            title = id_title[id_title.find('|') + 1 : ]
            id = id_title[0 : id_title.find('|')].strip()
            if html_style == False or (list_all[i][j].get_url().strip() == '' and engin == ''):
                id_title_lines[i][j] = id_title
            else:
                url = list_all[i][j].get_url()
                #if html_style and title.find('(') != -1 and title.strip().startswith('(') == False:
                #    title = title[0 : title.find('(')].strip()
                
                #if url.strip() != '':
                #    id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + '<a href="' + url + '" target="_blank">' + title + '</a>'
                rid = id_title[0: id_title.find('|')]
                if plugins_mode:
                        id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + title.strip().replace('%20', ' ')
                else:
                    if url.strip() != '':
                        id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + utils.enhancedLink(url, title.strip(), module='main', library=source, rid=rid, resourceType='topic')
                    else:
                        
                        id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + utils.toSmartLink(title.strip(), noFormat=(column_num == '1'), module='main', library=source, rid=rid, resourceType='topic')

                if engin != '':
                    engin_list_dict = utils.getEnginListLinks(engin_list, '#topic', id, engin.strip(), useQuote=True, module='star', library=source, pluginsMode=plugins_mode, fontSize=10)  #, '#33EE22')
                    #print engin_list_dict

            describe = utils.str_block_width(list_all[i][j].get_describe())
            start = 0
            end = 0
            if (output_with_describe or html_style) and (dir_mode == False or merger_result):
                lij = ''
                lines = len(describe_lines)
                linkID = ''
                content_divID = ''
                script = ''
                engin_content = ''
                nav_link_content = ''
                nav_links_content = ''
                
                for l in range(0, lines):
                    ijl = str(i) + '-' + str(j) + '-' + str(l)

		    if html_style:
                        describe_lines[l][i][j] = align_describe('')
                        if (engin != '' and engin_list_dict != '') or output_navigation_links:
                            engin_list_dive = []
                            engin_list_sub = []
                            engin_list_sub = engin_list

                            if l == 0:
                                if loadmore_mode and loadmore_count != 0:
                                    linkID = 'a-' + str(loadmore_count) + '-' + ijl;
                                    content_divID = "div-" + str(loadmore_count) + '-' + ijl
                                else:
                                    linkID = 'a-' + ijl;
                                    content_divID = "div-" + ijl
                                script += utils.genMoreEnginScript(linkID, content_divID, id, title.strip().replace(' ', '%20'), list_all[i][j].get_url().strip(), utils.getEnginUrlOtherInfo(list_all[i][j]), hidenEnginSection=Config.hiden_engins)


                            if output_with_describe and end < describe:
                                if loadmore_mode and loadmore_count != 0:
                                    script += "showdiv('td-div-" + str(loadmore_count) + '-' + ijl  + "', '" + linkID +"');"
                                    script += "showdiv('tr-" + str(loadmore_count) + '-' + str(j) + '-' + str(l) + "', '" + linkID +"');"
                                else:
                                    script += "showdiv('td-div-" + ijl  + "', '" + linkID +"');"
                                    script += "showdiv('tr-" + str(j) + '-' + str(l) + "', '" + linkID +"');"
                            if gen_html_done == False:

                                if (l+1) * max_links_row < len(engin_list_sub):
                                    engin_list_dive = engin_list_sub[l * max_links_row : (l+1) * max_links_row]
                                else:
                                    engin_list_dive = engin_list_sub[l * max_links_row :]

                                #print engin_list_dive
                                if len(engin_list_dive) == 0:
                                    describe_lines[l][i][j] = align_describe('')
                                else:
                                    describe_lines[l][i][j] = '#' + '#'.join(engin_list_dive)
                                if describe_lines[l][i][j].find('#') != -1:
                                    starDivCount += 1
                                    describe_lines[l][i][j] = describe_lines[l][i][j][0 : describe_lines[l][i][j].find('|') + 1] + \
                                                      '<div id="#div-star-' + str(l) +'" >' + describe_lines[l][i][j][describe_lines[l][i][j].find('|') + 1 : ] 
                                    if Config.hiden_engins and engin_list_dive[len(engin_list_dive) -1 ] == engin_list_sub[len(engin_list_sub) - 1]:
                                        describe_lines[l][i][j] += "#more"
                                    describe_lines[l][i][j] += '</div>'
                                    for (k, v) in engin_list_dict.items():
                                        describe_lines[l][i][j] = describe_lines[l][i][j].replace('#' + k.strip(), v)
                                    if len(engin_list_dict) > 0:
                                        engin_content = describe_lines[l][i][j].replace('|', '').strip().replace("'","")
                                        div_content_list.append(engin_content)
                                describe_lines[l][i][j] = ''
                                if l == lines - 1 and output_navigation_links:
                                    navLinks = utils.getNavLinkList(engin)
                                    content = ''
                                    hidenScript = ''
                                    hidenScript2 = ''
                                    hidenScript3 = ''
                                    #print 'l ' + str(l) + ' lines:' + str(lines - 1)
                                    #print 'getEnginTypes start:' + str(datetime.datetime.now()) + '<br>'
                                    last_engin_type = utils.getEnginTypes()[len(utils.getEnginTypes()) - 1]
                                    #print 'getEnginTypes end:' + str(datetime.datetime.now()) + '<br>'
                                    nopass_flag = True
                                    for link2 in navLinks:
                                        hidenScript += 'hidendiv_2("' + '#div-' + link2 + '");'
                                        if nopass_flag:
                                            hidenScript2 += 'hidendiv_2("' + '#div-' + link2 + '");'
                                        else:
                                            hidenScript3 += 'hidendiv_2("' + '#div-' + link2 + '");'
                                        if link2 == last_engin_type:
                                            nopass_flag = False
                                    count = 0
                                    count_index = 0
                                    nav_div_id = ''
                                    length = 0
                                    is_extension = False
                                    hidenScript = hidenScript2
                                    #print 'navLinks start:' + str(datetime.datetime.now()) + '<br>'
                                    for link in navLinks:
                                        nav_div_id = "#div-nav-" + str(count_index)
                                        divID = '#div'
                                        aid = "#div-nav-" + link
                                        if is_extension:
                                            hidenScript = hidenScript3
                                        if link == 'exclusive':
                                            hidenScript += 'hidenMoreContent(this.parentNode.parentNode.id,1);'
                                        #print 'genLinkWithScript2 start:' + str(datetime.datetime.now())
                                        content += utils.genLinkWithScript2(hidenScript + 'navTopic(this,\"' + divID + '\",\"' + '#div-nav-' + '\",' + str((len(navLinks) / max_nav_link_row) + 4) + ');', link, '#888888', 9, aid)
                                        #print 'genLinkWithScript2 end:' + str(datetime.datetime.now())
                                        count += 1 
                                        length += len(link) + 1
                                        if count >= max_nav_link_row or length > split_length or link == last_engin_type:
                                            div_style = ''
                                            if is_extension:
                                                continue
                                            #if column_num != 1:
                                            #    div_style = 'background-color:#EEEEFF; border-radius: 3px 3px 3px 3px;'
                                            if Config.hiden_engins:
                                                div_content_list.append('<div id="' + nav_div_id + '" style="display: none; ' + div_style + '">')
                                            else:
                                                div_content_list.append('<div id="' + nav_div_id + '" style="' + div_style + '">')
                                            div_content_list.append(content)
                                            div_content_list.append('</div>')
                                            count_index += 1
                                            count = 0
                                            content = '' 
                                            length = 0
                                            hidenScript2 += 'hidendiv_3("' + nav_div_id + '");'
                                        if link == last_engin_type:
                                            is_extension = True

                                    #print 'navLinks end:' + str(datetime.datetime.now()) + '<br>'
                                    #print 'genMoreEnginHtml start:' + str(datetime.datetime.now()) + '<br>'
                                    if Config.extension_mode == False and Config.hiden_engins:
                                        more_html = ''
                                        if Config.disable_nav_engins == False:
                                            more_html = utils.genMoreEnginHtml('#div-' + linkID, hidenScript2 + 'setText("' + '#div-' + linkID + '")', '...', content_divID + '-' + content_divID, doubleQ=False)
                                        for index in range(0, len(div_content_list)):
                                            if div_content_list[index].find('#more') != -1:
                                                div_content_list[index] = div_content_list[index].replace('#more', more_html)
                                                break
                                    #print 'genMoreEnginHtml end:' + str(datetime.datetime.now()) + '<br>'
                                    if content != '' and plugins_mode == False:
                                        div_style = ''
                                        if Config.backgrounds[Config.background] == '':
                                            div_style += 'background-color:#F8F8FF;'
                                        div_style += 'border-radius: 5px 5px 5px 5px; width:auto; float:left;'
                                        div_content_extension_list.append('<div id="' + nav_div_id + '" style="' + div_style + '">')
                                        div_content_extension_list.append(content)
                                        div_content_extension_list.append('</div>')
                                        #if plugins_mode == False:
                                        #if column_num == '3':
                                        div_content_extension_list.append('<br>')
                                    #print 'getDescDivs start:' + str(datetime.datetime.now()) + '<br>'
                                    dataMarginTop = getDataMarginTop()
                                    for link in navLinks:
                                        divID = '#div-' + link
                                        div_content_extension_list.append(utils.getDescDivs(divID, link, title.replace(' ', '%20'), max_nav_links_row, 'searchTopic(this,"' + "#rid" + '","' +"#topic" + '","' + "#otherInfo" + '");', '#822312', '#131612', 12, dataMarginTop=dataMarginTop, disableNavEngins=Config.disable_nav_engins))
                                    #print 'getDescDivs end:' + str(datetime.datetime.now()) + '<br>'
                                if l == lines - 1:
                                    gen_html_done = True

                    if end >= describe:
                        if html_style == False:
                            describe_lines[l][i][j] = align_describe("")
                        continue
                    record_describe = list_all[i][j].get_describe()
                    end = utils.next_pos(record_describe, start, course_name_len, keyword_list, htmlStyle=html_style, library=source2library(source)) 
                    if output_with_describe and Config.distribution == False:
                        #print list_all[i][j].get_describe()+ '<br>'
                        #print list_all[i][j].get_describe()[start : end] + '<br>'
                        describe_lines[l][i][j] = align_describe(list_all[i][j].get_describe()[start : end], list_all[i][j], containID="td-div-" + ijl)
                        #print describe_lines[l][i][j] + '<br>'
                        #print 'start:' + str(start) + '<br>'
                        #print 'end:' + str(end) + '<br>'
                        #print 'course_name_len: ' + str(course_name_len) + '<br>'
                    start = end
                count = 0
                
                if html_style: 
                    if url.strip() != '' and url.find(Config.ip_adress) == -1:
                        id_title_lines[i][j] += utils.getIconHtml('url', width=10, height=8)
                    if Config.extension_mode == False and Config.disable_default_engin == False:
                        id_title_lines[i][j] += utils.getDefaultEnginHtml(title, default_links_row)
                    if script != '' and Config.distribution == False:
                        id_title_lines[i][j] += utils.genMoreEnginHtml(linkID, script, '...', content_divID);
            elif engin != '' and html_style and engin_list_dict != '' and dir_mode == False:
                for (k, v) in engin_list_dict.items():
                    id_title_lines[i][j] += v
            
    #print 'build_lines end:' + str(datetime.datetime.now())
    return id_title_lines, describe_lines

def getDataMarginTop():
    return ''
    '''
    if column_num == '1':
        return ''
    else:
        return '15'
    '''

def get_line(lines, start, end, j):
    result = vertical
    text = ''
    for i in range(start, end):
        rID = ''
        if isinstance(lines[i][j], Record):
            lines[i][j] =  u' '.join(lines[i][j].get_describe()).encode('utf-8')
        text = utils.color_keyword(lines[i][j], keyword_list, color_index=color_index, html_style=html_style)
        if html_style and text.strip() == '':
            text = vertical
        result += text + vertical
    return result

def gen_html_body(content, row=0):
    style = 'info'
    if row % 2 == 0:
        style = ''
    
    index = 0
    if vertical == '|': 
        verticals = []
        id_style = 'vertical-align:top; width:' + str(course_num_len) + 'px; '
        name_style = 'vertical-align:top; width:' + str(course_name_len * 9) + 'px; '
        if Config.title_font_size > 0:
            name_style += 'font-size:' + str(Config.title_font_size) + '; '
        if Config.hiden_record_id:
            id_style += 'display: none; '
        if column_num == "2":
            verticals = ['<tr class="' + style + '"><td style="' + id_style + '">', '<div id="#div-thumb-0"></div></td><td style="' + name_style + '">', '</td><td style="' + id_style + '">', '<div id="#div-thumb-1"></div></td><td style="' + name_style + '">', '</td></tr>']   
        elif column_num == "3":
            verticals = ['<tr class="' + style + '"><td style="' + id_style + '">', '<div id="#div-thumb-0"></div></td><td style="' + name_style + '">', '</td><td style="' + id_style + '">', '<div id="#div-thumb-1"></div></td><td style="' + name_style + '">', '</td><td style="' + id_style + '">', '<div id="#div-thumb-2"></div></td><td style="' + name_style + '">', '</td></tr>']   
        elif column_num == "1":
            verticals = ['<tr class="' + style + '";"><td style="' + id_style + '">', '<div id="#div-thumb-0"></div></td><td style="' + name_style + '">', '</td></tr>']   

        ids = []
        content_back = content.split('|')
        for index in range(0, len(content_back)):
            if (index + 1) % 2 == 0 and index != 0:
                ids.append(content_back[index].strip())

        index = 0
        #print '--->'
        #print content
        while content.find(vertical) != -1:
            content = content[0 :content.find(vertical)] + verticals[index] + content[content.find(vertical) + 1:]
            index = index + 1
        for i in range(0, len(ids)):
            content = content.replace('#div-thumb-' + str(i), 'div-thumb-' + ids[i].lower())
            

    if Config.split_height > 0:
        return content + '<tr class="info" style="height: ' + str(Config.split_height) + 'px;"></tr>'
    else:
        return content

def get_background_color(content):
    content_back = content.split('|')
    background_colors = []
    for index in range(0, len(content_back)):
        if (index + 1) % 2 != 0 and index != 0:
            if (css_style_type == 0 or css_style_type == 6) and ((contain_keyword(content_back[index].strip()) == False or (contain_desc_keyword(content_back[index].strip())))):
                #background_colors.append('background-color:#f6f5ec; border-radius: 5px 5px 5px 5px;')
                if Config.backgrounds[Config.background] == '':
                    background_colors.append('background-color:#F8F8FF; border-radius: 5px 5px 5px 5px;')
                else:
                    background_colors.append('')
            else:
                background_colors.append('')
    return background_colors

def gen_html_body_v2(content, row, subRow):
    style = 'info'
    if row % 2 == 0:
        style = ''
    index = 0
    tr_id = ''
    td_div_id = ''
    td_div_0 = ''
    td_div_1 = ''
    td_div_2 = ''
    
    if loadmore_mode and loadmore_count > 0:
        tr_id = "tr-" + str(loadmore_count) + '-' + str(row) + '-' +str(subRow)
        td_div_id = '-' + str(row) + '-' + str(subRow)
        td_div_0 = 'td-div-' + str(loadmore_count) + '-' + '0' + td_div_id
        td_div_1 = 'td-div-' + str(loadmore_count) + '-' + '1' + td_div_id
        td_div_2 = 'td-div-' + str(loadmore_count) + '-' + '2' + td_div_id
    else:
        tr_id = "tr-" + str(row) + '-' +str(subRow)
        td_div_id = '-' + str(row) + '-' + str(subRow)
        td_div_0 = 'td-div-0' + td_div_id
        td_div_1 = 'td-div-1' + td_div_id
        td_div_2 = 'td-div-2' + td_div_id

    if vertical == '|':
        verticals = []
        id_style = ''
        background_color = ""
        if Config.hiden_record_id:
            id_style = 'style="display: none;"'
        background_colors = get_background_color(content)
        auto_size = ' width:auto; float:left;'
        if column_num == "2":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td ' + id_style + '>', '</td><td><div  id="' + td_div_0 + '" style="display: none; ' + background_colors[0] + auto_size + '">', '</div></td><td ' + id_style + '>', '</td><td><div id="' + td_div_1 + '" style="display: none; ' + background_colors[1] + auto_size + '">', '</div></td></tr>']
        elif column_num == "3":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td ' + id_style + '>', '</td><td><div id="' + td_div_0 + '" style="display: none; ' + background_colors[0] + auto_size + '">', '</div></td><td ' + id_style + '>', '</td><td><div id="' + td_div_1 + '" style="display: none; ' + background_colors[1] + auto_size + '">', '</div></td><td ' + id_style +'>', '</td><td><div id="' + td_div_2 + '" style="display: none; ' + background_colors[2] + auto_size + '">', '</div></td></tr>']
        elif column_num == "1":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td ' + id_style +'>', '</td><td><div id="' + td_div_0 + '" style="display: none; ' + background_colors[0] + auto_size + '">', '</div></td></tr>']

        while content.find(vertical) != -1:
            content = content[0 :content.find(vertical)] + verticals[index] + content[content.find(vertical) + 1:]
            index = index + 1

    return content

last_content = ''
def smartLink(content, record, containID=''):
    global last_content
    if content == '':
        return ''
    if content.strip().startswith('path:'):
        path = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'path', 'library' : source2library(source)}).strip()
        last_content = path
        if path.find('/custom') != -1:
            return ''
        if path.find(' ') != -1:
            path = path[0 : path.find(' ') ].strip()
        src = 'http://' + Config.ip_adress + '/?db=' + path[path.find('/') + 1 : path.rfind('/') + 1]+ '&key=' + path[path.rfind('/') + 1 : ] + '&column=2'
        folder = 'http://' + Config.ip_adress + '/?db=' + path[path.find('/') + 1 : path.rfind('/') + 1]+ '&key=?'
        alt = path[path.find('db') :]
        result = content[0 : content.find('db/')] + '&nbsp;'
        if path != source[source.find('db/') :]:
            result += utils.enhancedLink(src, 'path-file', img='<img alt="' + alt+ '" src="https://publicportal.teamsupport.com/Images/file.png" width="20" height="20">', module='main', library=source, rid=record.get_id()) + '&nbsp;'

        result += utils.enhancedLink(folder, 'path-dir', img='<img src="http://cdn.osxdaily.com/wp-content/uploads/2014/05/users-folder-mac-osx.jpg" width="20" height="15">', module='main', library=source, rid=record.get_id())
        
        return result
    elif content.strip().startswith('id:'):
        last_content = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'id', 'library' : source2library(source)}).strip()
        if record.get_url() != None and record.get_url() != '':
            return content[ 0 : content.find(':') + 1 ] + utils.enhancedLink(record.get_url().strip(), record.get_id().strip(), module='main', library=source, rid=record.get_id())
        else:
            return content
    elif content.strip().startswith('category:'):
        last_content = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'category', 'library' : source2library(source)}).strip()
        tags = content[content.find(':') + 1 : ].strip()
        if tags.find(',') != -1:
            tags = tags.split(',')
        elif tags.find(' ') != -1:
            tags = tags.split(' ')
        else:
            tags = [tags]
        html = ''
        for tag in tags:
            engin = utils.getTopEngin(tag.strip())
            if engin != '':
                html += utils.toSmartLink(record.get_title().strip(), engin=engin, showText=tag, module='main', library=source, rid=record.get_id()) 
                if tag.strip() != tags[len(tags) - 1].strip():
                    html += '<font color="blue"><i>,</i></font>&nbsp;'
        if html != '':
            return content[ 0 : content.find(':') + 1 ] + html
        else:
            return content
    elif content.strip().startswith('videourl:'):
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : 'videourl', 'library' : source2library(source)})
        last_content = ret
        html = utils.enhancedLink(ret.strip(), 'video', module='main', library=source, rid=record.get_id())
        return content[ 0 : content.find(':') + 1 ] + html
    elif isAccountTag(content):
        tag = content[ 0 : content.find(':')].strip()
        return genAccountHtml(tag, record, content, containID=containID)

    elif isSmartLinkTag(content):
        html = ''
        tag = content[ 0 : content.find(':')].strip()
        #ret = content[content.find(':') + 1 : ].strip()
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : tag, 'library' : source2library(source)})
        #print ret + '<br>'
        #ret = 
        last_content = ret
        if ret == None:
            return ''
        split_char = ','
        #if ret.find(' and ') != -1:
        #    ret = ret.replace(' and ', ', ')
        if ret.find(' or ') != -1:
            ret = ret.replace(' or ', ', ')
        #elif ret.find('/') != -1:
        #    ret = ret.replace('/', ', ')
        elif ret.find(';') != -1:
            #ret = ret.replace(';', ', ')
            split_char = ';'

        if tag == 'agent':
            return genSmartAgentLinkHtml(tag, ret, record, split_char, content)
        elif isDirectLinkTag(content):
            return genSmartLinkHtml(tag, ret, record, split_char, '', content, dialogMode=False, containID=containID)
        else:
            digMode = True
            if Config.smart_engin_for_tag_batch_open and Config.smart_engin_for_tag.has_key(tag):
                digMode = False
            else:
                digMode = True
            crossref = False

            if tag =='crossref':
                crossref = True
                #print content + "<br>"
                #print ret + '<br>'
                ret = content[content.find(':') + 1 :]
            return genSmartLinkHtml(tag, ret, record, split_char, '', content, dialogMode=digMode, containID=containID, crossref=crossref)

    else:
        last_content += content.strip()
        return content

def isSmartLinkTag(content):
    return utils.isSmartLinkTag(content2Tag(content), tag.get_list_smart_link(source2library(source)))

def isDirectLinkTag(content):
    return utils.isDirectLinkTag(content2Tag(content), tag.tag_list_direct_link)

def isAccountTag(content):
    return utils.isAccountTag(content, tag.tag_list_account)

def genSmartAgentLinkHtml(tag, ret, record, split_char, content):
    agentList = []
    if ret.find(split_char) != -1:
        agentList = ret.split(split_char)
    else:
        agentList = [ret]
    html = ''
    for agent in agentList:
        script = "agentRequest('" + agent + "', '" + record.get_id().strip() + "', '" + source + "');"
        html += '<a target="_blank" href="javascript:void(0);" onclick="' + script + '">' + agent + '</a>'
        if agent != agentList[len(agentList) -1]:
            html += split_char + '&nbsp;'

    return content[0 : content.find(':') + 1] + html


def genAccountHtml(tagStr, record, content, containID=''):
    if tag.tag_list_account.has_key(tagStr + ':'):
        url = tag.tag_list_account[tagStr + ':']
    else:
        url = utils.toQueryUrl(utils.getEnginUrl('glucky'), record.get_title().strip() + ' ' + tagStr)
    if url != '':
        ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : tagStr, 'library' : source2library(source)})
        dialogMode = False
        return genSmartLinkHtml(tagStr, ret, record, ',', url, content, urlFromServer=False, accountTag=True, containID=containID, dialogMode=dialogMode)
    else:
        return ''


def content2Tag(content):
    if content.find(':') != -1:
        return content[0 : content.find(':') + 1].strip()
    else:
        return content


def genSmartLinkHtml(tag, tag_content, record, split_char, url, content, urlFromServer=True, accountTag=False, dialogMode=False, containID='', crossref=False):
    global last_content
    ret = tag_content
    last_content = ret
    html = ''
    count = 0
    aid = ''
    originDialogMode = dialogMode
    remarkImg = ''
    if ret.find(split_char) != -1:
        ret = ret.split(split_char)
        lineLenCount = 0
        #print tag_content
        #print ret
        for i in ret:
            old_i = i.strip()
            #dialogMode = adjDialogMode(i.strip(), originDialogMode)
            #if i.find('(') != -1:
            #    print i + '<br>'
            #    print 'dialogMode:' + str(dialogMode) + '<br>' 
            if utils.getValueOrTextCheck(i):
                remarkImg = utils.getIconHtml('remark', width=10, height=8)
            else:
                remarkImg = ''
            #if Config.delete_from_char != '' and i.find(Config.delete_from_char) != -1:
            #    i = i[0 : i.find(Config.delete_from_char)].strip()
            lineLenCount += utils.getCutLen(tag, i.strip())
            if old_i == ret[0].strip():
                lineLenCount += len(tag)
            count += 1
            aid = containID + '-a-' + str(count)
            if crossref:
                #print i + '<br>'
                html += utils.genCrossrefHtml(record.get_id(), aid, tag, i, source, split_char=split_char)
                #if old_i != ret[len(ret) - 1].strip():
                #    split_char = '<br>'
                #    html += split_char
                #    continue
            else:
                sText = utils.getLinkShowText(accountTag, i.strip(), tag, len(ret), column_num=column_num)
                linkText = getLinkText(accountTag, i.strip(), sText)
                if url != '':
                    link = url
                    if url.find('%s') != -1:
                        link = utils.toAccountUrl(url, linkText.replace(' ', ''))
                    html += utils.enhancedLink(link, linkText, module='main', library=source, rid=record.get_id(), resourceType=tag, urlFromServer=urlFromServer, showText=utils.getLinkShowText(accountTag, i.strip(), tag, len(ret), column_num=column_num), dialogMode=dialogMode, aid=aid, originText=i.strip()) 
                else:
                    html += utils.enhancedLink(utils.bestMatchEnginUrl(linkText, resourceType=tag, source=record.get_url()), linkText, module='main', library=source, rid=record.get_id(), resourceType=tag, urlFromServer=urlFromServer, showText=utils.getLinkShowText(accountTag, i.strip(), tag, len(ret), column_num=column_num), dialogMode=dialogMode, aid=aid, originText=i.strip()) 

                html += remarkImg
            if old_i != ret[len(ret) - 1].strip():
                if accountTag:
                    html += '&nbsp;'
                else:
                    html += '<font color="blue"><i>' + split_char + '</i></font>' + '&nbsp;'

            if lineLenCount > course_name_len + course_name_len / 6:
                lineLenCount = 0
                html += '<br>'
            #dialogMode = originDialogMode

    else:
        #dialogMode = adjDialogMode(ret.strip(), originDialogMode)
        count = 1
        aid = containID + '-a-' + str(count)
        if utils.getValueOrTextCheck(ret):
            remarkImg = utils.getIconHtml('remark', width=10, height=8)
        else:
            remarkImg = ''
        if crossref:
            html += utils.genCrossrefHtml(record.get_id(), aid, tag, ret, source)
        else:
            sText = utils.getLinkShowText(accountTag, ret.strip(), tag, 1, column_num=column_num)
            linkText = getLinkText(accountTag, ret.strip(), sText)
            if url != '':
                link = url
                if url.find('%s') != -1:
                    link = utils.toAccountUrl(url, linkText)
                html += utils.enhancedLink(link, linkText, module='main', library=source, rid=record.get_id(), resourceType=tag, urlFromServer=urlFromServer, showText=sText, dialogMode=dialogMode, aid=aid, originText=ret.strip())
            else:
                html += utils.enhancedLink(utils.bestMatchEnginUrl(linkText, resourceType=tag, source=record.get_url()), linkText, module='main', library=source, rid=record.get_id(), resourceType=tag, urlFromServer=urlFromServer, showText=sText, dialogMode=dialogMode, aid=aid, originText=ret.strip())

            html += remarkImg
        #dialogMode = originDialogMode

    if accountTag and tag_content.find(split_char) != -1 and len(tag_content.split(split_char)) > Config.max_account_for_tag_batch_open:
        dialogMode = True
    return utils.genTagLink(content[ 0 :  content.find(':')].strip(), 'main', source, record.get_id(), tag, dialogMode, aid, crossref, accountTag) + html



def adjDialogMode(text, originDialogMode):

    if utils.getValueOrTextCheck(text):
        sText, value = utils.getValueOrTextSplit(text)
        #print 'stext:' + sText + ' value:' + value + ' ' + str(value.find('.') != -1) + '<br>' 
        if utils.isUrlFormat(value): # value is short link
            #print 'return False<br>'
            return False 

    return originDialogMode


def getLinkText(accountTag, text, showText):

    return utils.getValueOrText(text, returnType='value')
    '''
    if accountTag and tag.account_tag_alias.has_key(text):
        return tag.account_tag_alias[text]
    else:
        return text
    '''




def print_search_box(hiden):
    global search_box_displayed
    input_text = ''
    if html_style and search_box_displayed == False:
        search_box_displayed = True
        if plugins_mode == False:
            print '<br/>'
        else:
            input_text = source.replace('|', '').strip()
        onclick = "search('search_txt', 'select');"
        div = '<div style="text-align:center;width:100%;margin: 0px auto;' 
        if hiden:
            div += 'display: none;'
        #if plugins_mode:
        #    div += ' display:none;'
        div += '">'
	out = div + '<input id="search_txt" style="border-radius:5px;border:1px solid" maxlength="256" tabindex="1" size="46" name="word" autocomplete="off" type="text" value="' + input_text + '">&nbsp;&nbsp;' + genEnginOption("select", defaultEngin=Config.default_engin_searchbox) +\
              '&nbsp;&nbsp;<button alog-action="g-search-anwser" type="submit" id="search_btn" hidefocus="true" tabindex="2" onClick="' + onclick + '">Go</button>'
        if output_navigation_links:
               out += utils.genMoreEnginHtml("searchbox-a", utils.genMoreEnginScriptBox("searchbox-a", "searchbox_div", "search_txt"), '...', "searchbox_div") + '</div>' 
        else:
            out += '</div>' 
        print out

        if plugins_mode == False:
            for i in range(0, 1):
                print '<br/>'

def print_table_head_with_style():
    global gened_libary
    center_style = 'style="'
    if Config.center_content:
        width = '100%'
        background_color = '#FFFFFF'
        if column_num == '1':
            width = '75%'
            background_color = '#F6F3E5'
        if loadmore_mode == False:
            body = ''
            body += '<body  style="text-align:center; background-color:' + background_color + ';'
            if Config.backgrounds[Config.background] != '':
                body += 'background-image:url(' + Config.backgrounds[Config.background] + ');">'
            else:
                body += '">'
            print body
        center_style += 'margin:0px auto; background-color:#FFFFFF;  width:' + width + '; border:1; bordercolor=#000077;'
    else:
        if loadmore_mode == False:
            if Config.backgrounds[Config.background] != '':
                print '<body style="background-image:url(' + Config.backgrounds[Config.background] + ')">'
            else:
                print '<body>'
    center_style += 'margin-left:' + Config.content_margin_left + '; margin-top:' + Config.content_margin_top + ';'
    center_style += '"'
    if loadmore_mode == False and Config.distribution == False:
        print_search_box(search_box_hiden)
            
        if library_hiden == False and plugins_mode == False and gened_libary == False:
            if source.endswith('-library'):
                print utils.gen_libary(True,username, '', source=source)
            gened_libary = True
	if plugins_mode:
	    print '<br>'
        print '<div ' + center_style + ' >'
    center_style = ''
    if Config.center_content:
        if column_num == '1':
            center_style = 'style="margin-left:13px; background-color:#FFFFFF;"'
        else:
            center_style = 'style="margin:0px auto; background-color:#FFFFFF;"'
    if css_style_type == 3 or css_style_type == 4 or css_style_type == 5:
        print '<table class="easy-table easy-table-default coursesTable" ' + center_style + '>'
    else:
        print '<table class="table" ' + center_style + '>'

def print_table_footer():
    print "</table>"
    print '</div>'
    if loadmore_mode == False:
        print "</body>"

def get_space_cell(num, column_num):
    result = ""
    start = column_num - num
    end = start + num
    for i in range(start, end):
        result += get_space(0, line_id_max_len_list[i]) + vertical + get_space(0, cell_len - line_id_max_len_list[i] - 1)
        if num > 1 and i != num:
            result += vertical

    return result
def reset_max_len_list():
    global line_max_len_list, line_id_max_len_list
    line_max_len_list = [0, 0, 0]
    line_id_max_len_list = [0, 0, 0]

def includeDesc(keyword):
    for k in keyword_list:
        if keyword.find(k) != -1:
            return True
    return False

def getKeywordAndData(filter_keyword, line):
    data = ''
    for k in keyword_list:
        if filter_keyword.find(k) != -1:
            filter_keyword = filter_keyword.replace(k,'')
            args = { 'tag' : k , 'library' : source2library(source)} 
            ret = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', line, args)
            if ret != None:
                data += ret + ' '
    
    return filter_keyword, data

def containLogicalOperators(keyword):
    if keyword.find('#or') != -1 or keyword.find('#and') != -1 or keyword.find('#not') != -1:
        return True
    return False

def match(keyword, data, rid=''):
    if rid != '' and rid.find(keyword) != -1 and rid.strip().lower() != keyword.strip().lower():
        return False

    if data.lower().find(keyword.strip().lower()) != -1 or re.match(keyword.strip(), data) != None:
        return True
    return False

def isSpaceLine(line):
    newLine = line.replace(vertical, '').strip()
    if newLine == '':
        return True
    return False
    
def filter(keyword, data, rid=''):
    if containLogicalOperators(keyword):
        conditions = []
        if keyword.find('#not') != -1:
            conditions = keyword.split('#not')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data, rid=rid):
                    return False
            return True
        elif keyword.find('#and') != -1:
            conditions = keyword.split('#and')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data, rid=rid) == False:
                    return False
            return True
        elif keyword.find('#or') != -1:
            conditions = keyword.split('#or')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data, rid=rid):
                    return True
            return False
        
    return match(keyword, data)
    
def buildLine(content):
    return " id | " + content + " | | \n"

record_dict = {}
def getLines(file_name):
    global record_dict
    all_lines = []
    if os.path.exists(file_name):
        f = open(file_name,'rU')
        count = 0
        for line in f.readlines():
            if Config.hiden_parentid_record and line.find('parentid:') != -1:
                continue
            record = Record(line)
            if filter_keyword != "":
                
                data = record.get_id() + ' ' + record.get_title()
                keyword = filter_keyword

                if includeDesc(filter_keyword):
                    keyword, data = getKeywordAndData(filter_keyword, line)
                if record_dict.has_key(record.get_url().strip()) and record.get_url().strip() != '':
                    continue
                if filter(keyword, data, rid=record.get_id()):
                    count += 1
                    all_lines.append(enhancedRecord(file_name, record, count, True))
                    record_dict[record.get_url().strip()] = ""
            else:
                count += 1
                all_lines.append(enhancedRecord(file_name, record, count))
        f.close()

    return all_lines

def enhancedRecord(fileName, record, count, filter_mode=False):
    line = record.line

    if filter_mode:
        if record.get_describe().find('path:') == -1:
            line += ' path:' + fileName[fileName.find('db') :] 
        
    id = record.get_id().strip() 
    if id == '':
        id = 'custom-' + str(count)
        line = id + line
    
    if Config.hiden_record_id and record.get_describe().find('id:') == -1:
        line += ' id:' + id
    if fileName.find('exclusive') != -1:
        line += ' title:' + record.get_title().strip()

    if record.get_url().find(Config.ip_adress) != -1 and record.get_path() == '':
        url = record.get_url().strip()
        parts = url.split('&')
        path = ''
        for p in parts:
            if p.find('db=') != -1:
                path += p[p.find('db') : ].replace('db=', 'db/')
            if p.find('key=') != -1:
                path += p[p.find('key') : ].replace('key=', '')
        if path != '':
            line += ' path:' + path
    elif record.get_path() == '' and line.find('path:') == -1:
        line += ' path:' + fileName[fileName.find('db/') : ]

    if fileName.find('rank') != -1 and line.find('winner') == -1 and record.get_title().find(',') != -1:
        line += ' winner:' + record.get_title()
    
    title = record.get_title().strip()

    if Config.replace_with_smart_link:
        line = line[0 : line.find('|', line.find('|') + 1) + 1] + utils.bestMatchEnginUrl(title) + line[line.rfind('|') : ]

    if fileName.endswith('library') and record.get_title().find('(') != -1:
        line = formatTitle(title, '(', line)

    if Config.delete_from_char != '' and title.find(Config.delete_from_char) != -1:
        line = formatTitle(title, Config.delete_from_char, line, Config.delete_forward)

    return line

def formatTitle(title, char, line, deleteForward=True):
    new_title = ''
    if deleteForward:
        new_title = title[0 : title.find(char)].strip()
    else:
        new_title = title[title.find(char) + 1 :].strip()
    line = line[0 : line.find('|') + 1 ] + ' ' + new_title + ' ' + line[line.find('|', line.find('|') + 1) : ]
    return line



def getFileNameFromPath(path):
    fn = path
    while fn.find('/') != -1:
        fn = fn[fn.find('/') + 1 : ].strip()
    return fn

total_records = 0
current_page = 1
def print_list(all_lines, file_name = ''):
    global top_row, old_top_row, output_with_color, output_with_style, total_records
    current = 0
    old_line = ""
    old_line_2 = ""
    color_index = 0
    filter_keyword_2 = ''

    total_records = len(all_lines)

    if filter_keyword != '' and merger_result: 
        all_lines = utils.sortLines(all_lines)

    if Config.page_item_count > 0 and html_style and source.find('arxiv') == -1:
        start_item = (current_page - 1) * Config.page_item_count
        all_lines = all_lines[ start_item : start_item + Config.page_item_count]
        
    if html_style:
        if len(all_lines) == 1:# or file_name.find('paper') != -1:
            adjust_column_num('1')
        elif len(all_lines) == 2:
            adjust_column_num('2')
    
    if verify != '':
        file_name = verify

    if html_style == True and output_with_color:
        output_with_color = False
        output_with_style = True
    #print 'column_num:' + str(column_num)

    if len(all_lines) > 0:
        line_count = len(all_lines)
        if top_row > 0 and top_row > line_count:
            top_row = line_count
        else:
            top_row = old_top_row
        list_all = []
        reset_max_len_list()
 
        line_half = 0
        if column_num == "3":
            list_all.append([])
            list_all.append([])
            list_all.append([])
            if top_row > 0:
                if top_row % 3 == 0:
                    line_half = top_row / 3
                else:
                    if (top_row + 1) % 3 == 0:
                        line_half = (top_row + 1) / 3
                    else:
                        line_half = (top_row + 2) / 3
            else:
                line_half = line_count / 3
        elif column_num == "2":
            list_all.append([])
            list_all.append([])
            if top_row > 0:
                if top_row % 2 == 0:
                    line_half = top_row / 2
                else:
                    line_half = (top_row + 1) / 2
            else:
                line_half = line_count / 2
        elif column_num == "1":
            list_all.append([])
        
        for line in all_lines:
            current += 1

            line = utils.to_unicode(line)
            record = Record(line.replace("\n", ""))
            if column_num == "3":
                top = line_half + (line_count % 3)
                top2 = 2 * line_half + (line_count % 3)
                if top_row > 0:
                    top = line_half
                    top2 = 2 * line_half
                if current <= top:
                    update_max_len(record, 1)
                    list_all[0].append(record)
                elif current <= top2:
                    update_max_len(record, 2)
                    list_all[1].append(record)
                else:
                    update_max_len(record, 3)
                    list_all[2].append(record)

            elif column_num == "2":
                top = line_half + (line_count % 2)
                if top_row > 0:
                    top = line_half
                if current <= top:
                    update_max_len(record, 1)
                    list_all[0].append(record)
                else:
                    update_max_len(record, 2)
                    list_all[1].append(record)
            else:
                update_max_len(record, 1)
                list_all[0].append(record)

            if top_row > 0 and current >= top_row:
                break

        if column_num == "3":
            if len(list_all[0]) - len(list_all[1]) == 2:
                list_all[1].insert(0, list_all[0][len(list_all[0]) - 1])
                list_all[0].pop()
        #print list_all
        id_title_lines, describe_lines = build_lines(list_all, file_name)
        #print_search_box()
        #print id_title_lines
        #print describe_lines
        if column_num == "3":
            if html_style == False:
                print_table_head(3)
            else:
                getScript(file_name, list_all[0][0], total_records)
                print_table_head_with_style()
            for i in range(0, len(id_title_lines[2])):
                content = get_line(id_title_lines, 0, 3, i)
                if html_style == True:
                    content = gen_html_body(content, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True: 
                    for l in range(0, len(describe_lines)):
                        if html_style == True:
                            desc_line = get_line(describe_lines[l], 0, 3, i)
                            if isSpaceLine(desc_line) == False:
                                print gen_html_body_v2(desc_line, i, l)
                        else:
                            print get_line(describe_lines[l], 0, 3, i)

            if len(id_title_lines[0]) > len(id_title_lines[2]):
                last = len(id_title_lines[0]) - 1
                for last in range(len(id_title_lines[2]), len(id_title_lines[0])):
                    content = ""
                    if len(id_title_lines[0]) == len(id_title_lines[1]):
                        content = get_line(id_title_lines, 0, 2, last) + get_space_cell(1, 3) + vertical
                    else:
                        content = get_line(id_title_lines, 0, 1, last) + get_space_cell(2, 3) + vertical

                    if html_style == True:
                        content = gen_html_body(content, last)
                    if output_with_color == True:
                        print_with_color(content)
                    else:
                        print content
                    if output_with_describe == True:
                        for l in range(0, len(describe_lines)):
                            if len(id_title_lines[0]) == len(id_title_lines[1]):
                                if html_style == True:
                                    desc_line = get_line(describe_lines[l], 0, 2, last) + get_space_cell(1, 3) + vertical
                                    if isSpaceLine(desc_line) == False:
                                        print gen_html_body_v2(desc_line, last, l)
                                else:
                                    print get_line(describe_lines[l], 0, 2, last) + get_space_cell(1, 3) + vertical
                            else:
                                if html_style == True:
                                    desc_line = get_line(describe_lines[l], 0, 1, last) + get_space_cell(2, 3) + vertical
                                    if isSpaceLine(desc_line) == False:
                                        print gen_html_body_v2(desc_line, last, l)
                                else:
                                    print get_line(describe_lines[l], 0, 1, last) + get_space_cell(2, 3) + vertical

            if html_style == False:
                print_table_separator(3)
            else:
                print_table_footer();
                #print '</table>'
        elif column_num == "2":
            if html_style == False:
                print_table_head(2)
            else:
                getScript(file_name, list_all[0][0], total_records)
                print_table_head_with_style()
            for i in range(0, len(id_title_lines[1])):
                content = get_line(id_title_lines, 0, 2, i)
                if html_style == True:
                    content = gen_html_body(content, i)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:    
                    for l in range(0, len(describe_lines)):
                        if html_style == True:
                            desc_line = get_line(describe_lines[l], 0, 2, i)
                            if isSpaceLine(desc_line) == False:
                                print gen_html_body_v2(desc_line, i, l)
                        else:
                            print get_line(describe_lines[l], 0, 2, i)
            if len(id_title_lines[0]) > len(id_title_lines[1]):
                last = len(id_title_lines[0]) - 1
                content = get_line(id_title_lines, 0, 1, last) + get_space_cell(1, 2) + vertical
                if html_style == True:
                    content = gen_html_body(content, last)
                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        if html_style == True:
                            desc_line = get_line(describe_lines[l], 0, 1, last) + get_space_cell(1, 2) + vertical
                            if isSpaceLine(desc_line) == False:
                                print gen_html_body_v2(desc_line, last, l)
                        else:
                            print get_line(describe_lines[l], 0, 1, last) + get_space_cell(1, 2) + vertical

            if html_style == False:
                print_table_separator(2)
            else:
                print_table_footer()
                #print '</table>'
        elif column_num == '1':
            if html_style == False:
                print_table_head(1)
            else:
                getScript(file_name, list_all[0][0], total_records)
                print_table_head_with_style()
            for i in range(0, len(id_title_lines[0])):
                content = get_line(id_title_lines, 0, 1, i)
                if html_style == True:
                    content = gen_html_body(content, i)

                if output_with_color == True:
                    print_with_color(content)
                else:
                    print content
                if output_with_describe == True:
                    for l in range(0, len(describe_lines)):
                        if html_style == True:
                            desc_line = get_line(describe_lines[l], 0, 1, i)
                            if isSpaceLine(desc_line) == False:
                                print gen_html_body_v2(desc_line, i, l)
                        else:
                            print get_line(describe_lines[l], 0, 1, i)

            if html_style == False:
                print_table_separator(1)
            else:
                print_table_footer()
                #print '</table>'
  
       
        if current > 0 and Config.distribution == False:
            message = ''
            if html_style:
                message += '<div id="total-info"><br/>'
                if filter_keyword != "":
                    info = filter_keyword
                    if len(filter_keyword) > 20:
                        info = filter_keyword[0 : 20] + '..'
                    message += '\nTotal <font color="#999966">' + str(total_records) + "</font> records cotain " + info
                else:
                    message += '\nTotal <font color="#999966">' + str(total_records) + "</font> records"
            else:
                message += '\nTotal ' + str(total_records) + " records"
            if file_name != '':
                if html_style:
                    a = '<a target="_blank" href="' + getLibraryRealUrl(file_name) + '">' + file_name[file_name.rfind('/') + 1 :] + '</a>'
                    message += " in " + '<a target="_blank" href="http://github.com/'+ username + '">' + username +  "</a>' " + a + "\n\n"
                else:
                    message += ", File: " + file_name + "\n\n"
            else:
                message += "\n\n"

            if html_style:
                message += "<br/></div>"
                if loadmore_mode == False:
                    loadmore_div = ''
                    loadmore_div += '<div id="loadmore" style="' + 'margin-left:' + Config.content_margin_left + ';' + '"></div>'
                    message += loadmore_div
            if loadmore_mode:
                message = ''
            if plugins_mode == False:
                print message
                if html_style and Config.page_item_count > 0 and total_records > Config.page_item_count and source.find('arxiv') == -1:
                    total_pages = total_records / Config.page_item_count
                    if total_records % Config.page_item_count > 0:
                        total_pages += 1

                    print utils.gen_pages(current_page, total_pages, getLibraryRealUrl(file_name))
                
                if html_style and library_hiden == False:
                    print utils.gen_menu(source)
            
current_level = 1
level = 100

def getLibraryRealUrl(file_name):
    return 'http://' + Config.ip_adress + '/?db=' + file_name[file_name.find('/') + 1 : file_name.rfind('/') + 1] + '&key=' + file_name[file_name.rfind('/') + 1 :] + '&column=' + Config.column_num + '&width=' + Config.default_width


def notIncludeFile(item, fileNameNotContain):
    if fileNameNotContain == '':
        return False
    if fileNameNotContain.find('-') != -1:
        keywords = fileNameNotContain.split('-')
        for k in keywords:
            if item.find(k) != -1:
                return True
    elif item.find(fileNameNotContain) != -1:
        return True
    return False

def includeFile(item, fileNameFilter):
    #print item + ' ' + fileNameFilter
    if fileNameFilter.find('+') != -1:
        result = False
        for ft in fileNameFilter.split('+'):
            if ft != '' and item.find(ft) != -1:
                return True
        return result
    else:
        return item.find(fileNameFilter) != -1

def get_lines_from_dir(dir_name, fileNameFilter = ''):
    global current_level
    #print fileNameFilter
    current_level += 1
    cur_list = os.listdir(dir_name)
    all_lines = []
    fileNameNotContain = ''
    if fileNameFilter.find('#-') != -1:
        fileNameNotContain = fileNameFilter[fileNameFilter.find('#-') + 2 :]
        fileNameFilter = fileNameFilter[0 : fileNameFilter.find('#-')]

    if filter_keyword != '':
        if filter_keyword.find(':') != -1:
            cur_list = utils.find_file_by_pattern(filter_keyword[filter_keyword.find(':') + 1 :], os.getcwd() + '/' + dir_name)
        else:
            cur_list = utils.find_file_by_pattern(filter_keyword, os.getcwd() + '/' + dir_name)
        #print cur_list

    for item in cur_list:
        if item.startswith("."):
            continue
        if fileNameFilter != '' and includeFile(item, fileNameFilter) == False:
            continue
        if fileNameNotContain != "" and notIncludeFile(item, fileNameNotContain):
            continue
            

        full_path = os.path.join(dir_name, item)
        if os.path.isfile(full_path):
            for line in getLines(full_path):
                all_lines.append(line)
        else:
            if current_level >= level + 1:
                continue
            current_level = 1
            for line in get_lines_from_dir(full_path):
                all_lines.append(line)
    return all_lines

def print_dir(dir_name):
    global current_level, dir_mode
    dir_mode = True
    current_level += 1
    cur_list = os.listdir(dir_name)
    for item in cur_list:
        if item.startswith("."):
            continue

        full_path = os.path.join(dir_name, item)
        if os.path.isfile(full_path):
            print_list(getLines(full_path), full_path)
        else:
            if current_level >= level + 1:
                continue
            current_level = 1
            print_dir(full_path)

def adjust_cell_len():
    global custom_cell_len
    if column_num == '2':
        custom_cell_len = cell_len + (cell_len / 14)
    elif column_num == '3':
        custom_cell_len = int(cell_len * (2 / 3.0) + 7)
    elif column_num == '1':
        custom_cell_len = cell_len * 2

def adjust_link_number():
    global max_nav_link_row, max_links_row
    if column_num == '1':
        max_nav_link_row = max_nav_link_row * 2
    if column_num == '2':
        max_nav_link_row = (max_nav_link_row - 2) * 2
        #max_links_row = max_links_row - 1
    if column_num == '3':
        max_nav_link_row = max_nav_link_row + 1
        max_links_row = max_links_row - 2
    
def adjust_column_num(cn):
    global column_num
    column_num = cn
    adjust_cell_len()
    adjust_link_number()

def adjust_cell_row():
    global custom_cell_row 
    custom_cell_row = Config.custom_cell_row_list[int(column_num) - 1]
    #print int(custom_cell_row)

def source2library(source):
    if source.endswith('-library'):
        return source[source.rfind('/') + 1 :].strip()
    else:
        return source


def main(argv):
    global source, column_num,filter_keyword, output_with_color, output_with_describe, custom_cell_len, custom_cell_row, top_row, level, merger_result, old_top_row, engin, css_style_type, output_navigation_links, max_nav_links_row, verify, max_nav_link_row, database, plugins_mode, split_length, max_nav_link_row, loadmore_mode, search_box_hiden, library_hiden, username, current_page, trackmode, trackmode_engin_type, keyword_list
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hk:i:c:f:s:dw:r:t:l:mb:e:nv:u:apz:xy:o:q:', ["help", "keyword", "input", "column", "filter", "style", "describe", "width", "row", "top", "level", "merger", "border",\
                      "engin", "navigation", "verify", "use", "alexa", "plugins", 'loadmore', 'nosearchbox', 'username', 'page', 'tracemode'])
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
            column_num = a
            #print 'column_num:' + str(column_num)
            adjust_cell_len()
            adjust_link_number()
            adjust_cell_row()
        elif o in ('-f', '--filter'):
            filter_keyword = str(a).strip()
            #print filter_keyword
        elif o in ('-s', '--style'):
            output_with_color = True
            css_style_type = int(a)
        elif o in ('-d', '--describe'):
            output_with_describe = True
            adjust_cell_len()
            #output_with_color = True
        elif o in ('-w', '--width'):
            custom_cell_len = int(a) 
            split_length = custom_cell_len + 15
            #max_nav_link_row = 1000
        elif o in ('-r', '--row'):
            if int(a) > 0 and int(a) < 80:
                custom_cell_row = int(a)
            else:
                print 'the row must between 0 and 80'
        elif o in ('-t', '--top'):
            top_row = int(a)
            old_top_row = int(a)
        elif o in ('-l', '--level'):
            level = int(a)
        elif o in ('-m', '--merger'):
            merger_result = True
        elif o in ('-b', '--border'):
            chanage_border(a)
        elif o in ('-e', '--engin'):
            engin = str(a).strip()
            if utils.setEnginMode(engin):
                max_nav_links_row = 5
        elif o in ('-n', '--navigation'):
            output_navigation_links = True
        elif o in ('-v', '--verify'):
            verify = a
        elif o in ('-u', '--use'):
            database = a
        elif o in ('-a', '--alexa'):
            utils.loadAlexa()
        elif o in ('-p', '--plugins'):
            plugins_mode = True
        elif o in ('-z', '--loadmore'):
            loadmore_mode = True
        elif o in ('-y', '--username'):
            username = str(a)
        elif o in ('-x', '--nosearchbox'):
            search_box_hiden = True
            library_hiden = True
        elif o in ('-o', '--page'):
            current_page = int(a)
        elif o in ('-q', '--tracemode'):
            trackmode = True
            trackmode_engin_type = str(a)
            #print '---' + trackmode_engin_type

    if source.endswith('-library'):
        keyword_list = tag.get_tag_list(source2library(source))
        #print keyword_list

    
    if source.endswith('-library') and Config.auto_library_cell_len:
        adjust_column_num('3')
        custom_cell_len = 77
        split_length = custom_cell_len + 15


    if source == "":
        print "you must input the input file or dir"
        usage()
        return
    #if output_with_color == True:
    #    print "color"
    if source.lower().find(".pdf") != -1:
        os.system("open " + source)
        return
    if source.find('|') != -1:
        print_list([source])
    elif os.path.isfile(source):
        print_list(getLines(source), source)
    elif merger_result and os.path.isdir(source):
        print_list(get_lines_from_dir(source))
    elif os.path.isdir(source):
        print_dir(source)
    elif source.find('+') != -1:
        split = source.split('+')
        dirName = split[0]
        if dirName.startswith('db') == False:
            dirName = 'db/' + dirName
        print_list(get_lines_from_dir(dirName, source[source.find('+') + 1 :]))

if __name__ == '__main__':
    main(sys.argv)



