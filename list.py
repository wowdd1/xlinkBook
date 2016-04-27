#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import getopt
import time
import re
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from record import Record, Tag
from utils import Utils
import copy

source = ""
filter_keyword = ""
column_num = "2"

custom_cell_len = 88
custom_cell_row = 5
cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=10
color_index=0
output_with_color = False
output_with_style = False
output_with_describe = False
output_navigation_links = False
merger_result = False
top_row = 0
old_top_row = 0
max_links_row = 9
max_nav_link_row = 12
max_nav_links_row = 8
default_links_row = 2

utils = Utils()
line_max_len_list = [0, 0, 0]
line_id_max_len_list = [0, 0, 0]

tag = Tag()
keyword_list = tag.tag_list

plus = '+'
subtraction = '-'
vertical = '|'
html_style = False
css_style_type = 0

engin = ''

div_content_list = []

gen_html_done = False

script_head = '<script language="JavaScript" type="text/JavaScript">';
script = '\
function setText(objN){\
    var clicktext=document.getElementById(objN);\
    if (clicktext.innerText == "..."){\
        clicktext.innerText="less";\
    } else {\
	clicktext.innerText="...";\
    }\
    clicktext.style.color="#999966";\
}\
function showdiv(targetid,objN){\
      var target=document.getElementById(targetid);\
      var clicktext=document.getElementById(objN);\
            if (clicktext.innerText=="less"){\
                target.style.display="";\
            } else {\
                target.style.display="none";\
            }\
}\
function search(inputid,optionid){\
    var input = document.getElementById(inputid);\
    var select = document.getElementById(optionid);\
    console.log("xx",input.value);\
    console.log("",select.value);\
    window.open(select.value + input.value);\
}\
function trimStr(str){return str.replace(/(^\s*)|(\s*$)/g,"");}\
function searchTopic(obj, topic){\
    console.log("xx",obj.text);\
    console.log("xx",topic);\
    var options = document.getElementsByTagName("option");\
    for(var i=0;i<options.length;i++){\
        if (trimStr(options[i].text) == trimStr(obj.text)) {\
            console.log("xx", options[i].value);\
            if (trimStr(options[i].text) == "arxiv" || trimStr(options[i].text) == "doaj" || trimStr(options[i].text) == "ust.hk"){\
                window.open(options[i].value.replace("$", topic.replace("&nbsp;", " ")));\
            } else {\
                window.open(options[i].value + topic.replace("&nbsp;", " "));\
            }\
        }\
    }\
}\
function navTopic(obj, divID, parentDivID, countIndex){\
    var targetid = divID + "-" + obj.text;\
    var target=document.getElementById(targetid);\
    for (var i = 0; i < countIndex + 1; i++) {\
        var parentDiv = document.getElementById(parentDivID + i.toString());\
        var children = parentDiv.children;\
        for (var j = 0, len = children.length; j < len; j++) {\
            children[j].style.color="#888888";\
            children[j].style.fontSize="9pt";\
        }\
    }\
    obj.style.color="#822312";\
    obj.style.fontSize="12pt";\
    if (target.style.display == ""){\
        target.style.display="none";\
    } else {\
        target.style.display="";\
    }\
}\
function showdiv_2(targetid){\
      var target=document.getElementById(targetid);\
            if (target.style.display=="none"){\
                target.style.display="";\
            } else {\
                target.style.display="none";\
            }\
}\
function hidendiv_2(targetid){\
      var target=document.getElementById(targetid);\
                target.style.display="none";\
}\
function appendContent(targetid, topic){\
    var target=document.getElementById(targetid);\
    target.innerHTML = array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic);\
}'
script_end = '</script>'

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

def color_keyword(text):
    result = text
    for k in keyword_list:
        if (color_index - 1) % 2 == 0:
            if html_style == True:
                result = result.replace(k, '<font color="#33EE22">' + k + '</font>')
            else:
                result = result.replace(k, utils.getColorStr('brown', k))
        else:
            if html_style == True:
                result = result.replace(k, '<font color="#66CCFF">' + k + '</font>')
            else:
                result = result.replace(k, utils.getColorStr('darkcyan', k))

    return result

def align_id_title(record):
    course_num = record.get_id()
    course_name = record.get_title()
    if utils.str_block_width(course_name) > course_name_len:
        course_name = course_name[0 : course_name_len - 3 ] + "..."
    else:
        course_name = course_name + get_space(0, course_name_len - utils.str_block_width(course_name))

    if len(course_num) < course_num_len:
        space = get_space(0, course_num_len - len(course_num))
        return course_num + space + vertical + course_name
    else:
        return course_num + vertical + course_name

def align_describe(describe):
    if utils.str_block_width(describe) > course_name_len - 1 and output_with_describe == False:
        describe = describe[0 : course_name_len - 3 ] + "..."
    else:
        describe += get_space(0, course_name_len - utils.str_block_width(describe))
    return get_space(0, course_num_len) + vertical + describe

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
    return (end - start) * " "

def get_id_and_title(record):
    return record.get_id() + vertical + record.get_title()

def update_max_len(record, col):
    if utils.str_block_width(get_id_and_title(record)) > line_max_len_list[col - 1]:
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
    course_name_len = cell_len - course_num_len - 1

def next_pos(text, start):
    min_end = len(text)
    for k in keyword_list:
        end = text.lower().find(k, start + 2)
        if end != -1 and end < min_end:
            min_end = end

    if min_end != len(text):
        min_end -= 1
        if min_end - start > course_name_len:
            return start + course_name_len
        else:
            return min_end

    if (len(text) - start) < course_name_len:
        return start + len(text) - start
    else:
        return start + course_name_len

def genEnginOption(selectid):

    option = ''
    engin_list = utils.getAllEnginList()
    option = '<select id="' + selectid +'">'
    for e in engin_list:
        option += '<option value ="' + utils.getEnginUrl(e) + '">' + e + '</option>'
    option += '</select>'
    return option

def getScript():
    global script
    print "<head>"
    print script_head
    if len(div_content_list) > 0:
        print "var array = []; "
        for content in div_content_list:
            print "array.push('" + content + "');" 
        
    print script
    print script_end
        
    if output_with_style:
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

def build_lines(list_all):
    global div_link_content, gen_html_done;
    id_title_lines = copy.deepcopy(list_all)
    describe_lines = []
    engin_list = []
    if engin != '':
        engin_list = utils.getEnginList(engin.strip())
    if len(engin_list) > default_links_row:
        row = len(engin_list) / max_links_row
        if len(engin_list) % max_links_row > 0:
            row += 1
        if row == 0:
            row = 1
        
        border_style_five(row)
    title = ''
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
            if html_style == False or (list_all[i][j].get_url().strip() == '' and engin == ''):
                id_title_lines[i][j] = align_id_title(list_all[i][j])
            else:
                id_title = align_id_title(list_all[i][j])
                url = list_all[i][j].get_url()
                title = id_title[id_title.find('|') + 1 : ]
                if html_style and title.find('(') != -1 and title.strip().startswith('(') == False:
                    title = title[0 : title.find('(')].strip()
                id = id_title[0 : id_title.find('|')].strip()
                
                if url.strip() != '':
                    id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + '<a href="' + url + '" target="_blank">' + title + '</a>'
                
                if url.strip() != '':
                    id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + '<a href="' + url + '" target="_blank">' + title.strip() + '</a>'
                else:
                    id_title_lines[i][j] = id_title[0: id_title.find('|') + 1] + title.strip()
                if engin != '':
                    engin_list_dict = utils.getEnginListLinks(engin_list, '#topic', id, engin.strip())#, '#33EE22')

            describe = utils.str_block_width(list_all[i][j].get_describe())
            start = 0
            end = 0
            if output_with_describe or html_style:
                lij = ''
                lines = len(describe_lines)
                linkID = ''
                content_divID = ''
                script = ''
                engin_content = ''
                nav_link_content = ''
                nav_links_content = ''
                
                for l in range(0, lines):

		    if html_style:
                        describe_lines[l][i][j] = align_describe('')
                        if engin != '' and engin_list_dict != '':
                            engin_list_dive = []
                            engin_list_sub = engin_list[default_links_row :]

                            ijl = str(i) + str(j) + str(l)

                            if l == 0:
                                linkID = 'a-' + ijl;
                                script += "setText('" + linkID +"');"
                                content_divID = "div-" + ijl
                                script += "showdiv('" + content_divID + "', '" + linkID +"');"
                                script += "appendContent('" + content_divID + "', '" + title.strip().replace(' ', '%20')+ "');"
                            if output_with_describe:
                                script += "showdiv('tr-" + ijl[1:] + "', '" + linkID +"');"
                                script += "showdiv('td-div-" + ijl + "', '" + linkID +"');"
                            if gen_html_done == False:

                                if (l+1) * max_links_row < len(engin_list_sub):
                                    engin_list_dive = engin_list_sub[l * max_links_row : (l+1) * max_links_row]
                                else:
                                    engin_list_dive = engin_list_sub[l * max_links_row :]
                                if len(engin_list_dive) == 0:
                                    describe_lines[l][i][j] = align_describe('')
                                else:
                                    describe_lines[l][i][j] = '#' + '#'.join(engin_list_dive)
                                if describe_lines[l][i][j].find('#') != -1:
                                    describe_lines[l][i][j] = describe_lines[l][i][j][0 : describe_lines[l][i][j].find('|') + 1] + \
                                                      '<div id="#div-star-' + str(l) +'" >' + describe_lines[l][i][j][describe_lines[l][i][j].find('|') + 1 : ] + '</div>'
                                    for (k, v) in engin_list_dict.items():
                                        describe_lines[l][i][j] = describe_lines[l][i][j].replace('#' + k.strip(), v)
                                    engin_content = describe_lines[l][i][j].replace('|', '').strip().replace("'","")
                                    div_content_list.append(engin_content)
                                describe_lines[l][i][j] = ''
                                if l == lines - 1 and output_navigation_links:
                                    navLinks = utils.getNavLinkList()
                                    content = ''
                                    hidenScript = ''
                                    for link2 in navLinks:
                                        hidenScript += 'hidendiv_2("' + '#div-' + link2 + '");'
                                    count = 0
                                    count_index = 0
                                    nav_div_id = ''
                                    for link in navLinks:
                                        nav_div_id = "#div-nav-" + str(count_index)
                                        divID = '#div'
                                        content += utils.genLinkWithScript2(hidenScript + 'navTopic(this,\"' + divID + '\",\"' + '#div-nav-' + '\",' + str(len(navLinks) / max_nav_link_row) + ');', link, '#888888', 9)
                                        count += 1 
                                        if count >= max_nav_link_row:
                                            div_content_list.append('<div id="' + nav_div_id + '">')
                                            div_content_list.append(content)
                                            div_content_list.append('</div>')
                                            count_index += 1
                                            count = 0
                                            content = '' 
                                    if content != '':
                                        div_content_list.append('<div id="' + nav_div_id + '">')
                                        div_content_list.append(content)
                                        div_content_list.append('</div>')
                                    for link in navLinks:
                                        divID = '#div-' + link
                                        div_content_list.append(utils.getDescDivs(divID, link, title, max_nav_links_row, 'searchTopic(this,"' + "#topic" + '");', '#822312', 15, 
                                                                '#131612', 12))
                                if l == lines - 1:
                                    gen_html_done = True


                    if end >= describe:
                        if html_style == False:
                            describe_lines[l][i][j] = align_describe("")
                        continue
                    end = next_pos(list_all[i][j].get_describe(), start) 
                    if output_with_describe:
                        describe_lines[l][i][j] = align_describe(list_all[i][j].get_describe()[start : end])
                    start = end
                count = 0
                
                if html_style: 
                    for e in utils.getEnginList('d:default'):
                        id_title_lines[i][j] += utils.getEnginHtmlLink(e, title)
                        count += 1
                        if count == default_links_row:
                            break
                    if script != '':
                        id_title_lines[i][j] += utils.genLinkWithScript(linkID, script, '...');
                        id_title_lines[i][j] += "<div id='" + content_divID + "'></div>";
            elif engin != '' and html_style and engin_list_dict != '':
                for (k, v) in engin_list_dict.items():
                    id_title_lines[i][j] += v
            

    return id_title_lines, describe_lines


def get_line(lines, start, end, j):
    result = vertical
    for i in range(start, end):
        result += color_keyword(lines[i][j]) + vertical

    return result

def gen_html_body(content, row=0):
    style = 'info'
    if row % 2 == 0:
        style = ''
    
    index = 0
    if vertical == '|': 
        verticals = []
        if column_num == "2":
            verticals = ['<tr class="' + style + '"><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td></tr>']   
        elif column_num == "3":
            verticals = ['<tr class="' + style + '"><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td></tr>']   
        elif column_num == "1":
            verticals = ['<tr class="' + style + '"><td style="vertical-align:top;">', '</td><td style="vertical-align:top;">', '</td></tr>']   

        while content.find(vertical) != -1:
            content = content[0 :content.find(vertical)] + verticals[index] + content[content.find(vertical) + 1:]
            index = index + 1

    return content


def gen_html_body_v2(content, row, subRow):
    style = 'info'
    if row % 2 == 0:
        style = ''
    index = 0
    tr_id = "tr-" + str(row) + str(subRow)
    td_div_id = str(row) + str(subRow)
    if vertical == '|':
        verticals = []
        if column_num == "2":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td>', '</td><td><div id="td-div-0' + td_div_id + '" style="display: none;">', '</div></td><td>', '</td><td><div id="td-div-1' + td_div_id + '" style="display: none;">', '</div></td></tr>']
        elif column_num == "3":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td>', '</td><td><div id="td-div-0' + td_div_id + '" style="display: none;">', '</div></td><td>', '</td><td><div id="td-div-1' + td_div_id + '" style="display: none;">', '</div></td><td>', '</td><td><div id="td-div-2' + td_div_id + '" style="display: none;">', '</div></td></tr>']
        elif column_num == "1":
            verticals = ['<tr class="' + style + '" id="' + tr_id + '" style="display: none;"><td>', '</td><td><div id="td-div-0' + td_div_id + '" style="display: none;">', '</div></td></tr>']

        while content.find(vertical) != -1:
            content = content[0 :content.find(vertical)] + verticals[index] + content[content.find(vertical) + 1:]
            index = index + 1

    return content

def print_search_box():
    if html_style:
        print '<br/>'
        onclick = "search('search_txt', 'select');"
        print '<div style="width:778px;margin:auto;"><input id="search_txt" maxlength="256" tabindex="1" size="46" name="word" autocomplete="off">&nbsp;&nbsp;' + genEnginOption("select") +\
              '&nbsp;&nbsp;<button alog-action="g-search-anwser" type="submit" id="search_btn" hidefocus="true" tabindex="2" onClick="' + onclick + '">search</button></div>'
        for i in range(0, 1):
            print '<br/>'

def print_table_head_with_style():
    if css_style_type == 3 or css_style_type == 4 or css_style_type == 5:
        print '<table class="easy-table easy-table-default coursesTable">'
    else:
        print '<table class="table">'

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
            da = utils.reflection_call('record', 'CourseRecord', 'get_' + k[0 : len(k) - 1], line)
            if da != None:
                data += da + ' '
    
    return filter_keyword, data

def containLogicalOperators(keyword):
    if keyword.find('#or') != -1 or keyword.find('#and') != -1 or keyword.find('#not') != -1:
        return True
    return False

def match(keyword, data):
    if data.lower().find(keyword.strip().lower()) != -1 or re.match(keyword.strip(), data) != None:
        return True
    return False

def isSpaceLine(line):
    newLine = line.replace(vertical, '').strip()
    if newLine == '':
        return True
    return False
    
def filter(keyword, data):
    if containLogicalOperators(keyword):
        conditions = []
        if keyword.find('#not') != -1:
            conditions = keyword.split('#not')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data):
                    return False

        if keyword.find('#and') != -1:
            conditions = keyword.split('#and')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data) == False:
                    return False
            return True

        if keyword.find('#or') != -1:
            conditions = keyword.split('#or')
            for con in conditions:
                if con.strip() == '':
                    continue
                if match(con, data):
                    return True
        
    return match(keyword, data)
    
def buildLine(content):
    return " id | xx" + content + " | | \n"

def getLines(file_name):
    all_lines = []
    if os.path.exists(file_name):
        f = open(file_name,'rU')
        all_lines = f.readlines()
        if filter_keyword != "":
            filter_result = []
            for line in all_lines:
                record = Record(line)
                data = record.get_id() + record.get_title()
                keyword = filter_keyword
                if includeDesc(filter_keyword):
                    keyword, data = getKeywordAndData(filter_keyword, line)

                if filter(keyword, data):
                    filter_result.append(line)
            all_lines = filter_result[:]
    return all_lines

def print_list(all_lines, file_name = ''):
    current = 0
    old_line = ""
    old_line_2 = ""
    color_index = 0
    filter_keyword_2 = ''
    global top_row, old_top_row, output_with_color, output_with_style
    if html_style == True and output_with_color:
        output_with_color = False
        output_with_style = True

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
        id_title_lines, describe_lines = build_lines(list_all)
        print_search_box()
        #print id_title_lines
        if column_num == "3":
            if html_style == False:
                print_table_head(3)
            else:
                getScript()
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
                print '</table>'
        elif column_num == "2":
            if html_style == False:
                print_table_head(2)
            else:
                getScript()
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
                print '</table>'
        elif column_num == '1':
            if html_style == False:
                print_table_head(1)
            else:
                getScript()
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
                print '</table>'
  

        if current > 0:
            message = ''
            if filter_keyword != "":
                message = "\nTotal " + str(current) + " records cotain " + filter_keyword
            else:
                message = "\nTotal " + str(current) + " records"
            if file_name != '':
                message += ", File: " + file_name + "\n\n"
            else:
                message += "\n\n"
            print message
            
current_level = 1
level = 100
def get_lines_from_dir(dir_name, fileNameFilter = '', fileNameNotContain=''):
    global current_level
    current_level += 1
    cur_list = os.listdir(dir_name)
    all_lines = []
    for item in cur_list:
        if item.startswith("."):
            continue
        if fileNameFilter != '' and item.find(fileNameFilter) == -1:
            continue
        if fileNameNotContain != "" and item.find(fileNameNotContain) != -1:
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
    global current_level
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

def main(argv):
    global source, column_num,filter_keyword, output_with_color, output_with_describe, custom_cell_len, custom_cell_row, top_row, level, merger_result, old_top_row, engin, css_style_type, output_navigation_links
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hk:i:c:f:s:dw:r:t:l:mb:e:n', ["help", "keyword", "input", "column", "filter", "style", "describe", "width", "row", "top", "level", "merger", "border",\
                      "engin", "navigation"])
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
            adjust_cell_len()
        elif o in ('-f', '--filter'):
            filter_keyword = str(a).strip()
        elif o in ('-s', '--style'):
            output_with_color = True
            css_style_type = int(a)
        elif o in ('-d', '--describe'):
            output_with_describe = True
            adjust_cell_len()
            #output_with_color = True
        elif o in ('-w', '--width'):
            custom_cell_len = int(a) 
        elif o in ('-r', '--row'):
            if int(a) > 0 and int(a) < 30:
                custom_cell_row = int(a)
            else:
                print 'the row must between 0 and 30'
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
        elif o in ('-n', '--navigation'):
            output_navigation_links = True


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
        print_list(getLines(source), source)
    elif merger_result and os.path.isdir(source):
        print_list(get_lines_from_dir(source))
    elif os.path.isdir(source):
        print_dir(source)
    elif source.find('#') != -1:
        split = source.split('#')
        dirName = split[0]
        if dirName.startswith('db') == False:
            dirName = 'db/' + dirName
        if len(split) == 2:
            print_list(get_lines_from_dir(dirName, split[1]))
        elif len(split) == 3:
            print_list(get_lines_from_dir(dirName, split[1], split[2]))

if __name__ == '__main__':
    main(sys.argv)



