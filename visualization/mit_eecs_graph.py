#!/usr/bin/env python

import sys
import networkx as nx
from networkx.readwrite import json_graph
sys.path.append("..")
from record import CourseRecord
import re
import json

data_file = '../db/eecs/electrical-engineering-and-computer-science-mit2015'
regex = re.compile(r'[0-9]+\.[0-9]+[a-z]*')

f = open(data_file,'rU')
lines = f.readlines()
g = nx.DiGraph()
course_dict = {}

for line in lines:
    record = CourseRecord(line.strip())
    course_dict[record.get_id().strip()] = record.get_title()
    g.add_node(record.get_id().strip() + record.get_title())

print g.node.get('zhaodan','')
for line in lines:
    record = CourseRecord(line.strip())
    prereq_list = []
    if record.get_prereq() != None:
        print record.get_prereq()
        prereq_list = regex.findall(record.get_prereq().lower())

    if len(prereq_list) > 0:
        #prereq = 'prereq:'
        for p in prereq_list:
            if course_dict.get(p, '') == '':
                g.add_node(p)
                g.add_edge(record.get_id().strip() + record.get_title(), p)
            else:
                g.add_edge(record.get_id().strip() + record.get_title(), p + course_dict.get(p))

            #prereq += p + ' '
        #print prereq
     
d = json_graph.node_link_data(g)
json.dump(d, open('force.json', 'w'))

print nx.info(g)
