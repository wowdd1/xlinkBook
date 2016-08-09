#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
from update_harvard_online import HarvardOnlineSpider
sys.path.append("..")
from utils import Utils
import time

class HarvardSpider(Spider):    
    #harvard
    course_dict = {}

    dept_dict = {"AAAS" : "African & African Amer Studies",\
       "AMER" : "American Studies",\
       "ANTH" : "Anthropology",\
       "COMPSE" : "Applied Computation",\
       "APMA" : "Applied Mathematics",\
       "APPHYS" : "Applied Physics",\
       "URBP" : "Arch, Landscape & Urban Plan",\
       "ARCH" : "Architecture",\
       "ASTR" : "Astronomy",\
       "BSDM" : "Bio Sciences in Dental Med",\
       "BSPH" : "Bio Sciences in Public Health",\
       "DBS" : "Biological Science",\
       "BME" : "Biomedical Engineering",\
       "BIPH" : "Biophysics",\
       "BIST" : "Biostatistics",\
       "BIO" : "Biostatistics",\
       "CELT" : "Celtic Languages & Literatures",\
       "HSPH" : "Chan School of Public Health",\
       "CHPB" : "Chemical & Physical Biology",\
       "CHBI" : "Chemical Biology",\
       "CHEM" : "Chemistry & Chemical Biology",\
       "CLAS" : "Classics, The",\
       "CPLT" : "Comparative Literature",\
       "CS" : "Computer Science",\
       "CORE" : "Core Curriculum",\
       "HDS" : "Divinity School",\
       "DRPH" : "Doctor of Public Health",\
       "E&PS" : "Earth & Planetary Sciences",\
       "EALC" : "East Asian Langs & Civ",\
       "ECON" : "Economics",\
       "EDU" : "Education",\
       "ENGSCI" : "Engineering Sciences",\
       "ENGH" : "English",\
       "ESPP" : "Envi Science & Public Policy",\
       "EH" : "Environmental Health",\
       "EPI" : "Epidemiology",\
       "EMR" : "Ethnicity, Migration, Rights",\
       "CES" : "European Studies",\
       "EXPO" : "Expository Writing",\
       "FOLK" : "Folklore & Mythology",\
       "FRSP" : "Freshman Seminars",\
       "GENED" : "General Education",\
       "GCD" : "Genetics & Complex Diseases",\
       "GERM" : "Germanic Languages & Lit",\
       "GLOBHLTH" : "Global Health & Health Policy",\
       "GHP" : "Global Health & Population",\
       "GOVM" : "Government",\
       "GSD" : "Graduate School of Design",\
       "HGSE" : "Graduate School of Education",\
       "GOV" : "HKS Government",\
       "HPOL" : "Health Policy",\
       "HPM" : "Health Policy & Management",\
       "HIST" : "History",\
       "HLIT" : "History & Literature",\
       "HAA" : "History of Art & Architecture",\
       "HSCI" : "History of Science",\
       "HSEM" : "House Seminars",\
       "HEB" : "Human Evolutionary Biology",\
       "HUM" : "Humanities",\
       "IID" : "Immunology Infectious Disease",\
       "LAND" : "Landscape Architecture",\
       "LSCI" : "Life Sciences",\
       "LING" : "Linguistics",\
       "MATH" : "Mathematics",\
       "MDSC" : "Medical Sciences",\
       "MDST" : "Medieval Studies",\
       "MEST" : "Middle Eastern Studies",\
       "MBB" : "Mind, Brain & Behavior",\
       "MCB" : "Molecular & Cellular Biology",\
       "MUSC" : "Music",\
       "NELC" : "Near Eastern Languages & Civ",\
       "NEURO" : "Neurobiology",\
       "NODEPT" : "No Department",\
       "NUT" : "Nutrition",\
       "BIOE" : "Organismic & Evolutionary Biol",\
       "PHIL" : "Philosophy",\
       "PSCI" : "Physical Sciences",\
       "PHYS" : "Physics",\
       "PHS" : "Population Health Sciences",\
       "PSYC" : "Psychology",\
       "RSEA" : "Regional Studies-East Asia",\
       "RELG" : "Religion, The Study of",\
       "ROML" : "Romance Languages & Lit",\
       "REECA" : "Russia, E Europe, Central Asia",\
       "SANS" : "Sanskrit & Indian Studies",\
       "SLAV" : "Slavic Languages & Literatures",\
       "SBS" : "Social & Behavioral Sciences",\
       "SPOL" : "Social Policy",\
       "SOST" : "Social Studies",\
       "SHDH" : "Society, Human Dev & Health",\
       "SHH" : "Society, Human Dev & Health",\
       "SOCL" : "Sociology",\
       "SAST" : "South Asian Studies",\
       "SPCN" : "Special Concentrations",\
       "STAT" : "Statistics",\
       "SCRB" : "Stem Cell & Regenerative Biol",\
       "SBIO" : "Systems Biology",\
       "DRAM" : "Theater, Dance & Media",\
       "UKRA" : "Ukrainian Studies",\
       "URBAN" : "Urban Planning & Design",\
       "VES" : "Visual & Environmental Studies",\
       "WMGS" : "Women, Gender & Sexuality"}
    term_dict = {\
        "2166" : "2016 Summer",\
        "2168" : "2016 Fall"}
        #"2172" : "2017 Spring",
        #"2178" : "2017 Fall",
        #"2182" : "2018 Spring",
        #"2188" : "2018 Fall",
        #"2192" : "2019 Spring"


    def __init__(self):
        Spider.__init__(self)
        self.school = "harvard"
        self.url = "http://www.registrar.fas.harvard.edu"
        self.harvardOnlineSpider = HarvardOnlineSpider()
        self.utils = Utils()
    '''
    def formatCourseNum(self, subject, oldTitle):
        title = oldTitle[0 : oldTitle.find(".")]
        if title.find("(") != -1:
            title = title[0 : title.find("(")].strip()
        title = title.replace("*", "").replace("[", "")
        if title.find(subject) != -1:
            course_num = title[len(subject) : ].strip()
            if subject.find(" ") != -1:
                words = re.compile("[A-Za-z]+").findall(subject) 
                pre = ""
                for word in words:
                    pre += word[0 : 1]
                return pre + course_num
            else:
                return subject + course_num
        return title

    def getHarvardCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        sys.setrecursionlimit(3000)
        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0 
        online_course_dict = self.harvardOnlineSpider.getCourseDict(subject) 
        print len(online_course_dict)
        print "\n\nprocessing " + subject + " html and write data to file..."
        for p in soup.find_all("p"):
            if p != None:
                prereq = ''
                instructors = ''
                course_num = ''
                title = ''
                description = ''
                term = ''
                link = ''
                if p.strong != None and p.strong.a != None:
                    link = p.strong.a['href']
                for line in p.text.split('\n'):
                    if line.strip() != '' and line.startswith('Copyright') == False and line.startswith('.') == False and\
                        line.startswith('Catalog Number') == False:
                        line = line.replace("\n", '')
                        #print line
                        if line.find(subject) != -1 and line.find(subject) < 5:
                            course_num = self.formatCourseNum(subject, line)
                            title = line[line.find(".") + 2:].replace("]", "")
                            continue
                        if line.startswith('Half course'):
                            term = 'term:' + line + ' '
                            continue
                        if line.startswith('Prerequisite'):
                            prereq = 'prereq:' + line.replace("Prerequisite:", '').strip() + ' '
                            continue
                        if (len(line.strip()) > 40 and line.find('(' + subject + ')') == -1) or line.startswith('Note:'):
                            description = 'description:' + line + ' '
                            continue
                        instructors = 'instructors: ' + line + ' ' 


                description = instructors + prereq + term + description
                if course_num == '':
                    continue
                self.course_dict[course_num] = title
                self.count += 1
                if online_course_dict.get(course_num, '') != '':
                    description = 'features:Video lectures ' + description
                    if online_course_dict[course_num].get_url() != '':
                        link = online_course_dict[course_num].get_url()
                print course_num + ' ' + title + ' ' + link
                self.write_db(f, course_num, title, link, description)                      

        for node in soup.find_all("strong"):
            text = ""
            link = ""
            description = ''
            if node.string == None:
                if node.a != None and node.a.string != None:
                    text = node.a.string.replace("\n", "")
                    link = node.a["href"]
                else:
                    if node.a != None:
                        link = node.a["href"]
                    text = node.prettify()
                    if text.find("href=") > 0 :
                        text = text[text.find(">", 8) + 1 : text.find("<", text.find(">", 8)) - 1]
                    else:
                        text = text[text.find(">", 2) + 1 : text.find("<", 8) - 1]
                    text = text.replace("\n", "").strip()
            else:
                text = node.string.replace("\n", "")

            course_num = self.formatCourseNum(subject, text) 
            if self.course_dict.get(course_num, '') == '':
                title = text[text.find(".") + 2:].replace("]", "")
                self.count += 1
                if online_course_dict.get(course_num, '') != '':
                    description = 'features:Video lectures ' + online_course_dict[course_num].get_description()
                    if online_course_dict[course_num].get_url() != '':
                        link = online_course_dict[course_num].get_url()
                print course_num + ' ' + title + ' ' + link
                self.write_db(f, course_num, title, link, description)

        if self.count == 0:
            print subject + " can not get the data, check the html and python code"
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def doWork(self): 
        print "downloading harvard course info"
        r = requests.get("http://www.registrar.fas.harvard.edu/courses-exams/courses-instruction")
        soup = BeautifulSoup(r.text)
    
        for span in soup.find_all("span", class_="field-content"):
            #print span.a.string
            self.getHarvardCourse(span.a.string, self.url + str(span.a["href"]))
    '''

    def getUrlByYear(self, year):
        if year == 2016:
            return '%2C%22PageSize%22%3A%22%22%2C%22SortOrder%22%3A%5B%22IS_SCL_SUBJ_CAT%22%2C%22IS_SCL_SUBJ_CAT%22%5D%2C%22Facets%22%3A%5B%5D%2C%22Category%22%3A%22HU_SCL_SCHEDULED_BRACKETED_COURSES%22%2C%22SearchPropertiesInResults%22%3Atrue%2C%22FacetsInResults%22%3Atrue%2C%22SaveRecent%22%3Afalse%2C%22TopN%22%3A%22%22%2C%22SearchText%22%3A%22(STRM%3A2166%20%7C%20STRM%3A2168)%20(ACAD_ORG%3A%5C%22%s%5C%22)%22%2C%22DeepLink%22%3Afalse%7D'
        elif year == 2017:
            return '%2C%22PageSize%22%3A%22%22%2C%22SortOrder%22%3A%5B%22IS_SCL_SUBJ_CAT%22%2C%22IS_SCL_SUBJ_CAT%22%5D%2C%22Facets%22%3A%5B%5D%2C%22Category%22%3A%22HU_SCL_SCHEDULED_BRACKETED_COURSES%22%2C%22SearchPropertiesInResults%22%3Atrue%2C%22FacetsInResults%22%3Atrue%2C%22SaveRecent%22%3Afalse%2C%22TopN%22%3A%22%22%2C%22SearchText%22%3A%22(STRM%3A2172%20%7C%20STRM%3A2178)%20(ACAD_ORG%3A%5C%22%s%5C%22)%22%2C%22DeepLink%22%3Afalse%7D'
        elif year == 2018:
            return '%2C%22PageSize%22%3A%22%22%2C%22SortOrder%22%3A%5B%22IS_SCL_SUBJ_CAT%22%2C%22IS_SCL_SUBJ_CAT%22%5D%2C%22Facets%22%3A%5B%5D%2C%22Category%22%3A%22HU_SCL_SCHEDULED_BRACKETED_COURSES%22%2C%22SearchPropertiesInResults%22%3Atrue%2C%22FacetsInResults%22%3Atrue%2C%22SaveRecent%22%3Afalse%2C%22TopN%22%3A%22%22%2C%22SearchText%22%3A%22(STRM%3A2182%20%7C%20STRM%3A2188)%20(ACAD_ORG%3A%5C%22%s%5C%22)%22%2C%22DeepLink%22%3Afalse%7D'
        elif year == 2019:
            return '%2C%22PageSize%22%3A%22%22%2C%22SortOrder%22%3A%5B%22IS_SCL_SUBJ_CAT%22%2C%22IS_SCL_SUBJ_CAT%22%5D%2C%22Facets%22%3A%5B%5D%2C%22Category%22%3A%22HU_SCL_SCHEDULED_BRACKETED_COURSES%22%2C%22SearchPropertiesInResults%22%3Atrue%2C%22FacetsInResults%22%3Atrue%2C%22SaveRecent%22%3Afalse%2C%22TopN%22%3A%22%22%2C%22SearchText%22%3A%22(STRM%3A2166%20%7C%20STRM%3A2168)%20(ACAD_ORG%3A%5C%22%s%5C%22)%22%2C%22DeepLink%22%3Afalse%7D'

        return ''

    def doWork(self):
        url_part1 = "https://courses.my.harvard.edu/psc/courses/EMPLOYEE/EMPL/s/WEBLIB_IS_SCL.ISCRIPT1.FieldFormula.IScript_Search?SearchReqJSON={%22PageNumber%22%3A"
        year = int(time.strftime('%Y',time.localtime(time.time())))
        url_part2 = self.getUrlByYear(year)
        for k, v in self.dept_dict.items():
            if self.need_update_subject(v) == False:
                continue
            file_name = self.get_file_name(v, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            print 'processing ' + v
            page = 0
            courseid_dict = {}

            while True:
                page += 1
                url = url_part1 + str(page) +url_part2.replace('%s', k)
                print url
                r = requests.get(url)
                jobj = json.loads(r.text)
                search_ok = False
                for obj in jobj[0]['ResultsCollection']:
                    search_ok = True
                    dept = obj['IS_SCL_DESCR_IS_SCL_DESCRD'].strip().lower()
                    if dept != v.strip().lower():
                        print dept + ' not match ' + v.strip().lower()
                        continue
                    if obj.has_key('IS_SCL_DESCR_IS_SCL_DESCRH') and 'Not Offered' == obj['IS_SCL_DESCR_IS_SCL_DESCRH']:
                        continue
                    if courseid_dict.has_key(obj['CRSE_ID']):
                        continue
                    else:
                        courseid_dict[obj['CRSE_ID']] = ''

                    title = obj['Title']
                    term = 'term:' + obj['IS_SCL_DESCR_IS_SCL_DESCRH']
                    instructors = "instructors:"
                    description = "description:"

                    print obj['Title'] + ' ' + obj['IS_SCL_DESCR_IS_SCL_DESCRH']
                    if obj.has_key('DESCRLONG_DETAILS'):
                        for author in obj['DESCRLONG_DETAILS']:
                            instructors += author['Name'] + ', '
                        instructors = instructors[0 : len(instructors) - 2]
                    elif obj.has_key('IS_SCL_DESCR_IS_SCL_DESCRL'):
                        instructors += obj['IS_SCL_DESCR_IS_SCL_DESCRL']
                    if instructors.endswith(':'):
                        instructors = ''

                    desc = self.utils.clearHtmlTag(obj['Description'].strip()).strip()
                    if desc != '':
                        description += desc
                    else:
                        description = ''
                    self.count += 1
                    self.write_db(f, 'harford-' + k + '-' + obj['CRSE_ID'], title, 'https://courses.my.harvard.edu/psp/courses/EMPLOYEE/EMPL/h/?tab=HU_CLASS_SEARCH&SearchReqJSON=%7B%22SearchText%22%3A%22%s%22%7D'.replace('%s', obj['CRSE_ID']), term + ' ' + instructors + ' ' + description)
                
                if jobj[2]['PageNumber'] == jobj[2]['TotalPages'] or search_ok == False:
                    break
            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"


    
start = HarvardSpider()
start.doWork()
