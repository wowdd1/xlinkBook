#!/usr/bin/env python


from spider import *



class UstSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'ust'
        self.subs = {\
            'ACCT' : 'Accounting',\
            'ISOM' : 'Information Syst, Business Stats & Operations Mgmt',\
            'BIEN' : 'Bioengineering',\
            'LABU' : 'Language for Business',\
            'BMED' : 'Biomedical Engineering',\
            'LAGR' : 'Language for Environmental Issues',\
            'CENG' : 'Chemical and Biomolecular Engineering',\
            'LANG' : 'Language',\
            'CHEM' : 'Chemistry',\
            'LIFS' : 'Life Science',\
            'CIVL' : 'Civil and Environmental Engineering',\
            'MARK' : 'Marketing',\
            'COMP' : 'Computer Science and Engineering',\
            'MATH' : 'Mathematics',\
            'ECON' : 'Economics',\
            'MECH' : 'Mechanical Engineering',\
            'ELEC' : 'Electronic and Computer Engineering',\
            'MGMT' : 'Management',\
            'ENGG' : 'School of Engineering',\
            'PHYS' : 'Physics',\
            'ENTR' : 'Entrepreneurship',\
            'RMBI' : 'Risk Management and Business Intelligence',\
            'ENVR' : 'Environment',\
            'SBMT' : 'School of Business and Management',\
            'ENVS' : 'Environmental Science',\
            'SCED' : 'Science/IT Education',\
            'FINA' : 'Finance',\
            'SCIE' : 'School of Science',\
            'GBUS' : 'Global Business',\
            'SHSS' : 'School of Humanities and Social Science',\
            'GNED' : 'General Education',\
            'SISP' : 'Summer Institute for Secondary School Students',\
            'HART' : 'Studio Arts courses offered by HUMA',\
            'SOSC' : 'Social Science',\
            'HLTH' : 'Health and Physical Education',\
            'TEMG' : 'Technology and Management',\
            'HUMA' : 'Humanities',\
            'TYSP' : 'Talented Youth Summer Program',\
            'IELM' : 'Industrial Engineering and Logistics Management',\
            'UROP' : 'Undergraduate Research Opportunities Program',\
            'IROP' : 'International Research Opportunities Program',\
            'WBBA' : 'SF program in World Business'}

    def doWork(self):
        r = requests.get('http://publish.ust.hk/SISCourseCat/ShowUGSubjectList.aspx?WebSite=Production')
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a', 'code'):
            code = a.text.strip()
            if self.need_update_subject(self.subs[code]) == False:
                continue
            file_name = self.get_file_name(self.subs[code], self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0
            courses = {}
            for s in ['UG', 'PG']:
                url = 'http://publish.ust.hk/SISCourseCat/' + 'Show' + s + 'CourseList.aspx?Subject=' + code + '&WebSite=Production'
                print url
                r = requests.get(url)
                soup = BeautifulSoup(r.text)
                title = ''
                for tr in soup.find_all('tr'):
                    if tr.text.strip() == self.subs[code]:
                        continue
                    text = tr.text.replace('\n', '').strip()
                    if text.find('  ') != -1 and text.startswith(code):
                        data = text.split('  ')
                        course_num = data[0].replace(' ', '')
                        courses[course_num] = data[1].strip()
                        
                    if text.startswith(code):
                        title = courses[course_num]
                    elif title != '' and courses[course_num] != 'done':
                        print course_num + ' ' + title
                        self.count += 1
                        self.write_db(f, course_num, title, '', 'description:' + text)
                        courses[course_num] = 'done'

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"


start = UstSpider()
start.doWork()
