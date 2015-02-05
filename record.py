#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08


class Record():
    line = ""
    default_line = " | | | "
    def __init__(self, line):
        self.line = line
        if line == "":
            self.line = self.default_line
        self.file_path = ''

    def set_path(self, path):
        self.file_path = path

    def get_path(self):
        return self.file_path

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

class CourseRecord(Record):
    tag_prereq = 'prereq:'
    tag_project = 'project:'
    tag_university = 'university:'
    tag_available = 'available:'
    tag_level = 'level:'
    tag_features = 'features:'
    tag_instructors = 'instructors:'
    tag_description = 'description:'
    tag_textbook = 'textbook:'
    
    tag_list = [tag_prereq, tag_project, tag_university, tag_available, tag_level, tag_features, tag_instructors, tag_description, tag_textbook]

    describe = ''
    def __init__(self, line):
        Record.__init__(self, line)
        self.describe = self.get_describe()

    def next_tag_pos(self, pos, max_pos):
        min_pos = 1000
        for t in self.tag_list:
            next_pos = self.describe.lower().find(t, pos + 1)
            if next_pos != -1:
                if max_pos:
                    return next_pos
                elif next_pos < min_pos:
                    min_pos = next_pos

        if min_pos != 1000:
            return min_pos
        else:
            return -1

    def get_tag_content(self, tag, max_pos = False):
        start_pos = self.describe.lower().find(tag)
        if start_pos != -1:
            end_pos = self.next_tag_pos(start_pos, max_pos)
            if end_pos != -1:
                return self.describe[start_pos + len(tag) : end_pos].strip()
            else:
                return self.describe[start_pos + len(tag) : ]

        return None

    def get_prereq(self):
        return self.get_tag_content(self.tag_prereq)

    def get_project(self):
        return self.get_tag_content(self.tag_project)

    def get_university(self):
        return self.get_tag_content(self.tag_university)

    def get_available(self):
        return self.get_tag_content(self.tag_available)

    def get_level(self):
        return self.get_tag_content(self.tag_level)

    def get_features(self):
        return self.get_tag_content(self.tag_features)
    def get_instructors(self):
        return self.get_tag_content(self.tag_instructors)
    def get_description(self):
        return self.get_tag_content(self.tag_description)

    def get_textbook(self):
        content = self.get_tag_content(self.tag_textbook, True)
        if content != None:
            return content.replace(self.tag_textbook, '')
        return content


'''
r = CourseRecord('id | title | url | prereq:prereqxxx project:projectxxx university:universityxxx available:availablexxx level:levelxxx features:featuresxxx instructors:instructorsxxx textbook:textbook111 textbook:textbook222 description:descriptionxxx')

print r.get_prereq()
print r.get_project()
print r.get_university()
print r.get_available()
print r.get_level()
print r.get_features()
print r.get_instructors()
print r.get_description()
print r.get_textbook()
'''

#r = Record("id | title | url | describe")

#print r.get_id()
#print r.get_title()
#print r.get_describe()
#print r.get_url()
