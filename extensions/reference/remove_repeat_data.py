#!/usr/bin/env python

import os 
import sys
sys.path.append("../..")
from record import Record

files = os.listdir('data')
print files

for name in files:
    f = open('data/' + name)
    records = {}
    records_list = []
    lines = f.readlines()
    print name + ' before ' + str(len(lines))
    for line in lines:
        #print line.strip()
        r = Record(line.strip())
        if records.has_key(r.get_id().strip() + r.get_url().strip()) == False:
            records[r.get_id().strip() + r.get_url().strip()] = r
            records_list.append(r)
        else:
            for oldRecord in records_list:
                oldID = oldRecord.get_id().strip() + oldRecord.get_url().strip()
                newID = r.get_id().strip() + r.get_url().strip()
                if oldID == newID:
                    print oldID + ' == ' + newID
                    records_list.remove(oldRecord)
                    print 'line ' + oldRecord.line.strip() + ' will remove'
                    print 'new line ' + r.line.strip()
            records_list.append(r)
    f.close()
    f = open('data/' + name, 'w+')
    for record in records_list:
        f.write(record.line + '\n')

    f.close()
    print name + ' after ' + str(len(records_list))

