#!/usr/bin/env python

from utils import Utils
import os
from record import PaperRecord
#f = open('db/eecs/papers/arxiv/', 'rU')

files = os.listdir('db/eecs/papers/arxiv/')
all_lines = []
for f in files:
    if f.find('-inc') != -1:
        continue
    print f
    f = open('db/eecs/papers/arxiv/' + f, 'rU' )

    all_lines.extend(f.readlines())
    f.close()

    print len(all_lines)



print all_lines[0]
print all_lines[1000]

#all_lines = all_lines[17400 : 18300]
utils = Utils()
all_lines = utils.sortLines(all_lines)
print all_lines[0]
print all_lines[1]
#print all_lines[18299]


last = -1
count = 0
setp_size = 300
for i in range(len(all_lines), -setp_size, -setp_size):
    if last != -1:
        print str(i) + '-' + str(last)
        count += 300
        f = open('db/eecs/papers/new/arxiv' + str(count) + "-arxiv2016", 'w') 
        lines = []
        lines = all_lines[i : last]
        print len(lines)
        count_line = 0
        for line in lines:
            count_line += 1
            #print count_line
            record = PaperRecord(line)
            url = record.get_url()
            if url.find('v', url.find('org')) != -1:
                url = url[0 : url.rfind('v')]
            rawid = url[url.rfind('/') + 1 : ].strip().replace('.','-')
            
            f.write('arxiv-' + rawid + " | " + record.get_title().strip() + " | " + url  + " | " + record.get_describe().strip() + "\n")
        f.close()
    last = i
    if i < 0:
        break
       
