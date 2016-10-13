#!/usr/bin/env python

from spider import *


class Webcast():
    def __init__(self):
        self.semester = ''
        self.videoId = ''
        self.audioId = ''
        self.title = ''
        self.lecturer = ''
        self.descr = ''
        self.dept = ''
        self.youTube = ''

    def get_semester(self):
        return self.semester

    def get_videoId(self):
        return self.videoId

    def get_audioId(self):
        return self.audioId

    def get_title(self):
        return self.title

    def get_lecturer(self):
        return self.lecturer

    def get_descr(self):
        return self.descr

    def get_dept(self):
        return self.dept

    def get_youTube(self):
        return self.youTube

    def set_semester(self, value):
        self.semester = value

    def set_videoId(self, value):
        self.videoId = value

    def set_audioId(self, value):
        self.audioId = value

    def set_title(self, value):
        self.title = value

    def set_lecturer(self, value):
        self.lecturer = value

    def set_descr(self, value):
        self.descr = value

    def set_dept(self, value):
        self.dept = value

    def set_youTube(self, value):
        self.youTube = value

class BerkeleyWebcastSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
    
    def compareTerm(self, term1, term2):
        if term2[term2.find(' ') :].strip() > term1[term1.find(' ') :].strip():
            return True
        elif term2[term2.find(' ') :].strip() == term1[term1.find(' ') :].strip():
            if term2 == 'Fall':
                return True
        return False

    def getWebcastDict(self, subject_list):
        r = requests.get('http://webcast.berkeley.edu/itunesu_podcasts.js')
        pos = r.text.find('itu_courses = [')
        webcast_dict = {}
        for item in r.text[pos + 16 : r.text.find('];', pos)].replace('} ,', '},').split('},'):
            if item.strip() != '':
                webcast = Webcast()
                for kv in item.replace('{', '').replace('};', '').replace('", "', '","').strip().split('","'):
                    kv = kv.replace('"', '')
                    key = kv[0 : kv.find(':')]
                    value = kv[kv.find(':') + 1 :]
                    if key == 'semester':
                        webcast.set_semester(value.strip())
                    elif key == 'videoId':
                        webcast.set_videoId('https://itunes.apple.com/us/podcast/id' + value)
                    elif key == 'audioId':
                        webcast.set_audioId(value)
                    elif key == 'title':
                        if value.find(',') != -1:
                            webcast.set_title(value[0 : value.find(',')].strip())
                        elif value.find('-') != -1:
                            webcast.set_title(value[0 : value.find('-')].strip())
                        else:
                            webcast.set_title(value)
                    elif key == 'lecturer':
                        webcast.set_lecturer(value)
                    elif key == 'descr':
                        webcast.set_descr(value.strip())
                    elif key == 'dept':
                        webcast.set_dept(value.strip())
                    elif key == 'youTube':
                        webcast.set_youTube('https://www.youtube.com/view_play_list?p=' + value)
                for subject in subject_list:
                    if webcast.get_dept() == subject:
                        webcast.set_title(webcast.get_title().replace('Computer Science ', 'CS').replace('Electrical Engineering ', 'EE'))
                        if webcast_dict.get(webcast.get_title(), '') != '':
                            if self.compareTerm(webcast_dict[webcast.get_title()].get_semester(), webcast.get_semester()):
                                webcast_dict[webcast.get_title()] = webcast
                        else:
                            webcast_dict[webcast.get_title()] = webcast

        return webcast_dict
        '''
        for k, v in [(k, webcast_dict[k]) for k in sorted(webcast_dict.keys())]:
            print k + ' ' + v.get_semester()
        '''

    def getDepts(self):
        r = requests.get('http://webcast.berkeley.edu/itunesu_podcasts.js')
        pos = r.text.find('itu_courses = [')
        depts = {}
        for item in r.text[pos + 16 : r.text.find('];', pos)].replace('} ,', '},').split('},'):
            if item.strip() != '':
                for kv in item.replace('{', '').replace('};', '').replace('", "', '","').strip().split('","'):
                    kv = kv.replace('"', '')
                    key = kv[0 : kv.find(':')]
                    value = kv[kv.find(':') + 1 :]
                    if key == 'dept':
                        if depts.has_key(value.strip()):
                            continue
                        depts[value.strip()] = ''
                        #print value.strip()
        return depts

    def doWork(self):
        for subject, v in self.getDepts().items():
            if self.need_update_subject(subject) == False:
                continue
            print 'processing ' + subject
            data = self.getWebcastDict([subject])
            for k, webcast in data.items():
                print webcast.get_title()

def main(argv):
    start = BerkeleyWebcastSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)
