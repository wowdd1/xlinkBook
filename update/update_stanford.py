#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *
from update_stanford_online import StanfordOnlineSpider
sys.path.append("..")
from record import CourseRecord

class StanfordSpider(Spider):
    include_unoffered_courses = False
    
    video_lecture_list = {\
        'CS1U' : 'http://openclassroom.stanford.edu/MainFolder/CoursePage.php?course=PracticalUnix',\
        'CS101' : 'https://class.coursera.org/cs101-selfservice',\
        'CS106A' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=824a47e1-135f-4508-a5aa-866adcae1111',\
        'CS106B' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=11f4f422-5670-4b4c-889c-008262e09e4e',\
        #'CS107' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=2d712634-2bf1-4b55-9a3a-ca9d470755ee',\
        'CS143' : 'https://class.coursera.org/compilers-2012-002',\
        'CS145' : 'https://class.coursera.org/db',\
        'CS147' : 'http://openclassroom.stanford.edu/MainFolder/CoursePage.php?course=HCI',\
        'CS154' : 'https://class.coursera.org/automata-002',\
        'CS157' : 'https://class.coursera.org/intrologic-005',\
        'CS161' : 'http://openclassroom.stanford.edu/MainFolder/CoursePage.php?course=IntroToAlgorithms',\
        'CS183B' : 'https://class.coursera.org/startup-001',\
        'CS193G' : 'https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=384233322#ls=1',\
        'CS193P' : 'https://www.youtube.com/playlist?list=PLCCE29F69A864766F',\
        'CS223A' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=86cc8662-f6e4-43c3-a1be-b30d1d179743',\
        'CS224N' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=63480b48-8819-4efd-8412-263f1a472f5a',\
        'CS227B' : 'https://class.coursera.org/ggp-002',\
        'CS228' : 'https://class.coursera.org/pgm-003',\
        'CS229' : 'https://class.coursera.org/ml-004',\
        'CS246' : 'https://class.coursera.org/mmds-001',\
        'CS255' : 'https://class.coursera.org/crypto-008',\
        'CS264' : 'https://www.youtube.com/playlist?list=PLEGCF-WLh2RL8jsZpaf2tLHa5LotFEt5b',\
        'CS334A' : 'https://www.youtube.com/playlist?list=PL3940DD956CDF0622',\
        'CS545' : 'https://mvideos.stanford.edu/graduate#/SeminarDetail/Winter/2015/CS/545',\
        'CS547' : 'http://scpd.stanford.edu/free-learning/webinars/human-computer-interaction-seminar-series-2013/stanford-seminar-jure-leskovec',\
        'CS55N' : 'https://www.coursera.org/course/security',\
        'EE184' : 'http://www.youtube.com/playlist?list=PL9D558D49CA734A02',\
        'EE203' : 'https://mvideos.stanford.edu/graduate#/SeminarDetail/Winter/2015/EE/203',\
        'EE261' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=84d174c2-d74f-493d-92ae-c3f45c0ee091',\
        'EE263' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=17005383-19c6-49ed-9497-2ba8bfcfe5f6',\
        'EE363' : 'http://www.youtube.com/playlist?list=PL06960BA52D0DB32B',\
        'EE364A' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=2db7ced4-39d1-4fdb-90e8-364129597c87',\
        'EE364B' : 'http://see.stanford.edu/see/courseinfo.aspx?coll=523bbab2-dcc1-4b5a-b78f-4c9dc8c7cf7a',\
        'EE380' : 'https://www.youtube.com/playlist?list=PLpGHT1n4-mAuFqpRnQIbOakzLWMBd4M6G'\
    }
 
    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
        self.deep_mind = True
        stanfordOnlineSpider = StanfordOnlineSpider()
        self.course_name_dict = stanfordOnlineSpider.getCourseNameDict()

    def getRealUrl(self, course_num):
        test_url = 'http://' + course_num + '.stanford.edu'
        backup_url = "https://explorecourses.stanford.edu/search?q=" + course_num
        try:
            r = requests.get(test_url)
        except Exception , e:
            return backup_url
        
        if r.status_code == 200:
            return test_url
        else:
            return backup_url 

    def getDescriptionDict(self, subject):
        results = {}
        for line in open(self.get_file_name(subject, self.school),'rU').readlines():
            record = CourseRecord(line)
            results[record.get_id().strip()] = record.get_description().strip()
        return results

    def getVideoLectureList(self):
        return self.video_lecture_list

    def formatCourseTitle(self, title):
        if title.find('(') != -1:
            title = title[0 : title.find('(')]
        return title.strip()

    def processData(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        print "processing " + subject + " " + url

        from update_stanford_cs import StanfordCSSpider
        self.records_dict = StanfordCSSpider().getRecordsDict()
        r = requests.get(url)
        soup = BeautifulSoup(r.text); 
        course_num_list = []
        course_name_list = []
        course_description_list = []
        course_instructors_list = []

        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for span in soup.find_all("span", attrs={"class": "courseNumber"}):
            course_num_list.append(span.text[0:len(span.text) - 1].replace(' ', ''))

        for span in soup.find_all("span", attrs={"class": "courseTitle"}):
            course_name_list.append(span.text.strip().strip())

        for div in soup.find_all("div", attrs={"class": "courseDescription"}):
            course_description_list.append(div.text.strip()) 
        i = 0
        for div in soup.find_all("div", attrs={"class": "courseAttributes"}):
            i += 1
            if i % 2 == 0:
                if div.text.strip().lower().find('instructors:') == -1:
                    course_instructors_list.append('')
                    i -= 1
                    continue
                course_instructors_list.append(div.text.strip().replace('\n', '').replace('Instructors: ;', '').strip())

        for i in range(0, len(course_num_list)):
            print course_num_list[i] + " " + course_name_list[i]
            if subject == 'Computer Science' and self.records_dict.get(course_num_list[i], '') != '' \
                       and self.records_dict.get(course_num_list[i]).get_instructors().find('none listed') == -1:
                description = "instructors:" + self.records_dict.get(course_num_list[i]).get_instructors().strip() + ' '
                url = self.records_dict.get(course_num_list[i]).get_url().strip()
            else:
                description = "instructors:" + course_instructors_list[i] + ' '
                url = 'http://' + course_num_list[i] + '.stanford.edu'
                if self.deep_mind:
                    url = self.getRealUrl(course_num_list[i])
            if self.video_lecture_list.get(course_num_list[i], '') != '' or self.course_name_dict.get(self.formatCourseTitle(course_name_list[i]), '') != '':
                description +='features:Video lectures' + ' ' 
            description += 'description:' + course_description_list[i] + ' '

            self.write_db(f, course_num_list[i], course_name_list[i], url, description)
            self.count += 1

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        r = requests.get("https://explorecourses.stanford.edu/browse")
        soup = BeautifulSoup(r.text);
        for li in soup.find_all("li"):
            subject = ""
            if li.a.text.find("(") != -1:
                subject = li.a.text[0: li.a.text.find("(")].strip()
            else:
                subject = li.a.text.strip()
            
            url = "https://explorecourses.stanford.edu/" + str(li.a["href"]).replace("&filter-term-Winter=on", "").replace("search", "print") + "&descriptions=on"
            if self.include_unoffered_courses == True:
                url += "&filter-term-Winter=off&filter-term-Autumn=off&filter-term-Summer=off&filter-term-Spring=off"
            else:
                url += "&filter-term-Autumn=on&filter-term-Summer=on&filter-term-Spring=on&filter-term-Winter=on"
            self.processData(subject, url)

def main(argv):
    start = StanfordSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)
