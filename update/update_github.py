#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class GithubSpider(Spider):
    lang_list = [
        "C",
        "C#",
        "C++",
        "Clojure",
        "CoffeeScript",
        "Common Lisp",
        "CSS",
        "Diff",
        "Emacs Lisp",
        "Erlang",
        "Haskell",
        "HTML",
        "Java",
        "JavaScript",
        "Lua",
        "Objective-C",
        "Perl",
        "PHP",
        "Python",
        "Ruby",
        "Scala",
        "Scheme",
        "Shell",
        "SQL"]

    def __init__(self):
        Spider.__init__(self)
        self.school = "github"

    def processGithubData(self, lang, greater):
        file_name = self.get_file_name("eecs-" + lang, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        url = "https://api.github.com/search/repositories?q=stars:>" + greater +"+language:" +  lang + "&sort=stars&order=desc"
        print "processing " + lang + " " + url
        r = requests.get(url)
        dict_obj = json.loads(r.text)
        self.count = 0
        for (k, v) in dict_obj.items():
            if k =="message":
                print v
                self.cancel_upgrade(file_name)
                return
            if k == "items":
                for item in v:
                    data = str(item['stargazers_count']) + " " + item["name"] + " " + item['html_url']
                    print data
                    self.write_db(f, item["name"] + "-" + str(item['stargazers_count']), item["full_name"], item['html_url'])
                    self.count = self.count + 1
 
        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def do_work(self):
        for lang in self.lang_list:
            self.processGithubData(lang, '100')

start = GithubSpider()
start.do_work()
