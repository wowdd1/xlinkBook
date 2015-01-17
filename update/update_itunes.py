#!/usr/bin/env python
# -*- coding: utf-8 -*-
from spider import *
import codecs
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

class ItunesSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'itunes'

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

        div = soup.find('div', class_="product-review")
        if div != None:
            description += 'description:' + div.text.strip().replace('\n', '')[div.text.strip().replace('\n', '').find(' ') :].strip() + ' '
            
        return description
 
    def processData(self, subject, courses, school):
        print 'processing ' + subject + ' of ' + school
        file_name = self.get_file_name(subject + "/itunes/" + subject, school)
        file_lines = self.countFileLineNum(file_name)
        if file_lines == len(courses):
            print school + ' no need upgrade\n'
            return
        f = self.open_db(file_name + ".tmp")      
        self.count = 0

        for course in courses:
            r = requests.get("https://itunes.apple.com/search?term=" + course)
            jobj = json.loads(r.text)
            if len(jobj['results']) > 0:
                print str(jobj['results'][0]['collectionId']) + ' ' + jobj['results'][0]['collectionName'] + ' ' + jobj['results'][0]['collectionViewUrl']
                self.count += 1
                url = jobj['results'][0]['collectionViewUrl']
                description = self.getDescription(url)
                self.write_db(f, str(jobj['results'][0]['collectionId']), jobj['results'][0]['collectionName'], url, description)

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
