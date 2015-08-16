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

    popular_lang_list = [
        "ActionScript",
        "C",
        "C#",
        "C++",
        "Clojure",
        "CoffeeScript",
        "CSS",
        "Go",
        "Haskell",
        "HTML",
        "Java",
        "JavaScript",
        "Lua",
        "Matlab",
        "Objective-C",
        "Perl",
        "PHP",
        "Python",
        "R",
        "Ruby",
        "Scala",
        "Shell",
        "Swift",
        "TeX",
        "VimL"]

    other_lang_list = [
        "ABAP",
        "Ada",
        "Agda",
        "AGS Script",
        "Alloy",
        "AMPL",
        "Ant Build System",
        "ANTLR",
        "ApacheConf",
        "Apex",
        "API Blueprint",
        "APL",
        "AppleScript",
        "Arc",
        "Arduino",
        "AsciiDoc",
        "ASP",
        "AspectJ",
        "Assembly",
        "ATS",
        "Augeas",
        "AutoHotkey",
        "AutoIt",
        "Awk",
        "Batchfile",
        "Befunge",
        "Bison",
        "BitBake",
        "BlitzBasic",
        "BlitzMax",
        "Bluespec",
        "Boo",
        "Brainfuck",
        "Brightscript",
        "Bro",
        "C-ObjDump",
        "C2hs Haskell",
        "Cap'n Proto",
        "CartoCSS",
        "Ceylon",
        "Chapel",
        "Charity",
        "ChucK",
        "Cirru",
        "Clarion",
        "Clean",
        "CLIPS",
        "CMake",
        "COBOL",
        "ColdFusion",
        "ColdFusion CFC",
        "Common Lisp",
        "Component Pascal",
        "Cool",
        "Coq",
        "Cpp-ObjDump",
        "Creole",
        "Crystal",
        "Cucumber",
        "Cuda",
        "Cycript",
        "Cython",
        "D",
        "D-ObjDump",
        "Darcs Patch",
        "Dart",
        "desktop",
        "Diff",
        "DIGITAL Command Language",
        "DM",
        "Dockerfile",
        "Dogescript",
        "DTrace",
        "Dylan",
        "E",
        "Eagle",
        "eC",
        "Ecere Projects",
        "ECL",
        "edn",
        "Eiffel",
        "Elixir",
        "Elm",
        "Emacs Lisp",
        "EmberScript",
        "Erlang",
        "F#",
        "Factor",
        "Fancy",
        "Fantom",
        "Filterscript",
        "fish",
        "FLUX",
        "Formatted",
        "Forth",
        "FORTRAN",
        "Frege",
        "G-code",
        "Game Maker Language",
        "GAMS",
        "GAP",
        "GAS",
        "GDScript",
        "Genshi",
        "Gentoo Ebuild",
        "Gentoo Eclass",
        "Gettext Catalog",
        "GLSL",
        "Glyph",
        "Gnuplot",
        "Golo",
        "Gosu",
        "Grace",
        "Gradle",
        "Grammatical Framework",
        "Graph Modeling Language",
        "Graphviz (DOT)",
        "Groff",
        "Groovy",
        "Groovy Server Pages",
        "Hack",
        "Haml",
        "Handlebars",
        "Harbour",
        "Haxe",
        "HCL",
        "HTML+Django",
        "HTML+ERB",
        "HTML+PHP",
        "HTTP",
        "Hy",
        "HyPhy",
        "IDL",
        "Idris",
        "IGOR Pro",
        "Inform 7",
        "INI",
        "Inno Setup",
        "Io",
        "Ioke",
        "IRC log",
        "Isabelle",
        "Isabelle ROOT",
        "J",
        "Jade",
        "Jasmin",
        "Java Server Pages",
        "JFlex",
        "JSON",
        "JSON5",
        "JSONiq",
        "JSONLD",
        "Julia",
        "KiCad",
        "Kit",
        "Kotlin",
        "KRL",
        "LabVIEW",
        "Lasso",
        "Latte",
        "Lean",
        "Less",
        "Lex",
        "LFE",
        "LilyPond",
        "Limbo",
        "Linker Script",
        "Linux Kernel Module",
        "Liquid",
        "Literate Agda",
        "Literate CoffeeScript",
        "Literate Haskell",
        "LiveScript",
        "LLVM",
        "Logos",
        "Logtalk",
        "LOLCODE",
        "LookML",
        "LoomScript",
        "LSL",
        "M",
        "Makefile",
        "Mako",
        "Markdown",
        "Mask",
        "Mathematica",
        "Maven POM",
        "Max",
        "MediaWiki",
        "Mercury",
        "MiniD",
        "Mirah",
        "Modelica",
        "Modula-2",
        "Module Management System",
        "Monkey",
        "Moocode",
        "MoonScript",
        "MTML",
        "MUF",
        "mupad",
        "Myghty",
        "NCL",
        "Nemerle",
        "nesC",
        "NetLinx",
        "NetLinx+ERB",
        "NetLogo",
        "NewLisp",
        "Nginx",
        "Nimrod",
        "Ninja",
        "Nit",
        "Nix",
        "NL",
        "NSIS",
        "Nu",
        "NumPy",
        "ObjDump",
        "Objective-C++",
        "Objective-J",
        "OCaml",
        "Omgrofl",
        "ooc",
        "Opa",
        "Opal",
        "OpenCL",
        "OpenEdge ABL",
        "OpenSCAD",
        "Org",
        "Ox",
        "Oxygene",
        "Oz",
        "Pan",
        "Papyrus",
        "Parrot",
        "Parrot Assembly",
        "Parrot Internal Representation",
        "Pascal",
        "PAWN",
        "Perl6",
        "PicoLisp",
        "PigLatin",
        "Pike",
        "PLpgSQL",
        "PLSQL",
        "Pod",
        "PogoScript",
        "PostScript",
        "PowerShell",
        "Processing",
        "Prolog",
        "Propeller Spin",
        "Protocol Buffer",
        "Public Key",
        "Puppet",
        "Pure Data",
        "PureBasic",
        "PureScript",
        "Python traceback",
        "QMake",
        "QML",
        "Racket",
        "Ragel in Ruby Host",
        "RAML",
        "Raw token data",
        "RDoc",
        "REALbasic",
        "Rebol",
        "Red",
        "Redcode",
        "RenderScript",
        "reStructuredText",
        "RHTML",
        "RMarkdown",
        "RobotFramework",
        "Rouge",
        "Rust",
        "Sage",
        "SaltStack",
        "SAS",
        "Sass",
        "Scaml",
        "Scheme",
        "Scilab",
        "SCSS",
        "Self",
        "ShellSession",
        "Shen",
        "Slash",
        "Slim",
        "Smali",
        "Smalltalk",
        "Smarty",
        "SMT",
        "SourcePawn",
        "SPARQL",
        "SQF",
        "SQL",
        "SQLPL",
        "Squirrel",
        "Standard ML",
        "Stata",
        "STON",
        "Stylus",
        "SuperCollider",
        "SVG",
        "SystemVerilog",
        "Tcl",
        "Tcsh",
        "Tea",
        "Text",
        "Textile",
        "Thrift",
        "TOML",
        "Turing",
        "Turtle",
        "Twig",
        "TXL",
        "TypeScript",
        "Unified Parallel C",
        "Unity3D Asset",
        "UnrealScript",
        "Vala",
        "VCL",
        "Verilog",
        "VHDL",
        "Visual Basic",
        "Volt",
        "Vue",
        "Web Ontology Language",
        "WebIDL",
        "wisp",
        "xBase",
        "XC",
        "XML",
        "Xojo",
        "XPages",
        "XProc",
        "XQuery",
        "XS",
        "XSLT",
        "Xtend",
        "Yacc",
        "YAML",
        "Zephir",
        "Zimpl"]

    result = ""
    request_times = 0
    token = ''
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

    def processPageData(self, f, file_name, lang, url, name_contain=''):
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
                    if name_contain != '' and item["name"].find(name_contain) == -1:
                        continue
                    data = str(item['stargazers_count']) + " " + item["name"] + " " + item['html_url']
                    print data
                    description = ""
                    if item['description'] != None:
                        description = 'author:' + item['owner']['login'] + ' description:' + item['description'] + " (stars:" + str(item["stargazers_count"]) + " forks:" + str(item['forks_count']) + " watchers:" + str(item['watchers']) + ")"
                    self.write_db(f, str(item["stargazers_count"]) + "-" + str(item['forks_count']), item["name"], item['html_url'], description)
                    self.count = self.count + 1
        return total_size

    def processGithubData(self, lang, large_than_stars, per_page, name_contain=''):
        file_name = self.get_file_name("eecs/github/" + lang, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        page = 1
        url = self.getUrl(lang, page, str(large_than_stars), str(per_page))
        self.count = 0

        print "processing " + lang + " url: " + url

        total_size = self.processPageData(f, file_name, lang, url, name_contain)
        if total_size > 1000:
            total_size = 1000
        while total_size > (page *per_page):
            #print "total size:" + str(total_size) + " request page 2"
            page += 1
            self.processPageData(f, file_name, lang, self.getUrl(lang, page, str(large_than_stars), str(per_page)), name_contain)
     
        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getUserUrl(self, location, followers, page, per_page):
        if location == "all":
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
        file_name = self.get_file_name("rank/" + location, self.school + "-user")
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
        star = 300
        per_page = 100
        for lang in self.lang_list:
            self.processGithubData(lang, star, per_page)

        if len(self.result) > 1:
            print self.result + " is not be updated"
        keywords = ['awesome', 'computer vision', 'nlp', 'nltk', 'spark', 'machine learning', 'deep learning', 'android']
        for keyword in keywords:
            print "get " + keyword + " data..."
            if keyword == "awesome":
                self.processGithubData(keyword, 100, per_page, keyword)
            else:
                self.processGithubData(keyword, star, per_page)
        print "get user data..."
        self.processGithubiUserData("all", 500, 100)
        self.processGithubiUserData("china", 500, 100)
start = GithubSpider()
start.doWork()
