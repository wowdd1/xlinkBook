#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class ProjectPaperSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.utils = Utils()
        self.school = "project-papers"
        self.dirs = "eecs/papers/project-papers/" 

    def doWork(self):
        '''
        self.getSTAIRPapers()
        self.getSTARTPapers()
        self.getSparkPapers()
        self.getHadoopPapers()
        #self.getRoboBrainPapers()
        self.getMobileyePapers()
        self.getAutonomousDrivingPapers()

        self.getCALOPapers()
        '''
        #self.getWastonPapers()
        self.getDeepmindPapers()
        #self.getFacebookResearchPapers()
        #self.getGoogleBrainPapers()
	#self.getAI2Papers()
	#self.getBaiduResearchPapers()

    def getBaiduResearchPapers(self):

	urls = ['http://research.baidu.com/silicon-valley-ai-lab/', 'http://research.baidu.com/institute-of-deep-learning', 'http://research.baidu.com/big-data-lab/']
        file_name = self.get_file_name(self.dirs + "baidu-research", self.school)
	file_lines = self.countFileLineNum(file_name)
	f = self.open_db(file_name + ".tmp")
	self.count = 0
        papers = {}
	for url in urls:
	    r = requests.get(url)
	    soup = BeautifulSoup(r.text)
            title = ''
	    link = ''
	    authors = 'author:'
	    summary = 'summary:'
	    desc = 'description:'
	    for p in soup.find_all('p'):
		title = ''
		link = ''
		authors = 'author:'
		summary = 'summary:'
		desc = 'description:'
	        data = p.text.split('\n')
	        if len(data) == 3 or (len(data) == 1 and p.em != None):
		    if data[0] == '':
		        continue
		    if len(data) == 3:
		        title = data[0]
			if p.a != None:
			    link = p.a['href']
			authors += data[1] + ' '
			desc += data[2] + ' '
			#print title
			self.count += 1
	                id = 'baidu-research-' + str(self.count)
			if self.count < 10:
			    id = 'baidu-research-0' + str(self.count)

			papers[id] = [title, link, authors, desc]
			title = ''
			link = ''
			authors = 'author:'
			summary = 'summary:'
			desc = 'description:'
		    elif len(data) == 1:
			summary += data[0] + ' '
			id = 'baidu-research-' + str(self.count)
			if self.count < 10:
			    id = 'baidu-research-0' + str(self.count)
			papers[id].append(summary)
	for k, v in sorted(papers.items(), key=lambda papers:papers[0][papers[0].rfind('-') + 1 :]):
	    print v
	    if len(v) == 5:
	        self.write_db(f, k, v[0], v[1], v[2] + v[4] + v[3])
            else:
	        self.write_db(f, k, v[0], v[1], v[2] + v[3])
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
	    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
	else:
	    self.cancel_upgrade(file_name)
	    print "no need upgrade\n"

    def getAI2Papers(self):
	r = requests.get('http://allenai.org/papers.html')
	soup = BeautifulSoup(r.text)
	ul = soup.find('ul', class_='filter-data')
	soup = BeautifulSoup(ul.prettify())

        file_name = self.get_file_name(self.dirs + "ai2", self.school)
        file_lines = self.countFileLineNum(file_name)
	f = self.open_db(file_name + ".tmp")
	self.count = 0
	for li in soup.find_all('li'):
	    title = li.a.text.strip()
	    link = li.a['href']
	    sp = BeautifulSoup(li.prettify())
	    authors = "author:"
	    desc = 'description:'
	    count = 0
	    for em in sp.find_all('em'):
                count += 1
		if count == 1:
		    authors += em.text.replace('\n', '').strip() + ' '
		else:
	            desc += em.text.replace('\n', '').strip() + ' '
	    print authors
	    print desc
	    self.count += 1
	    self.write_db(f, 'ai2-' + str(self.count), title, link, authors + desc)
        if file_lines != self.count and self.count > 0:
	    self.do_upgrade_db(file_name)
	    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
	else:
	    self.cancel_upgrade(file_name)
	    print "no need upgrade\n"

    def getGoogleBrainPapers(self):
        r = requests.get('https://research.google.com/pubs/BrainTeam.html')
	soup = BeautifulSoup(r.text)
	ul = soup.find('ul', class_='pub-list')
	soup = BeautifulSoup(ul.prettify())

        file_name = self.get_file_name(self.dirs + "googlebrain", self.school)
        file_lines = self.countFileLineNum(file_name)
	f = self.open_db(file_name + ".tmp")
        self.count = 0
	for li in soup.find_all('li'):
            sp = BeautifulSoup(li.prettify())
	    link = sp.find('a', class_='pdf-icon tooltip')
	    if link != None:
		link = 'https://research.google.com' + link['href']
	    else:
		link = ''
	    title = sp.find('p', class_='pub-title')
	    count = 0
	    authors ="author:"
	    desc = 'description:'
	    for p in sp.find_all('p'):
	        count += 1
	        if count == 1:
	            title = self.utils.removeDoubleSpace(p.text.strip().replace('\n', ''))
		if count == 2:
		    authors += self.utils.removeDoubleSpace(p.text.replace('\n', '')).strip() + ' '
		    authors = authors.replace(' ,', ',').strip() + ' '
		if count == 3:
		    desc += self.utils.removeDoubleSpace(p.text.replace('\n', '')).strip() + ' '
            print title
	    print link
	    print authors
	    print desc
	    self.count += 1
	    self.write_db(f, 'googlebrain-' + str(self.count), title, link, authors + desc)
        self.close_db(f)
	if file_lines != self.count and self.count > 0:
	    self.do_upgrade_db(file_name)
	    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
	else:
	    self.cancel_upgrade(file_name)
	    print "no need upgrade\n"

    def getFacebookResearchPapers(self):
        count = 0

        file_name = self.get_file_name(self.dirs + "facebook-ai", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        while True:
            count += 1
	    #https://research.facebook.com/publications/machinelearning,machinelearningarea/
            r = self.requestWithProxy2('https://research.facebook.com/publications/ai/?p=' + str(count))
            print r.status_code
            if r.status_code != 200:
                break
            if r.text.find('More contents coming soon') != -1:
                break
            soup = BeautifulSoup(r.text)
            divs = soup.find_all('div', class_='_3y3h')
            for div in divs:
                sp = BeautifulSoup(div.prettify())
                title = ''
                link = ''
                authors = 'author:'
                published = 'published:'
                summary = 'summary:'
                category = 'category:'
                desc = 'description:'
                div = sp.find('div', class_='_3y3i')
                if div == None:
                    continue
                if div.a != None:
                    title += div.a.text.strip() + ' '
                    link = 'https://research.facebook.com' + div.a['href']
                div = sp.find('div', class_='_3y34')
                if div != None:
                    for li in BeautifulSoup(div.prettify()).find_all('li'):
                        authors += li.text.strip() + ', '
                    authors = authors[0 : len(authors) - 2] + ' '
                div = sp.find('div', class_='_3y3n')
                if div != None:
                    desc += div.text.strip() + ' '
                div = sp.find('div', class_='_3y3l')
                if div != None:
                    published += div.text.strip() + ' '
                div = sp.find('div', class_='_1c-z')
                if div != None:
                    summary += div.text.strip() + ' '
                div = sp.find('div', class_='_3y3m')
                if div != None:
                    category += self.utils.removeDoubleSpace(div.text.replace('\n', '')).strip() + ' '

                print title
                self.count += 1
                self.write_db(f, 'facebook-ai-' + str(self.count), title, link, authors + published + category + summary + desc)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDeepmindPapers(self):
        file_name = self.get_file_name(self.dirs + "deepmind", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        '''
        for ul in soup.find_all('ul', class_='publication'):
            #print ul
            sp = BeautifulSoup(ul.prettify())
            title = sp.find('li', class_='title').text.strip()
            link = sp.find('li', class_='title').a['href']
            authors = ''
            for span in sp.find_all('span', class_='author'):
                authors += span.text.strip() + ', '
            authors = authors[0 : len(authors) - 2]
            desc = self.utils.removeDoubleSpace(sp.find('li', class_='abstract').text.strip().replace('\n', ' '))

            print title
            print link
            print authors
            print desc
            self.count += 1
            self.write_db(f, 'deepmind-' + str(self.count), title, link, 'author:' + authors + ' description:' + desc)
        '''
        all_authors = {}
        for page in range(0 , 100):
            url = 'https://deepmind.com/research/publications/?page=' + str(page + 1)
            print url
            r = self.requestWithProxy(url)

            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text)
            divs = soup.find_all('div', class_='research-list--item-heading')
            if len(divs) == 0:
                break
            for div in divs:
                print div.h1.text
                desc = div.p.text
                data = self.utils.removeDoubleSpace(div.text[div.text.find('Authors:') + 8 :].strip().replace('\n', ' '))
                for author in data.split(','):
                    author = author.strip()
                    if all_authors.has_key(author) == False:
                        all_authors[author] = author
                print data
                self.count += 1
                self.write_db(f, 'deepmind-paper-' + str(self.count), div.h1.text, '', 'author:' + data + ' description:' + desc)

        print ', '.join(all_authors.keys())

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getCALOPapers(self):
        r = requests.get('http://www.ai.sri.com/pubs/search.php?project=179')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.dirs + "CALO", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            title = li.p.strong.text.strip()
            link = 'http://www.ai.sri.com' + li.p.a['href']
            print title
            self.count += 1
            self.write_db(f, 'calo-' + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getAutonomousDrivingPapers(self):
        r = requests.get("http://driving.stanford.edu/papers.html")
        soup = BeautifulSoup(r.text)
        title = ""
        author = ""
        journal = ""
        desc = ""
        url = ""
        file_name = self.get_file_name(self.dirs + "AutonomousDriving", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for p in soup.find_all("p"):
            if p.span != None:
                sp = BeautifulSoup(p.prettify())
                title = sp.find('span', class_='papertitle').text.strip()
                author = "author:" + self.utils.removeDoubleSpace(sp.find('span', class_='authors').text.strip().replace('\n', '')) + " "
                journal = "journal:" + sp.find('span', class_='meeting').text.strip()
                journal += " " + sp.find('span', class_='year').text.strip() + " "
                desc = "description:" +  self.utils.removeDoubleSpace(sp.find('span', class_='summary').text.strip().replace('\n', ''))
            if p.a != None and p.a['href'].find(".pdf") != -1:
                if p.a['href'].startswith('http'):
                    url = p.a['href']
                else:
                    url = 'http://driving.stanford.edu/' + p.a['href']
                self.count += 1
                self.write_db(f, "autonomousdriving-paper-" + str(self.count), title, url, author + journal + desc)
                title = ""
                author = ""
                journal = ""
                desc = ""
                url = "" 
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getMobileyePapers(self):
        file_name = self.get_file_name(self.dirs + "Mobileye", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for i in range(1, 3):
            r = requests.get("http://www.mobileye.com/technology/mobileye-research/page/" + str(i))
            soup = BeautifulSoup(r.text)

            for div in soup.find_all("div", class_="ContentItemText"):
                title = div.h2.text.strip()
                link = div.h2.a['href']
                author = "author:" + div.p.text.strip()
                print title
                self.count += 1
                self.write_db(f, "mobileye-paper-" + str(self.count), title, link, author)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getHadoopPapers(self):
        r = requests.get("http://wiki.apache.org/hadoop/Papers")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.dirs + "hadoop", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.p != None:
                print li.p.a.text
                self.count += 1
                self.write_db(f, "hadoop-paper-" + str(self.count), li.p.a.text, li.p.a["href"])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSparkPapers(self):
        r = requests.get("http://spark.apache.org/documentation.html")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.dirs + "spark", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None and li.a["href"].find("pdf") != -1 and li.em != None:
                title = li.a.text
                author =  "author:" + li.prettify()[li.prettify().find('</a>') + 7: li.prettify().find('<em>')].strip() + " "
                journal = "journal:" + li.em.text
                print title
                self.count += 1
                self.write_db(f, "spark-paper-" + str(self.count), title , li.a["href"], author + journal)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"



    def getSTARTPapers(self):
        r = requests.get("http://start.mit.edu/publications.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.dirs + "START", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
       
        link = ""
        title = ""
        journal = ""
        author = ""
        for td in soup.find_all("td"):
            if td.a != None and td.strong == None and td.a["href"] != "index.php":
                print ""
                if td.a["href"].find("http") == -1:
                    link = "http://start.mit.edu/" + td.a["href"]
                else:
                    link = td.a["href"]
                print link
            else:
                if td.strong != None:
                    if td.em != None:
                        journal = "journal:" + td.em.text + " "
                        print journal
                    if td.strong != None:
                        title = td.strong.text
                        print title
                else:
                    if td.em != None:
                        title = td.em.text
                        print title
                if td.text.find(".") != -1:
                    author = "author:" + td.text[0 : td.text.find(".")] + " "
                    print author
                    print ""
                    self.count += 1
                    self.write_db(f, "start-paper-" + str(self.count), title, link, author + journal)
                    title = ""
                    link = ""
                    author = ""
                    journal = ""

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSTAIRPapers(self):
        r = requests.get("http://stair.stanford.edu/papers.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.dirs + "STAIRP", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            title = ""
            link = ""
            if li.span == None:
                continue
            title = li.span.text
                
            if li.a != None:
                link = li.a['href']
            self.count += 1
            self.write_db(f, "STAIRP-paper-" + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getRoboBrainPapers(self):
        r = requests.get("http://robobrain.me/#/about")
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.dirs + "robotbrain", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        print r.text
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getWastonPapers(self):
        r = requests.get('http://researcher.watson.ibm.com/researcher/view_group_pubs.php?grp=2099')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.dirs + "waston", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all("div", class_="publication"):
            link = ""
            authors = ""
            journal = ""
            title = div.h4.text.strip()
            if div.h4.a != None:
                link = div.h4.a['href']
            sp = BeautifulSoup(div.prettify())
            count = 0
            for span in sp.find_all("span", class_="pubspan"):
                count += 1
                data = self.utils.removeDoubleSpace(span.text.strip().replace("\n", ""))
                if count == 1:
                    authors = "author:" + data + " "
                if count == 2:
                    journal = "journal:" + data
            print title
            print authors
            print journal
            print link
            self.count += 1
            self.write_db(f, "waston-paper-" + str(self.count), title, link, authors + journal)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = ProjectPaperSpider()
start.doWork()
