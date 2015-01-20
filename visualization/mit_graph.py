#!/usr/bin/env python

import sys
import os
import networkx as nx
from networkx.readwrite import json_graph
sys.path.append("..")
from record import CourseRecord
import re
import json
from operator import itemgetter
import getopt

#data_file = '../db/eecs/electrical-engineering-and-computer-science-mit2015'
#data_file = '../db/mathematics/mathematics-mit2015'
regex = re.compile(r'[0-9]+\.[0-9]+[a-z]*')

g = nx.DiGraph()
course_dict = {}
data_file_list = ['../db/eecs/electrical-engineering-and-computer-science-mit2015',\
                  '../db/mathematics/mathematics-mit2015',\
                  '../db/biology-life-sciences/biological-engineering-mit2015',\
                  '../db/biology-life-sciences/biology-mit2015',\
                  '../db/biology-life-sciences/computational-and-systems-biology-mit2015',\
                  '../db/physics/physics-mit2015'\
                 ]

data_file_lines_list = []
sub_graph_node_list = []
course = ''
def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c, --course: the course number for computer graph'

def load_data(course):
    print 'generate graph for ' + course
    result_node_name = ''
    for data_file in data_file_list:
        f = open(data_file,'rU')
        lines = f.readlines()
        data_file_lines_list.append(lines)
        node_type = data_file[data_file.find('db/') + 3:data_file.find('/', data_file.find('db/') + 3)]

        for line in lines:
            record = CourseRecord(line.strip())
            course_dict[record.get_id().strip()] = (record.get_title(), record.get_url().strip())
            node_name = record.get_id().strip() + " " + record.get_title().strip()
            if record.get_id().strip() == course:
                result_node_name = node_name
            g.add_node(node_name, name=node_name, type=node_type)

    for lines in data_file_lines_list:
        for line in lines:
            record = CourseRecord(line.strip())
            prereq_list = []
            if record.get_prereq() != None:
                #print record.get_prereq()
                prereq_list = regex.findall(record.get_prereq().lower())

            if len(prereq_list) > 0:
                #prereq = 'prereq:'
                for p in prereq_list:
                    node_name = record.get_id().strip() + ' ' + record.get_title().strip()
                    if course_dict.get(p, '') == '':
                        g.add_node(p, name=p, type='prep')
                        g.add_edge(node_name, p)
                    else:
                        g.add_edge(node_name, p + ' ' + course_dict.get(p)[0].strip())

                    #prereq += p + ' '
                #print prereq
    return result_node_name


def gen_html_link(f, content, tu, level):
    if tu != None:
        f.write((2 * level  * "&nbsp;") + "<a href='" + tu[1] + "' onclick='window.open(this.href); return false'>" +content + '</a><br>')
    else:
        f.write((2 * level  * "&nbsp;") + content + '<br>')
    

def print_out_edges(f, g, node, level):
    sub_graph_node_list.append(node['name'])
    if len(g.out_edges(node['name'])) > 0:
        gen_html_link(f, str(node['name']).strip(), course_dict.get(node['name'][0 : node['name'].find(' ')]), level)
        #print (2 * level  * "&nbsp;") + str(node['name']).strip() + '<br>'
        for i in range(0, len(g.out_edges(node['name']))):
            print_out_edges(f, g, g.node[g.out_edges(node['name'])[i][1]], level + 2)
    else:
        gen_html_link(f, str(node['name']).strip(), course_dict.get(node['name'][0 : node['name'].find(' ')]), level)
        #print (2 * level * "&nbsp;") + str(node['name']).strip() + '<br>'

''' 
print "Popular courses"
pop_list = sorted([(n,d) 
              for (n,d) in g.out_degree_iter()
                  if g.node[n]['type'] == 'eecs' ], \
             key=itemgetter(1), reverse=True)[:1]

print pop_list[0]
'''

def main(argv):
    global course
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:', ["help","course"])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            course = a

    if course == '':
        print 'please input course number'
        return

    
    node_name = load_data(course)

    if node_name == '':
        print 'can not find data for ' + course
        return
    #print nx.info(g)

    f = open('remark.html', "w")
    print_out_edges(f, g, g.node[node_name], 0)
    f.close()
    sub_graph = g.subgraph(sub_graph_node_list)

    d = json_graph.node_link_data(sub_graph)
    json.dump(d, open('force.json', 'w'))

    print nx.info(sub_graph)

    os.system("open force.html") 

if __name__ == '__main__':
    main(sys.argv)
