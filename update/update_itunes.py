#!/usr/bin/env python
# -*- coding: utf-8 -*-
from spider import *
import codecs
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
sys.path.append("..")
from utils import Utils
from record import Record

class ItunesSpider(Spider):
    utils = Utils()

    def __init__(self):
        Spider.__init__(self)
        self.school = 'itunes'
        self.deep_mind = True

    def itunesPdfParser(self, data):
        outfile = data+'.txt'
        fp = file(data, 'rb')
        outfp = file(outfile,'w')
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.


        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data =  retstr.getvalue()

        device.close()
        outfp.close()

        f = open(outfile,'r')
        result = ''
        course_list = []
        i = 0
        for line in f.readlines():
            if len(line.strip()) > 0:
                i += 1
                if i < 3 and line.find('…') == -1:
                    result += line.strip() + ' '
            else:
                if result.strip() == 'Explore App Store':
                    break
                if result.find('iTunes U') != -1 or result.find('Featured Featured') != -1:
                    result = ''
                    i = 0
                    continue
                course_list.append(result)
                #print result
                result = ''
                i = 0
        f.close()
        os.remove(outfile)
        return course_list

    def getDescription(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        div = soup.find('div', class_='intro')
        description = ''
        if div != None:
            for line in div.text.strip().split('\n'):
                if line.strip()[0 : 2] == 'by':
                    description = 'instructors:' + line.strip()[2 : ].strip() + ' '
                    break
        
        span = soup.find('span', class_="rating-count")
        if span != None:
            description += " ratings:" + span.text[0 : span.text.find(" ")] + ' '

        div = soup.find('div', class_="product-review")
        if div != None:
            description += 'description:' + div.text.strip().replace('\n', '')[div.text.strip().replace('\n', '').find(' ') :].strip() + ' '
            
            
        return description

    def getTerm(self, title):
        term = ''
        if title.find("Fall") != -1:
            term = title[title.find("Fall") : ].replace('UC Berkeley', '').replace('|', '').replace(' ', '')
        if title.find("Spring") != -1:
            term = title[title.find("Spring") : ].replace('UC Berkeley', '').replace('|', '').replace(' ', '')
        return term

    def convertBerkeleyTitle(self, title):
        if title.find("Computer Science ") == -1 and title.find("Electrical Engineering ") == -1:
            return title, self.getTerm(title), ""
        if title.find("Computer Science ") != -1:
            title = title.replace('Computer Science ', 'CS')

        term = self.getTerm(title)
        if title.find("Electrical Engineering ") != -1:
            title = title.replace('Electrical Engineering ', 'EE')        
        if title.find(",") != -1:
            title = title[0 : title.find(",")]
        if title.find("|") != -1:
            title = title[0 : title.find("|")]
        if title.find("/") != -1:
            title = title[0 : title.find("/")]
        
        return title, term, self.utils.getRecord(title, path="../db/eecs/").get_title().strip()

    def processData(self, subject, courses, school):
        print 'processing ' + subject + ' of ' + school
        file_name = self.get_file_name(subject + "/itunes/" + subject, school)
        file_lines = self.countFileLineNum(file_name)
        if file_lines == len(courses):
            print school + ' no need upgrade\n'
            return
        f = self.open_db(file_name + ".tmp")      
        self.count = 0
        course_dict = {}

        for course in courses:
            r = requests.get("https://itunes.apple.com/search?term=" + course)
            jobj = json.loads(r.text)
            if len(jobj['results']) > 0:
                print str(jobj['results'][0]['collectionId']) + ' ' + jobj['results'][0]['collectionName'] + ' ' + jobj['results'][0]['collectionViewUrl']
                url = jobj['results'][0]['collectionViewUrl']
                description = ''
                if self.deep_mind:
                    description = self.getDescription(url)
                title = jobj['results'][0]['collectionName']
                if school.lower().find('berkeley') != -1:
                    course_num, term, title = self.convertBerkeleyTitle(title)
                    record = self.get_storage_format(str(jobj['results'][0]['collectionId']), course_num + ' ' + title + ' ' + term, url, description)
                    course_dict[course_num + str(jobj['results'][0]['collectionId']) + term] = Record(record)
                else:
                    course_dict[str(jobj['results'][0]['collectionId'])] = Record(self.get_storage_format(str(jobj['results'][0]['collectionId']), title, url, description))
                    for item in sorted(course_dict.items(), key=lambda course_dict:course_dict[1].get_title().strip()):
                        print item[1].get_title().strip()

        if school.lower().find('berkeley') != -1:
            for k, record in [(k,course_dict[k]) for k in sorted(course_dict.keys())]:
                self.count += 1
                self.write_db(f, record.get_id().strip(), record.get_title().strip(), record.get_url().strip(), record.get_describe().strip())
        else:
            for item in sorted(course_dict.items(), key=lambda course_dict:course_dict[1].get_title().strip()):
                self.count += 1
                self.write_db(f, item[1].get_id().strip(), item[1].get_title().strip(), item[1].get_url().strip(), item[1].get_describe().strip())

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.processData('eecs', self.itunesPdfParser('../pdf/mit_engineering_itunes2015.pdf'), "mit-" + self.school)
        self.processData('eecs', self.itunesPdfParser('../pdf/stanford_engineering_itunes2015.pdf'), "stanford-" + self.school)
        self.processData('eecs', self.itunesPdfParser('../pdf/berkeley_engineering_itunes2015.pdf'), "berkeley-" + self.school)
        self.processData('eecs', self.itunesPdfParser('../pdf/harvard_engineering_itunes2015.pdf'), "harvard-" + self.school)
        self.processData('eecs', self.itunesPdfParser('../pdf/princeton_engineering_itunes2015.pdf'), "princeton-" + self.school)

start = ItunesSpider()
start.doWork()
