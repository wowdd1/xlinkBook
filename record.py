#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08


class Record():
    r_id = ""
    title = ""
    utl = ""
    line = ""
    describe = ""
    default_line = " | | | "
    def __init__(self, line):
        self.line = line
        if line == "":
            self.line = self.default_line
    def get_default_line(self):
        return self.default_line

    def get_pos(self, pos):
        if pos == 1:
            return self.line.find('|')
        else:
            return self.line.find('|', self.get_pos(pos - 1) + 1)
        return -1 

    def get_id(self):
        return self.line[0 : self.get_pos(1)]

    def get_title(self):
        return self.line[self.get_pos(1) + 1 : self.get_pos(2)]

    def get_url(self):
        return self.line[self.get_pos(2) + 1 : self.get_pos(3)]

    def get_describe(self):
        return self.line[self.get_pos(3) + 1 : ]



#r = Record("id | title | url | describe")

#print r.get_id()
#print r.get_title()
#print r.get_describe()
#print r.get_url()
