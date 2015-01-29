#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
sys.path.append("..")
from record import CourseRecord

class BerkeleyCatalogSpider(Spider):
    

    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.subject = "eecs"
    
    
    def processBerkeleyData(self, course_dict, url, prefix):
        if self.need_update_subject(self.subject) == False:
            return
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        pre_line = ""
        for p in soup.find_all('p'):
            try:
                if p.b != None and pre_line != p.b.text[0: p.b.text.find(".")]:
                    pre_line = p.b.text[0: p.b.text.find(".")]
                    course_num = prefix + p.b.text[0: p.b.text.find(".")]
                    course_name = p.b.text[p.b.text.find(".") + 1 : p.b.text.find(".", p.b.text.find(".") + 1)].strip()
                    #print course_num + " " + course_name
                    instructors = ''
                    description = ''
                    prereq = ''
                    all_line = p.text.strip().split('\n')
                    for i in range(0, len(all_line)):
                        if i != 0 and len(all_line[i]) > 90 and all_line[i].startswith('Prerequisites:') == False:
                            description = 'description:' + all_line[i] + ' '
                        if all_line[i].startswith('Prerequisites:'):
                            prereq = 'prereq:' + all_line[i].replace('Prerequisites:', '').replace('.','').strip() + ' '
                        if i == len(all_line) - 1 and all_line[i].startswith('(') == False and len(all_line[i]) < 90:
                            instructors = 'instructors:' + all_line[i] + ' '
                    if instructors != '':
                        description = instructors + description
                    if prereq != '':
                        description = prereq + description
                    course_dict[course_num] = CourseRecord(self.get_storage_format(course_num, course_name, '', description)) 
            except Exception , e:
                print e
    
    def getCourseDict(self, subject_list):
        #berkeley
        print "downloading berkeley catalog course info"
        course_dict = {}
        for subject in subject_list:
            if subject == 'Computer Science':
                self.processBerkeleyData(course_dict, "http://general-catalog.berkeley.edu/catalog/gcc_list_crse_req?p_dept_name=Computer+Science&p_dept_cd=COMPSCI&p_path=l", "CS")
            if subject == 'Electrical Engineering':
                self.processBerkeleyData(course_dict, "http://general-catalog.berkeley.edu/catalog/gcc_list_crse_req?p_dept_name=Electrical+Engineering&p_dept_cd=EL+ENG&p_path=l", "EE")
      
        return course_dict


