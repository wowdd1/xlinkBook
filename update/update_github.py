#!/usr/bin/env python
 
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class GithubSpider(Spider):
    lang_list = [
        "C",
        "C++",
        "C#",
        "Clojure",
        "CoffeeScript",
        "Common Lisp",
        "CSS",
        "D",
        "Dart",
        "Emacs Lisp",
        "Erlang",
        "F#",
        "Go",
        "Haskell",
        "Java",
        "JavaScript",
        "Julia",
        "Lua",
        "Matlab",
        "Objective-C",
        "Perl",
        "PHP",
        "Python",
        "R",
        "Ruby",
        "Scala",
        "Scheme",
        "Shell",
        "SQL",
        "Swift"]

    result = ""
    request_times = 0
    token = '2193754a92b5e1d9bbd2e3c3bbb7186fa3fd0b1f'
    def __init__(self):
        Spider.__init__(self)
        self.school = "github"

    def isQueryLang(self, lang):
        for item in self.lang_list:
            if item.lower() == lang.lower():
                return True
        return False

    def requestWithAuth(self, url):
        if self.token != "":
            return requests.get(url, auth=(self.token, ''))    
        else:
            return requests.get(url)

    def getUrl(self, lang, page, large_than_stars, per_page):
        if self.isQueryLang(lang) == True:
            return "https://api.github.com/search/repositories?page=" + str(page) + "&per_page=" + per_page + "&q=stars:>" + large_than_stars +"+language:" +  lang.replace("#","%23").replace("+","%2B") + "&sort=stars&order=desc"
        else:
            return "https://api.github.com/search/repositories?page=" + str(page) + "&per_page=" + per_page + "&q=" + lang + "+stars:>" + large_than_stars + "&sort=stars&order=desc"

    def checkRequestTimes(self):
        self.request_times += 1
        if self.request_times % 10 == 0:
            print "wait 60s..."
            time.sleep(60) 

    def processPageData(self, f, file_name, lang, url):
        #self.checkRequestTimes()
        #print "url: " + url
        r = self.requestWithAuth(url)
        dict_obj = json.loads(r.text)
        total_size = 0
        for (k, v) in dict_obj.items():
            if k == "total_count":
                total_size = v
            if k == "message":
                print v
                self.result += lang + " "
                self.cancel_upgrade(file_name)
                return
            if k == "items":
                for item in v:
                    data = str(item['stargazers_count']) + " " + item["name"] + " " + item['html_url']
                    print data
                    description = ""
                    if item['description'] != None:
                        description = 'author:' + item['owner']['login'] + ' description:' + item['description'] + " (stars:" + str(item["stargazers_count"]) + " forks:" + str(item['forks_count']) + " watchers:" + str(item['watchers']) + ")"
                    self.write_db(f, str(item["stargazers_count"]) + "-" + str(item['forks_count']), item["name"], item['html_url'], description)
                    self.count = self.count + 1
        return total_size

    def processGithubData(self, lang, large_than_stars, per_page):
        file_name = self.get_file_name("eecs/github/" + lang, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        page = 1
        url = self.getUrl(lang, page, str(large_than_stars), str(per_page))
        self.count = 0

        print "processing " + lang
 
        total_size = self.processPageData(f, file_name, lang, url)
        if total_size > 1000:
            total_size = 1000
        while total_size > (page *per_page):
            #print "total size:" + str(total_size) + " request page 2"
            page += 1
            self.processPageData(f, file_name, lang, self.getUrl(lang, page, str(large_than_stars), str(per_page)))
     
        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getUserUrl(self, location, followers, page, per_page):
        if location == "":
            return "https://api.github.com/search/users?page=" + str(page) + "&per_page=" + per_page + "&q=followers:>" + followers
        else:
            return "https://api.github.com/search/users?page=" + str(page) + "&per_page=" + per_page + "&q=followers:>" + followers + "+location:" + location

    def getUserRepos(self, url):
        #self.checkRequestTimes()
        r = self.requestWithAuth(url)
        repos = ""
        jobj = json.loads(r.text)
        repo_dict = {}

        for repo in jobj:
            str_repo = repo['name'] + "("
            if repo["stargazers_count"] != None and repo["stargazers_count"] > 0:
                str_repo += "stars:" + str(repo["stargazers_count"])
            if repo['forks_count'] != None and repo['forks_count'] > 0:
                str_repo += " forks:" + str(repo['forks_count'])
            if repo['watchers'] != None and repo['watchers'] > 0:
                str_repo += " watchers:" + str(repo['watchers'])
            if repo["language"] != None:
                 str_repo += " lang:" + str(repo["language"])
            if repo['stargazers_count'] != None:
                repo_dict[repo.get("stargazers_count", 0)] = str_repo.strip() + ") "
            else:
                repo_dict[0] = str_repo.strip() + ") "
        print sorted(repo_dict.keys(), reverse=True)
        i = 0
        for k, repo in [(k,repo_dict[k]) for k in sorted(repo_dict.keys(), reverse=True)]:
            i += 1
            if i == 1:
                repos += "toprepo:" + repo + ' '
            else:
                repos += "project:" + repo

        print repos + "\n"
        return repos 

    def getUserFollowers(self, url):
        #self.checkRequestTimes()
        r = self.requestWithAuth(url)
        followers = ""
        jobj = json.loads(r.text)

        for follower in jobj:
            followers += follower["login"] + " "

        print followers + "\n"
        return followers

    def processUserPageData(self, f, file_name, url):
        #self.checkRequestTimes()
        r = self.requestWithAuth(url)
        dict_obj = json.loads(r.text)
        total_size = 0
        for (k, v) in dict_obj.items():
            if k == "total_count":
                total_size = v
            if k == "message":
                print v
                self.cancel_upgrade(file_name)
                return
            if k == "items":
                for item in v:
                    data = str(item["id"]) + " " + item["login"] + " " + item["html_url"]
                    print data
                    self.write_db(f, item["type"] + "-" + str(item["id"]), item["login"], item["html_url"], self.getUserRepos(item["repos_url"])) #"followers: " + self.getUserFollowers(item["followers_url"]))
                    self.count = self.count + 1
        return total_size

    def processGithubiUserData(self, location, followers, per_page):
        #self.checkRequestTimes()
        file_name = self.get_file_name("eecs/github/" + location, self.school + "-user")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        page = 1
        url = self.getUserUrl(location, str(followers), str(page), str(per_page))
            
        print "processing " + url
        total_size = self.processUserPageData(f, file_name, url)
        if total_size > 1000:
            total_size = 1000
        while total_size > (page *per_page):
            page += 1
            self.processUserPageData(f, file_name, self.getUserUrl(location, str(followers), str(page), str(per_page)))

        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        for lang in self.lang_list:
            self.processGithubData(lang, 500, 100)

        if len(self.result) > 1:
            print self.result + " is not be updated"
        keywords = ['spark', 'machine learning', 'deep leanrning', 'android']
        for keyword in keywords:
            print "get " + keyword + " data..."
            self.processGithubData(keyword, 350, 100)
        
        print "get user data..."
        self.processGithubiUserData("", 500, 100)
        self.processGithubiUserData("china", 500, 100)
        
        
start = GithubSpider()
start.doWork()
