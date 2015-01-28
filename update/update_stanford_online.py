#!/usr/bin/env python

from spider import *

class StanfordOnlineSpider(Spider):

    def __init__(self):
        Spider.__init__(self)


    def getCourseNameDict(self):
        r = requests.get('http://online.stanford.edu/courses/all')
        soup = BeautifulSoup(r.text)
        course_dict = {}
        i = 0
        for tr in soup.find_all('tr'):
            link = ''
            if tr.td != None and tr.td.a != None and tr.td.a.attrs.has_key("href"):
                link = tr.td.a['href']
            data = tr.text.replace('\n', '|').strip()
            if data[0 : 1] == '|':
                data = data[1 : ].strip()
            if data == '':
                continue
            i += 1
            key = data[0 : data.find('|')].strip()
            if key.find('(') != -1:
                key = key[0 : key.find('(')].strip()
            if course_dict.get(key, '') != '' and course_dict[key].find('http') == -1 and link == '':
                continue
            if link == '':
                continue

            course_dict[key] = link
        return course_dict


