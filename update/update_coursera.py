#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *


class CourseraSpider(Spider):
    sessions = []
    universities = []
    instructors = []
    course_specialization = {}

    def __init__(self):
        Spider.__init__(self)    
        self.school = "coursera"
        self.category = self.category_obj.course
        
    #coursera
    def loopJobj(self, url, dataList):
        r = requests.get(url);
        jobj = json.loads(r.text)
        for item in jobj.items()[0][1]:
            dataList.append(item)

    def initList(self):
        url = "https://api.coursera.org/api/catalog.v1/sessions?fields=id,courseId,homeLink,status,active,durationString,startDay,startMonth,startYear,name,signatureTrackCloseTime,signatureTrackOpenTime,signatureTrackPrice,signatureTrackPrice,eligibleForCertificates,eligibleForSignatureTrack,certificateDescription,certificatesReady"
                
        self.loopJobj(url, self.sessions)

        url = "https://api.coursera.org/api/catalog.v1/universities?fields=id,name,description,homeLink,website,websiteTwitter,websiteFacebook,websiteYoutube"
        self.loopJobj(url, self.universities)
       

        url = "https://api.coursera.org/api/catalog.v1/instructors?fields=fullName,title,department,website,websiteTwitter,websiteFacebook,websiteLinkedin,websiteGplus,shortName" 
        self.loopJobj(url, self.instructors)

    def initCourseSpecialization(self):
        r = requests.get('https://www.coursera.org/maestro/api/specialization/list?currency=USD')
        jobj = json.loads(r.text)
        for specialization in jobj:
            for course in specialization['topics']:
                self.course_specialization[str(course['id'])] = specialization['name']

    def getInstructorName(self, instructorIds):
        name = ""
        for instructor in self.instructors:
            for instructorId in instructorIds:
                if instructor['id'] == instructorId:
                    name += instructor['firstName'] + " " + instructor['lastName'] + ","
        if name[len(name) -  1 : ] == ",":
            name = name[0 : len(name) - 1]
        return name

    def getUniversitieName(self, universityIds):
        name = ""
        for universitie in self.universities:
            for universityId in universityIds:
                if universitie['id'] == universityId:
                    name += universitie['name'] + ","
        if name[len(name) -  1 : ] == ",":
            name = name[0 : len(name) - 1]
        return name

    def getSessionLinkAndStatus(self, sessionIds, slug): 
        session_id_dict = {}
        for session in self.sessions:
            for sessionId in sessionIds:
                if session['id'] == sessionId and session['active'] == True:
                    session_id_dict[sessionId] = session['homeLink']
        if len(session_id_dict.keys()) > 0:
            return session_id_dict[sorted(session_id_dict.keys())[len(session_id_dict.keys()) - 1]], True

        return "https://www.coursera.org/course/" + slug, False
    
    def getCategoryUrl(self, subjectId):
        return "https://api.coursera.org/api/catalog.v1/categories?id=" + str(subjectId) + "&includes=courses"
    
    def getCourseraOnlineCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        r = requests.get(url)
        jobj = json.loads(r.text)
        ids = ""
        for courseObj in jobj.items()[1][1]['courses']:
            ids += str(courseObj['id']) + ","

        url = "https://api.coursera.org/api/catalog.v1/courses?ids=" + ids[0 : len(ids) - 1] + "&fields=id,shortName,name,language,previewLink,shortDescription,instructor&includes=sessions,instructors,universities,categories"

        r = requests.get(url)
        print url
        jobj = json.loads(r.text)

        file_name = self.get_file_name(subject.strip(), self.school)
        if file_name.find('/eecs/') != -1:
            file_name = file_name.replace('/eecs/', '/eecs/' + self.school + '/')
        print "subject " + subject.strip() + " ----> " + file_name
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        count = 0

        for courseObj in jobj.items()[0][1]:
            url = ''
            active = ''
            if courseObj['links'].has_key('sessions'):
                url, active = self.getSessionLinkAndStatus(courseObj['links']['sessions'], courseObj['shortName'])
            remark = ""
            session_id = ""
            if active == True:
                remark = "available:yes "
                session_id = url[url.find("org/") + 4 : ].replace("/", "")
                url = url + "lecture"
            else:
                remark = "available:no "
                session_id = courseObj['shortName']

            remark += 'university:' + self.getUniversitieName(courseObj['links']['universities']) + ' '
            if self.getInstructorName(courseObj['links'].get('instructors', '')) != '':
                remark += "instructors:" + self.getInstructorName(courseObj['links'].get('instructors',"")) + ' '
            if self.course_specialization.get(str(courseObj['id']), '') != '':
                remark += 'specialization:' + self.course_specialization[str(courseObj['id'])] + ' '

            title = courseObj['name'].strip()
            print session_id + " " + title + " " + url
            remark += 'description:' + self.delZh(courseObj['shortDescription'])
            self.write_db(f, session_id, title, url, remark.replace("\n", "" ).strip()) 
            count += 1

        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        print "downloading coursera course info"
    
        print "loading data..."
        self.initList()
        self.initCourseSpecialization()

        r = requests.get("https://api.coursera.org/api/catalog.v1/categories") 
        jobj = json.loads(r.text)
        for k, v in jobj.items():
            if k == "elements":
                for subject in v:
                    self.getCourseraOnlineCourse(subject['name'], self.getCategoryUrl(subject['id']))
   

start = CourseraSpider()
start.doWork() 
