#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *

py3k = sys.version_info[0] >= 3
if py3k:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser

class TableHandler(HTMLParser):
    def __init__(self, **kwargs):
        HTMLParser.__init__(self)
        self.kwargs = kwargs
        self.active = None
        self.last_content = ""
        self.rows = []
        self.found_first_valid_num = False

    def handle_starttag(self,tag, attrs):
        self.active = tag

    def handle_endtag(self,tag):
        #if tag in ["th", "td"]:
        #    print self.last_content.strip()
        #if tag in ['tr']:
        #    self.last_content = " "

        self.active = None
    def valid_course_num(self, text):
        if text.find(' ') == -1 and text != '&' and text != 'Previous' and text != 'unknown' and text != 'Neural' and text != 'Mechatronics' and text != 'Cryptography':
            return True
        return False

    def handle_data(self, data):
        data = data.replace('\n', '').strip()
        if len(data) == 0 or data == '[' or data == ']' or data == 'archives':
            return

        if self.valid_course_num(data):
            if self.found_first_valid_num:
                #print self.last_content
                self.rows.append(self.last_content)
               
            if data[0 : 2] == 'CS': 
                self.found_first_valid_num = True
            self.last_content = ""
 
        #print data.strip()
        if data[0: 4] == 'Last':
            return
        self.last_content += data + ' '


class BerkeleySpider(Spider):
    video_lecture_list = {\
        'CS10' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iAq0HYSJAcbgbjjSIafuHJF',\
        'CS149' : 'https://www.youtube.com/playlist?list=PL62BE418C34C3B2BD',\
        'CS162' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iD9V_LiNxDf_itUWO5BMl_6',\
        'CS164' : 'https://www.youtube.com/playlist?list=PL3A16CFC42CA6EF4F',\
        'CS169' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iAS_kCeleydK6mDc0kCbdhU',\
        'CS170' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iBapEvcNwRuTJVt6BPpcMaJ',\
        'CS184' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iBifi0GQVF1R9M_QBWw3xgG',\
        'CS188' : 'https://www.youtube.com/playlist?list=PLF1A9D9034225FC92',\
        'CS194' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iB_5Q8G8kW5idSwNmXypmQE',\
        'CS61A' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iC9x0nmh5OZyxljQU6pUWWk',\
        'CS61B' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iAlnI-BQr9hjqADPBtujFJd',\
        'CS61C' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iDHtKXLFJbDG-i6L9oDr5X9',\
        'CS61CL' : 'https://itunes.apple.com/us/podcast/computer-science-61cl-001/id354819035?mt=2&ign-mpt=uo%3D4',\
        'CS70' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iDze6fOp3qofgyjJVUioedA',\
        'CS98' : 'https://itunes.apple.com/us/podcast/computer-science-98-198-032/id913301637?mt=2&uo=4',\
        'CSC149' : 'https://www.youtube.com/playlist?list=PL62BE418C34C3B2BD',\
        'EE40' : 'https://www.youtube.com/playlist?list=PL627AE6688C09001E',\
        'EE100' : 'https://www.youtube.com/playlist?list=PL62BE418C34C3B2BD',\
        'EE105' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iApSM93gWkcSauu8gRoH7It',\
        'EE119' : 'https://itunes.apple.com/us/podcast/electrical-engineering-119/id354821527?mt=2&ign-mpt=uo%3D4',\
        'EE130' : 'https://itunes.apple.com/us/podcast/electrical-engineering-130/id557805531?mt=2&ign-mpt=uo%3D4',\
        'EE127' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iDuLMumekQlMWrPDm08V0co',\
        'EE130' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iDy-rACIy-kh40XJJDp3Y0X',\
        'EE140' : 'https://www.youtube.com/playlist?list=PL-XXv-cvA_iD7dvgmsm7lQTxvjbjBNh4I',\
        'EE141' : 'https://www.youtube.com/playlist?list=PLD4C75518947B4347',\
        'EE149' : 'https://www.youtube.com/playlist?list=PL62BE418C34C3B2BD',\
        'EE20N' : 'https://itunes.apple.com/us/podcast/electrical-engineering-20n/id354821504?mt=2&ign-mpt=uo%3D4',\
        'EE227A' : 'https://itunes.apple.com/us/podcast/electrical-engineering-227a/id498403557?mt=2&ign-mpt=uo%3D4',\
        'EE240' : 'https://www.youtube.com/playlist?list=PLFB77B9910B9FD20E',\
        'EE241' : 'https://itunes.apple.com/us/podcast/electrical-engineering-241/id354820903?mt=2&ign-mpt=uo%3D4',\
        'EE247' : 'https://itunes.apple.com/us/podcast/electrical-engineering-247/id354821202?mt=2&ign-mpt=uo%3D4',\
        'EE290C' : 'https://itunes.apple.com/us/podcast/electrical-engineering-290c/id438303607?mt=2&ign-mpt=uo%3D4',\
        'EE290F' : 'https://www.youtube.com/playlist?list=PL04A2692F8E5B9D2B',\
        'EE40' : 'https://itunes.apple.com/us/podcast/electrical-engineering-40/id391534824?mt=2&ign-mpt=uo%3D4',\
        'EEC245' : 'https://www.youtube.com/playlist?list=PL8A24132C07C45F61',\
        'EEW290C' : 'https://www.youtube.com/playlist?list=PL81E2F15D026EEA81'\
    }   

    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.subject = "eecs"
        self.deep_mind = True
   
    def getLink(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        links = []
        for a in soup.find_all('a'):
            if a['href'][0 : 2] == './':
                links.append(url.replace('archives.html', '') + a['href'][2:])
        return links[len(links) - 1]
    
    def processBerkeleyData(self, f, tr):
        if self.need_update_subject(self.subject) == False:
            return
        i = 0
        title = ""
        link = ""
        for td in tr.children:
           if i == 3:
               title = title + td.a.string + " "
           if i == 5:
               title = title + td.u.string
               link = "http://www-inst.eecs.berkeley.edu" + td.a["href"]
               link = self.getLink(link)
           i = i + 1
        if i > 4:
            self.count = self.count + 1
            self.write_db(f, title[0:title.find(" ")], title[title.find(" "):], link)

    def genUrl(self, course_num):
        return 'http://www-inst.eecs.berkeley.edu/~' + course_num.lower() + '/archives.html'    

    def getRealUrl(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        link_dict = {}
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'][0 : 2] == './':
                key = a.text.strip().replace('Spring ', '').replace('Summer ', '').replace('Fall ', '').replace('Winter ', '')
                link_dict[key] = (url.replace('archives.html', '') + a['href'][2:])
        sorted_keys = sorted(link_dict)

        for i in range(len(sorted_keys) - 1, -1 , -1):
            test_url = link_dict[sorted_keys[i]]
            try:
                r = requests.get(test_url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text)
                    for a in soup.find_all('a'):
                        if a.text.strip() == url:
                            #print test_url + ' not match'
                            break
                    #print 'match ' + test_url
                    return test_url
            except Exception , e:
                print e
        if len(sorted_keys) > 0:
            return link_dict[sorted_keys[len(sorted_keys) - 1]]
        else:
            return url

    def doWork(self):
        #berkeley
        #"""
        print "downloading berkeley course info"
        r = requests.get("http://www-inst.eecs.berkeley.edu/classes-cs.html")

        parser = TableHandler()
        parser.feed(r.text)

        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
    
        print "processing html and write data to file..."
        '''
        for table in soup.find_all("table", class_="column"):
            tr =  table.tr
            self.processBerkeleyData(f, tr)
    
            for next_tr in tr.next_siblings:
                if next_tr.string == None:
                    self.processBerkeleyData(f, next_tr)
    
        '''
        for row in parser.rows:
            url = self.genUrl(row[0: row.find(" ")])
            print row 
            self.count = self.count + 1
            if self.deep_mind:
                url = self.getRealUrl(url)
            description = ''
            if self.video_lecture_list.get(row[0:row.find(" ")] , '') != '':
                description = 'features:Video lectures' + ' '
            self.write_db(f, row[0:row.find(" ")], row[row.find(" "):], url, description)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
start = BerkeleySpider();
start.doWork() 
