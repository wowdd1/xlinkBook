#!/usr/bin/env python
import os, sys
import getopt
import re
import mmap

# use this script for migrate data when record had moved form one file to another 
# not included library reocrd

source = ''
target = ''
id = ''

def needDelete(line, delete_lines):
    for dl in delete_lines:
        if line == dl:
            return True
    return False

def migrate(source, target, id):

    print 'migrate ' + source + ' to ' + target + ' id:' + id
    return
    if id.strip() == '':
        print 'id must provide'
        return

    if os.path.exists(source) and os.path.exists(target):
        source_f = open(source, 'rU')
        

        source_lines = source_f.readlines()
        migrate_data = []
        for source_line in source_lines:
            #print source_line
            if source_line.startswith(id):
                migrate_data.append(source_line)

        print migrate_data
        source_f.close()
        source_f = open(source, 'w')
        target_f = open(target, 'a')

        if len(migrate_data) > 0:
            for line in source_lines:
                if needDelete(line, migrate_data) == False:
                    
                    source_f.write(line)
        for line in migrate_data:
            print 'migrate line ' + line.strip()
            target_f.write(line)

        target_f.close()
        source_f.close()


    else:
        print 'source or target file not exists'

def getTargerFile(d, file_name):
    return d + '/data/' + file_name + '-' + d

def check(source, id, data):
    result_data = []
    for d in data:

        full_path = getTargerFile(d, source)
        if os.path.exists(full_path) == False:
            print  'file ' + full_path + ' not exists'
            continue 

        re_file = re.compile(id, re.I)
        with open(full_path, 'r+') as f:
            try:
                data = mmap.mmap(f.fileno(), 0)
                if re_file.search(data):
                    print 'found ' + id + ' in ' + full_path
                else:
                    continue
                    
            except Exception as e:
                print str(e) + full_path
                continue

        result_data.append(d)

    return result_data

def main(argv):
    global source, target, id
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:t:i:', ["source", "target", "id"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:
        if o in ('-i', '--id'):
            id = a
        if o in ('-s', '--source'):
            source = a
        if o in ('-t', '--target'):
            target = a

    check_data = ['reference', 'content', 'milestone']
    check_data = check(source, id, check_data)
    if len(check_data) > 0:
        for d in check_data:
            migrate(getTargerFile(d, source), getTargerFile(d, target), id)
    else:
        print 'no data need migrate'
    

if __name__ == '__main__':
    main(sys.argv)

