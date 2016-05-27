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
        if line.find('|') == -1:
            self.line =  " | " + line.replace('\n', '') + " | | "
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
        return self.line[self.get_pos(3) + 1 : ].replace('|', '')

class Category():
    def __init__(self):
        self.book = "book"
        self.journal = "journal"
        self.paper = "paper"
        self.course = "course"
        self.project = "project"
        self.slide = "slide"
        self.code = "code"
        self.dataset = "dataset"
        self.patent = "patent"
        self.people = "people"
        self.blog = "blog"
        self.rank = "rank"
        self.website = "website"
        self.engin = "engin"

    def match(self, desc, category):
        index = desc.find('category:')
        if index != -1 and desc.find(category, index + 1) != -1:
            print category + ' match'
            return True
        print  category + ' not match ' + desc
        return False

    def containMatch(self, key, category):
        if key.find(category) != -1:
            print category + ' match'
            return True
        return False

class Tag():
    def __init__(self):
        self.tag_videourl = 'videourl:'
        self.tag_author = 'author:'
        self.tag_ratings = 'ratings:'
        self.tag_term = 'term:'
        self.tag_prereq = 'prereq:'
        self.tag_toprepo = 'toprepo:'
        self.tag_project = 'project:'
        self.tag_university = 'university:'
        self.tag_available = 'available:'
        self.tag_level = 'level:'
        self.tag_features = 'features:'
        self.tag_instructors = 'instructors:'
        self.tag_description = 'description:'
        self.tag_textbook = 'textbook:'
        self.tag_paper = 'paper:'
        self.tag_homepage = 'homepage:'
        self.tag_organization = 'organization:'
        self.tag_platform = 'platform:'
        self.tag_specialization = 'specialization:'
        self.tag_journal = "journal:"

        self.tag_priority = "priority:"
        self.tag_parentid = "parentid:"
       
        self.tag_category = "category:"
        self.tag_summary = "summary:"
        self.tag_published = "published:"
        self.tag_version = "version:"

        self.tag_list = [self.tag_videourl, self.tag_author, self.tag_ratings, self.tag_term, self.tag_prereq, self.tag_toprepo, self.tag_project, self.tag_university,\
                         self.tag_available, self.tag_level, self.tag_features, self.tag_instructors, self.tag_description, self.tag_textbook, self.tag_paper, self.tag_homepage,\
                         self.tag_organization, self.tag_platform, self.tag_specialization, self.tag_journal, self.tag_priority, self.tag_parentid, self.tag_category, self.tag_summary, self.tag_published, self.tag_version]

        self.tag_list_short = ["d:"]


class WrapRecord(Record):

    describe = ''
    def __init__(self, line):
        Record.__init__(self, line)
        self.describe = self.get_describe()
        self.tag = Tag()

    def next_tag_pos(self, pos, max_pos):
        min_pos = 1000
        for t in self.tag.tag_list:
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

class CategoryRecord(WrapRecord):
    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_category(self):
        return self.get_tag_content(self.tag.tag_category)

class PaperRecord(WrapRecord):
    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_author(self):
        return self.get_tag_content(self.tag.tag_author)

    def get_category(self):
        return self.get_tag_content(self.tag.tag_category)

    def get_summary(self):
        return self.get_tag_content(self.tag.tag_summary)

    def get_published(self):
        return self.get_tag_content(self.tag.tag_published)

    def get_version(self):
        return self.get_tag_content(self.tag.tag_version)



class PriorityRecord(WrapRecord):

    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_priority(self):
        return self.get_tag_content(self.tag.tag_priority)


class ReferenceRecord(PriorityRecord):
    def __init__(self, line):
        PriorityRecord.__init__(self, line)

class ContentRecord(PriorityRecord):
    def __init__(self, line):
        PriorityRecord.__init__(self, line)

    def get_parentid(self):
        return self.get_tag_content(self.tag.tag_parentid)


class CourseRecord(PriorityRecord):

    def __init__(self, line):
        PriorityRecord.__init__(self, line)

    def get_videourl(self):
        return self.get_tag_content(self.tag.tag_videourl)

    def get_author(self):
        return self.get_tag_content(self.tag.tag_author)

    def get_ratings(self):
        return self.get_tag_content(self.tag.tag_ratings)

    def get_term(self):
        return self.get_tag_content(self.tag.tag_term)

    def get_prereq(self):
        return self.get_tag_content(self.tag.tag_prereq)

    def get_toprepo(self):
        return self.get_tag_content(self.tag.tag_toprepo)

    def get_project(self):
        return self.get_tag_content(self.tag.tag_project)

    def get_university(self):
        return self.get_tag_content(self.tag.tag_university)

    def get_available(self):
        return self.get_tag_content(self.tag.tag_available)

    def get_level(self):
        return self.get_tag_content(self.tag.tag_level)

    def get_features(self):
        return self.get_tag_content(self.tag.tag_features)

    def get_instructors(self):
        return self.get_tag_content(self.tag.tag_instructors)

    def get_description(self):
        return self.get_tag_content(self.tag.tag_description)

    def get_textbook(self):
        content = self.get_tag_content(self.tag.tag_textbook, True)
        if content != None:
            return content.replace(self.tag.tag_textbook, '')
        return content

    def get_paper(self):
        return self.get_tag_content(self.tag.tag_paper)

    def get_homepage(self):
        return self.get_tag_content(self.tag.tag_homepage)

    def get_organization(self):
        return self.get_tag_content(self.tag.tag_organization)

    def get_platform(self):
        return self.get_tag_content(self.tag.tag_platform)

    def get_specialization(self):
        return self.get_tag_content(self.tag.tag_specialization)
   
    def get_journal(self):
        return self.get_tag_content(self.tag.tag_journal)



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
