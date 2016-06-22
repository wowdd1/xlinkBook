#!/usr/bin/env python

from spider import *

class YoutubeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'youtube'
        self.playlist = {}
        self.videos = {}
        
        self.playlist_urls = {\
                'mit': 'https://www.youtube.com/user/MIT/playlists',\
                'stanford': 'https://www.youtube.com/user/StanfordUniversity/playlists',\
                'stanfordonline' : 'https://www.youtube.com/user/stanfordonline/playlists',\
                'berkeley': 'https://www.youtube.com/user/UCBerkeley/playlists',\
                'cmu': 'https://www.youtube.com/user/CarnegieMellonU/playlists?view=1&sort=dd',\
                'harvard': 'https://www.youtube.com/user/harvard/playlists',\
                'caltech': 'https://www.youtube.com/user/caltech/playlists',\
                'udacity' : 'https://www.youtube.com/user/Udacity/playlists?view=1&sort=dd',\
                'cambridge' : 'https://www.youtube.com/user/CambridgeUniversity/playlists?sort=dd&view=1',\
                'oxford' : 'https://www.youtube.com/user/oxford/playlists?sort=dd&view=1',\
                'ucla' : 'https://www.youtube.com/user/UCLA/playlists',\
                'texas' : 'https://www.youtube.com/user/utaustintexas/playlists',\
                'imperialcollegelondon' : 'https://www.youtube.com/user/imperialcollegevideo/playlists',\
                'toronto' : 'https://www.youtube.com/user/universitytoronto/playlists',\
                'uns' : 'https://www.youtube.com/user/NUScast/playlists',\
                'unsw' : 'https://www.youtube.com/user/UNSWelearning/playlists?sort=dd&view=1',\
                'nptel' : 'https://www.youtube.com/user/nptelhrd/playlists',\
		'CBMM' : 'https://www.youtube.com/channel/UCGoxKRfTs0jQP52cfHCyyRQ/playlists'}

        self.videos_urls = { 'ucl' : 'https://www.youtube.com/user/Mikesev/videos?view=0&sort=dd&live_view=500&flow=grid',
                             'sciwrite' : 'https://www.youtube.com/channel/UC-wb-n89yM0lBiP2QltsDaA/videos',\
                             'MicrosoftResearch' : 'https://www.youtube.com/user/MicrosoftResearch/videos',\
                             'GoogleTechTalks' : 'https://www.youtube.com/user/GoogleTechTalks/videos',\
                             'GoogleDevelopers' : 'https://www.youtube.com/user/GoogleDevelopers/videos',\
                             'Apple' : 'https://www.youtube.com/user/Apple/videos',\
                             'FacebookDevelopers' : 'https://www.youtube.com/user/FacebookDevelopers/videos',\
                             'IBMResearch' : 'https://www.youtube.com/user/IBMLabs/videos',\
                             'BaiduResearch' : 'https://www.youtube.com/channel/UCm08TSsp87RRfn9SB_khuUQ/videos',\
                             'DeepMind' : 'https://www.youtube.com/channel/UCP7jMXSY2xbc3KCAE0MHQ-A/videos',\
                             'Nvidia' : 'https://www.youtube.com/user/nvidia/videos',\
                             'BostonDynamics' : 'https://www.youtube.com/user/BostonDynamics/videos',\
                             'TwitterDev' : 'https://www.youtube.com/channel/UCcRd4oOOUPKAvg6vs2P9ReA/videos',\
                             'DARPA' : 'https://www.youtube.com/user/DARPAtv/videos',\
                             'nasa' : 'https://www.youtube.com/user/NASAtelevision/videos',\
                             'Watson' : 'https://www.youtube.com/user/IBMWatsonSolutions/videos',\
                             'IBM' : 'https://www.youtube.com/user/IBM/videos',\
                             'cvprtum' : 'https://www.youtube.com/user/cvprtum/videos',\
                             'ibmthinkacademy' : 'https://www.youtube.com/user/ibmthinkacademy/videos',\
                             'developerworks' : 'https://www.youtube.com/user/developerworks/videos',\
                             'rework' : 'https://www.youtube.com/user/teamrework/videos',\
                             'AmazonWebServices' : 'https://www.youtube.com/user/AmazonWebServices/videos',\
                             'MITCSAIL' : 'https://www.youtube.com/user/MITCSAIL/videos',\
                             'cmurobotics' : 'https://www.youtube.com/user/cmurobotics/videos',\
                             'stanfordeng' : 'https://www.youtube.com/user/stanfordeng/videos',\
                             'docker' : 'https://www.youtube.com/user/dockerrun/videos',\
                             'spark' : 'https://www.youtube.com/user/TheApacheSpark/videos',\
                             'TwitterUniversity' : 'https://www.youtube.com/user/TwitterUniversity/videos',\
                             'AI2' : 'https://www.youtube.com/channel/UCEqgmyWChwvt6MFGGlmUQCQ',\
                             'GoogleCloudPlatform' : 'https://www.youtube.com/user/googlecloudplatform/videos',\
                             'lifeatgoogle' : 'https://www.youtube.com/user/lifeatgoogle/videos',\
                             'spacex' : 'https://www.youtube.com/user/spacexchannel/videos',\
                             'mitmedialab' : 'https://www.youtube.com/user/mitmedialab/videos',\
                             'MagicLeap' : 'https://www.youtube.com/channel/UC2E1x3l45YUO2eOhRv-A7lw/videos',\
                             'RockstarGames' : 'https://www.youtube.com/user/RockstarGames/videos',\
                             'oculusvr' : 'https://www.youtube.com/user/oculusvr/videos',\
                             'ign' : 'https://www.youtube.com/user/IGNentertainment/videos',\
                             'CryTek' : 'https://www.youtube.com/user/CryDevPortal/videos',\
                             'UnrealEngin' : 'https://www.youtube.com/user/UnrealDevelopmentKit/videos',\
                             'TwoMinutePapers' : 'https://www.youtube.com/user/keeroyz/videos',\
                             'watsonanalytics' : 'https://www.youtube.com/user/watsonanalytics/videos',\
                             'VisualStudio' : 'https://www.youtube.com/user/VisualStudio/videos',\
                             'WorkingAtMicrosoft' : 'https://www.youtube.com/user/WorkingAtMicrosoft/videos',
                             'singularityu' : 'https://www.youtube.com/user/singularityu/videos',\
                             'SingularityLectures' : 'https://www.youtube.com/channel/UC-a4MiIis33-Z9vLYFerN6g/videos',\
                             '2045Initiative' : 'https://www.youtube.com/user/2045ru/videos',\
                             'MITTechnologyReview' : 'https://www.youtube.com/user/TechnologyReview/videos',\
                             'nature' : 'https://www.youtube.com/user/NatureVideoChannel/videos',\
                             'ScienceMag' : 'https://www.youtube.com/user/ScienceMag/videos',\
                             'SciAmerican' : 'https://www.youtube.com/user/SciAmerican/videos',\
			     'nips' : 'https://www.youtube.com/user/NeuralInformationPro/videos',\
			     'UCFCRCV' : 'https://www.youtube.com/user/UCFCRCV/videos',\
			     'McGovernInstitute' : 'https://www.youtube.com/channel/UCDqKkRpDCSqPx8kGn0aTIZw/videos',\
			     'NIBIB' : 'https://www.youtube.com/user/NIBIBTV/videos',\
			     'TheHumanBrainProject' : 'https://www.youtube.com/user/TheHumanBrainProject/videos',\
			     'allenInstitute' : 'https://www.youtube.com/user/AllenInstitute/videos',\
			     'ICLR' : 'https://www.youtube.com/channel/UCqxFGrNL5nX10lS62bswp9w/videos',\
			     'singularitysummit' : 'https://www.youtube.com/user/singularitysummit/videos',\
			     'anfavideo' : 'https://www.youtube.com/user/anfavideo/videos',\
			     'broadinstitute' : 'https://www.youtube.com/user/broadinstitute/videos',\
                             'harvardmedicalschool' : 'https://www.youtube.com/user/harvardmedicalschool/videos',\
                             'iBiology' : 'https://www.youtube.com/user/ibioseminars/videos',\
                             'iBioMagazine' : 'https://www.youtube.com/user/ibiomagazine/videos',\
                             'iBioEducation' : 'https://www.youtube.com/user/iBioEducation/videos',\
                             'tedx' : 'https://www.youtube.com/user/TEDxTalks/videos',\
                             'ted' : 'https://www.youtube.com/user/TEDtalksDirector/videos',\
                             'CodeNeuro' : 'https://www.youtube.com/channel/UCZqlliYGopB9zved7pJTi_A/videos'}
    def getPlaylist(self, html, user):
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
                self.playlist[key] = 'https://www.youtube.com' + a['href']

    def getLoadMoreHref(self, html):
        if html.strip() == '':
            return ''
        soup = BeautifulSoup(html)
        button = soup.find('button', class_='yt-uix-button yt-uix-button-size-default yt-uix-button-default load-more-button yt-uix-load-more browse-items-load-more-button')
        if button != None:
            return button['data-uix-load-more-href']
        return ''

    def getVideo(self, f, html, user, contain, prefix):
        soup = BeautifulSoup(html)
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'].startswith('/watch?v='):
                key = a.text.strip()
                if key == '':
                    continue
                if contain != '' and key.find(contain) == -1:
                    continue
                url = 'https://www.youtube.com' + a['href']
                self.count += 1
                print prefix + '-' + str(self.count) + ' | ' + key + ' | ' + url + ' | '
		self.write_db(f, prefix + '-' + str(self.count), key, url)
                self.videos[key] = url

    def getVideos(self, user, url):
        self.videos = {}
        file_name = self.get_file_name('videos/' + user, self.school)
	file_lines = self.countFileLineNum(file_name)
	f = self.open_db(file_name + ".tmp")
	self.count = 0

        r = requests.get(url)
        contain = ''
        prefix = user.lower()
        self.count = 0
        self.getVideo(f, r.text, user, contain, prefix)
        
        load_more_href = self.getLoadMoreHref(r.text)

        while (load_more_href != ''):

            r = requests.get('https://www.youtube.com' + load_more_href)
            jobj = json.loads(r.text)
            load_more_href = self.getLoadMoreHref(jobj['load_more_widget_html'].strip())

            self.getVideo(f, jobj['content_html'], user, contain, prefix) 

        self.close_db(f)
	if file_lines != self.count and self.count > 0:
	    self.do_upgrade_db(file_name)
	    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
	else:
	    self.cancel_upgrade(file_name)
	    print "no need upgrade\n"



    def getPlaylists(self, user, url):
        self.playlist = {}
        r = requests.get(url)
        self.getPlaylist(r.text, user)

        load_more_href = self.getLoadMoreHref(r.text)

        while (load_more_href != ''):

            r = requests.get('https://www.youtube.com' + load_more_href)
            jobj = json.loads(r.text)
            load_more_href = self.getLoadMoreHref(jobj['load_more_widget_html'].strip())

            self.getPlaylist(jobj['content_html'], user)

        file_name = self.get_file_name('playlist/' + user, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for k, v in [(k,self.playlist[k]) for k in sorted(self.playlist.keys())]:
        #for k, v in self.playlist.items():
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
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        #for user, url in self.playlist_urls.items():
        #    self.getPlaylists(user, url)
        for user, url in self.videos_urls.items():
            self.getVideos(user, url)


def main(argv):
    start = YoutubeSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)

