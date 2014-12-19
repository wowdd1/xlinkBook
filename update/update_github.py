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
    def __init__(self):
        Spider.__init__(self)
        self.school = "github"

    def processGithubData(self, lang, greater):
        file_name = self.get_file_name("eecs-" + lang, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        url = "https://api.github.com/search/repositories?q=stars:>" + greater +"+language:" +  lang.replace("#","%23").replace("+","%2B") + "&sort=stars&order=desc"
        print "processing " + lang + " " + url
        r = requests.get(url)
        dict_obj = json.loads(r.text)
        self.count = 0
        for (k, v) in dict_obj.items():
            if k =="message":
                self.result += lang + " "
                self.cancel_upgrade(file_name)
                return
            if k == "items":
                for item in v:
                    data = str(item['stargazers_count']) + " " + item["name"] + " " + item['html_url']
                    print data
                    self.write_db(f, str(item["stargazers_count"]) + "-" + str(item['forks_count']), item["name"], item['html_url'])
                    self.count = self.count + 1
 
        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def do_work(self):
        i = 0
        for lang in self.lang_list:
            i += 1
            self.processGithubData(lang, '100')
            if i == 10 or i == 20:
                print "wait 35s..."
                time.sleep(35)

        if len(self.result) > 1:
            print self.result + " is not be updated"

start = GithubSpider()
start.do_work()
