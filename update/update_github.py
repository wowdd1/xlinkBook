#!/usr/bin/env python
 
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *
sys.path.append("..")
from utils import Utils
from record import Record

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
        "Jupyter+Notebook",
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
        f = open('../github_token', 'rU')
        self.token = ''.join(f.readlines()).strip()


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
                    self.write_db(f, 'github-' + item['owner']['login'].strip() + '-' + item["name"].strip(), item["name"], item['html_url'], description)
                    self.count = self.count + 1
        return total_size

    def processGithubData(self, lang, large_than_stars, per_page, name_contain=''):
        file_name = self.get_file_name("eecs/projects/github/" + lang, self.school)
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

    def getOrganizationProjects(self):
        data_eecs = {"google" : "https://github.com/google",\
                "google-cloud-platform" : "https://github.com/GoogleCloudPlatform",\
                'googlesamples' : 'https://github.com/googlesamples',\
                "youtube" : 'https://github.com/youtube',\
                "microsoft" : "https://github.com/Microsoft",\
                "donet" : "https://github.com/dotnet",\
                "apple" : "https://github.com/apple/",\
                "yahoo" : "https://github.com/yahoo",\
                "facebook" : "https://github.com/facebook",\
                "twitter" : "https://github.com/twitter",\
                "aws" : "https://github.com/aws",\
                "awslabs" : "https://github.com/awslabs",\
                "amznlabs" : "https://github.com/amznlabs",\
                "awslabs" : "https://github.com/awslabs",\
                "linkedin" : "https://github.com/linkedin",\
                "baidu" : "https://github.com/Baidu",\
                "baidu-research" : 'https://github.com/baidu-research',\
                "dmlc" : "https://github.com/dmlc",\
                "amplab" : "https://github.com/amplab",\
                'OculusVR' : 'https://github.com/OculusVR/',\
                'OSVR' : 'https://github.com/OSVR/',\
                'ValveSoftware' : 'https://github.com/ValveSoftware',\
                'id-Software' : 'https://github.com/id-Software',\
                'EA-games' : 'https://github.com/electronicarts',\
                'sony' : 'https://github.com/sony',\
                'Blizzard' : 'https://github.com/Blizzard',\
                'openai' : 'https://github.com/openai',\
                'deepmind' : "https://github.com/deepmind",\
                'mozilla' : 'https://github.com/mozilla',\
                'openstack': 'https://github.com/openstack',\
                'reddit' : 'https://github.com/reddit',\
                'quora' : 'https://github.com/quora',\
                'netflix' : 'https://github.com/Netflix',\
                'adobe' : 'https://github.com/adobe',\
                'alibaba' : 'https://github.com/Alibaba',\
                'ebay' : 'https://github.com/ebay',\
                'zhihu' : 'https://github.com/zhihu',\
                'vimeo' : 'https://github.com/vimeo',\
                'aol' : 'https://github.com/aol',\
                'yelp' : 'https://github.com/yelp',\
                'wordpress' : 'https://github.com/wordpress',\
                'ibm' : 'https://github.com/ibm',\
                'netease' : 'https://github.com/NetEase',\
                'mysql' : 'https://github.com/mysql',\
                'imgur' : 'https://github.com/imgur',\
                'sogou' : 'https://github.com/sogou',\
                'flickr' : 'https://github.com/Flickr',\
                'hulu' : 'https://github.com/hulu',\
                'coursera' : 'https://github.com/coursera',\
                'edx' : 'https://github.com/edx',\
                'udacity' : 'https://github.com/udacity',\
                'commaai' : 'https://github.com/commaai',\
                'bvlc' : 'https://github.com/BVLC',\
                'tum-vision' : 'https://github.com/tum-vision/',\
                'GoogleChrome' : 'https://github.com/GoogleChrome',\
                'uArm-Developer' : 'https://github.com/uArm-Developer',\
                'arduino' : 'https://github.com/arduino',\
                'ai2' : 'https://github.com/allenai',\
                'microsoft-research' : 'https://github.com/microsoftresearch',\
                'facebook-research' : 'https://github.com/facebookresearch',\
                'ibm-research' : 'https://github.com/ibm-research',\
                'ibm-watson' : 'https://github.com/ibm-watson',\
                'csail' : 'https://github.com/csail',\
                'stanford' : 'https://github.com/stanford',\
                'IBM-Bluemix' : 'https://github.com/IBM-Bluemix',\
                'watson-developer-cloud' : 'https://github.com/watson-developer-cloud',\
                'Samsung' : 'https://github.com/Samsung',\
                'nvidia' : 'https://github.com/nvidia',\
                'AMD' : 'https://github.com/amd',\
                'macmillanpublishers' : 'https://github.com/macmillanpublishers',\
                'oreillymedia' : 'https://github.com/oreillymedia',\
                'usgs' : 'https://github.com/usgs',\
                'gitter' : 'https://github.com/gitterHQ',\
                'Oxford-Robotics-Institute' : 'https://github.com/oxford-ori',\
                'ToyotaResearchInstitute' : 'https://github.com/ToyotaResearchInstitute',\
                'mila-udem' : 'https://github.com/mila-udem'}

        data_neuro = {'INCF' : 'https://github.com/INCF',\
                'nipy' : 'https://github.com/nipy',\
                'OpenNeuroLab' : 'https://github.com/OpenNeuroLab',\
                'PySurfer' : 'https://github.com/PySurfer',\
                'CBMM' : 'https://github.com/CBMM',\
                'AllenInstitute' : 'https://github.com/AllenInstitute',\
                'ACElab' : 'https://github.com/aces',\
                'MCB80x' : 'https://github.com/mcb80x',\
                'BackyardBrains' : 'https://github.com/BackyardBrains',\
                'nengo' : 'https://github.com/nengo'}

        data_gene = { 'CIDAR-LAB' : 'https://github.com/CIDARLAB',\
                      'Voigt-Lab' : 'https://github.com/VoigtLab',\
                      'ENCODE-DCC' : 'https://github.com/ENCODE-DCC'}

        self.getProjectByDict(data_eecs, 'eecs/projects/github/organization/')
        self.getProjectByDict(data_neuro, 'neuroscience/projects/github/organization/')
        self.getProjectByDict(data_gene, 'biology/projects/github/organization/')
        #self.getStartupPorjects('../db/economics/startup-billion-dollar-club2016')
        #self.getStartupPorjects('../db/rank/smartest-companies2016')
        #self.getStartupPorjects('../db/rank/self-driving-company2016')

    def getStartupPorjects(self, path):
        data = {}
        if os.path.exists(path):
            f = open(path, 'rU')
            for line in f.readlines():
                record = Record(line)
                key = record.get_title().replace(' ', '').replace('.', '').strip()
                url = 'https://github.com/' + key
                data[key.lower()] = url 
                  
        if len(data) > 0:
            self.getProjectByDict(data, 'eecs/projects/github/organization/')

    def getProjectByDict(self, data, path):
        for k in data:

            file_name = self.get_file_name(path + k, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            print data[k]
            r = self.requestWithAuth(data[k])
            soup = BeautifulSoup(r.text)
            pages = 1
            for a in soup.find_all('a'):
                if a['href'].find('page=') != -1 and a.text != "Next":
                    pages = int(a.text)
            print pages
            project_dict = {}
            for i in range(1, pages + 1):
                print data[k] + "?page=" + str(i)
                r = self.requestWithAuth(data[k] + "?page=" + str(i))
                soup = BeautifulSoup(r.text) 

                starDict = {}
                for a in soup.find_all('a', class_='muted-link tooltipped tooltipped-s mr-3'):
                    project = a['href'].replace('/stargazers', '')
                    project = project[project.rfind('/') + 1 :].lower()
                    starDict[project] = int(a.text.strip().replace(',', ''))

                for li in soup.find_all('li'):
                    if li.h3 == None:
                        continue
                    title =  li.h3.a.text.strip()
                    if starDict.has_key(title.lower()) == False:
                        starDict[title.lower()] = 0
                    
                    desc = ''
                    if li.p != None:
                        desc = "description:" + li.p.text.strip().replace('\n', '')
                    self.count += 1
                    id = 'github-' + k + "-" + str(self.count) 
                    record = self.get_storage_format(str(starDict[title.lower()]), title, "https://github.com" + li.h3.a['href'], desc)
                    project_dict[id] = Record(record)
            self.count = 0
            for item in sorted(project_dict.items(), key=lambda project_dict:int(project_dict[1].get_id().strip()), reverse=True):
                print item[1].get_id() + " " + item[1].get_title()
                self.count += 1
                id = item[0][0 : item[0].rfind('-')] + '-' + item[1].get_title().strip()
                self.write_db(f, id, item[1].get_title().strip(), item[1].get_url().strip(), 'author:'+ k + ' ' + item[1].get_describe().strip())

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

        self.getProjects(star, per_page)
        #self.getKeyProjects(star, per_page)
        #self.getUsers(500, 100)
        #self.getOrganizations()

    def getProjects(self, star, per_page):
        for lang in self.lang_list:
            self.processGithubData(lang, star, per_page)
        
        if len(self.result) > 1:
            print self.result + " is not be updated"

    def getKeyProjects(self, star, per_page):
        keywords = ['awesome', 'computer vision', 'nlp', 'artificial intelligence', 'spark', 'machine learning', 'deep learning', 'android']
        for keyword in keywords:
            print "get " + keyword + " data..."
            if keyword == "awesome":
                self.processGithubData(keyword, 100, per_page, keyword)
            else:
                self.processGithubData(keyword, star, per_page)

    def getUsers(self, star, per_page):
        print "get user data..."
        self.processGithubiUserData("all", star, per_page)
        self.processGithubiUserData("china", star, per_page)

    def getOrganizations(self):
        self.getOrganizationProjects()

start = GithubSpider()
start.doWork()
