#!/usr/bin/env python

import sys
import networkx as nx
from networkx.readwrite import json_graph
sys.path.append("..")
from record import CourseRecord
import re
import json
from operator import itemgetter

#data_file = '../db/eecs/electrical-engineering-and-computer-science-mit2015'
#data_file = '../db/mathematics/mathematics-mit2015'
regex = re.compile(r'[0-9]+\.[0-9]+[a-z]*')

g = nx.DiGraph()
course_dict = {}
data_file_list = ['../db/eecs/electrical-engineering-and-computer-science-mit2015',\
                 # '../db/mathematics/mathematics-mit2015',\
                 # '../db/biology-life-sciences/biological-engineering-mit2015',\
                 # '../db/biology-life-sciences/biology-mit2015',\
                 # '../db/biology-life-sciences/computational-and-systems-biology-mit2015',\
                 # '../db/physics/physics-mit2015'\
                 ]

data_file_lines_list = []

for data_file in data_file_list:
    f = open(data_file,'rU')
    lines = f.readlines()
    data_file_lines_list.append(lines)
    node_type = data_file[data_file.find('db/') + 3:data_file.find('/', data_file.find('db/') + 3)]

    for line in lines:
        record = CourseRecord(line.strip())
        course_dict[record.get_id().strip()] = record.get_title()
        g.add_node(record.get_id().strip() + record.get_title(), name=record.get_id().strip() + record.get_title(), type=node_type)

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
                if course_dict.get(p, '') == '':
                    g.add_node(p, name=p, type='prep')
                    g.add_edge(record.get_id().strip() + record.get_title(), p)
                else:
                    g.add_edge(record.get_id().strip() + record.get_title(), p + course_dict.get(p))

                #prereq += p + ' '
            #print prereq
     
d = json_graph.node_link_data(g)
json.dump(d, open('force.json', 'w'))

print nx.info(g)
'''
def print_out_edges(g, node, level):
    if len(g.out_edges(node['name'])) > 0:
        print (2 * level  * " ") + str(node['name']).strip()
        for i in range(0, len(g.out_edges(node['name']))):
            print_out_edges(g, g.node[g.out_edges(node['name'])[i][1]], level + 2)
    else:
        print (2 * level * " ") + str(node['name']).strip()
    
print "Popular courses"
pop_list = sorted([(n,d) 
              for (n,d) in g.out_degree_iter()
                  if g.node[n]['type'] == 'eecs' ], \
             key=itemgetter(1), reverse=True)[:1]

for n in pop_list:
    print 'begin----'
    print_out_edges(g, g.node[n[0]], 0)
    print '----end'
'''
