#!/usr/bin/env python

from spider import *

class YoutubeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'youtube'
        self.courses = {}
        self.playlist_urls = {\
                'mit': 'https://www.youtube.com/user/MIT/playlists',\
                'stanford': 'https://www.youtube.com/user/StanfordUniversity/playlists',\
                'berkeley': 'https://www.youtube.com/user/UCBerkeley/playlists',\
                'cmu': 'https://www.youtube.com/user/CarnegieMellonU/playlists?view=1&sort=dd',\
                'harvard': 'https://www.youtube.com/user/harvard/playlists',\
                'caltech': 'https://www.youtube.com/user/caltech/playlists',\
                'udacity' : 'https://www.youtube.com/user/Udacity/playlists?view=1&sort=dd',\
                'cambridge' : 'https://www.youtube.com/user/CambridgeUniversity/playlists?sort=dd&view=1',\
                'nptel' : 'https://www.youtube.com/user/nptelhrd/playlists'}

    def getCourse(self, html, user):
        soup = BeautifulSoup(html)
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'].startswith('/playlist?list='):
                key = a.text.strip()
                if key.find('|') != -1:
                    key = key[key.find('|') + 1 :].strip() 
                if user == 'berkeley' and key.startswith('Computer Science '):
                    key = key.replace('Computer Science ', 'CS')
                if user == 'berkeley' and key.startswith('Electrical Engineering '):
                    key = key.replace('Electrical Engineering ', 'EE')
                self.courses[key] = 'https://www.youtube.com' + a['href']

    def getLoadMoreHref(self, html):
        if html.strip() == '':
            return ''
        soup = BeautifulSoup(html)
        button = soup.find('button', class_='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button')
        if button != None:
            return button['data-uix-load-more-href']
        return ''
        
    def getPlaylist(self, user, url):
        self.courses = {}
        r = requests.get(url)
        self.getCourse(r.text, user)

        load_more_href = self.getLoadMoreHref(r.text)

        while (load_more_href != ''):

            r = requests.get('https://www.youtube.com' + load_more_href)
            jobj = json.loads(r.text)
            load_more_href = self.getLoadMoreHref(jobj['load_more_widget_html'].strip())

            self.getCourse(jobj['content_html'], user)


        file_name = self.get_file_name(self.school + '/' + user, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for k, v in [(k,self.courses[k]) for k in sorted(self.courses.keys())]:
            self.count += 1
            video_id = user + '-' + str(self.count)
            if k.startswith('MIT'):
                k = k[4:]
                if k[0 : k.find(' ')].find('.') != -1:
                    video_id = user + '-' + k[0 : k.find(' ')]
                    k = k[k.find(' ') : ].strip()

            print k + ' ' + v
            self.write_db(f, video_id, k, v, 'videourl:' + v)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        for user, url in self.playlist_urls.items():
            self.getPlaylist(user, url)


def main(argv):
    start = YoutubeSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)

