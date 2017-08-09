#!/usr/bin/env python


from spider import *
import urllib
import time
import feedparser
import os
import cPickle as pickle
import argparse
import random
sys.path.append("..")
from utils import Utils
from record import Record
from record import PaperRecord
from random import randint

'''
prefix  explanation
ti      Title
au      Author
abs     Abstract
co      Comment
jr      Journal Reference
cat     Subject Category
rn      Report Number
id      Id (use id_list instead)
all     All of the above

Subject Abbreviation    Description
stat.AP Statistics - Applications
stat.CO Statistics - Computation
stat.ML Statistics - Machine Learning
stat.ME Statistics - Methodology
stat.TH Statistics - Theory
q-bio.BM        Quantitative Biology - Biomolecules
q-bio.CB        Quantitative Biology - Cell Behavior
q-bio.GN        Quantitative Biology - Genomics
q-bio.MN        Quantitative Biology - Molecular Networks
q-bio.NC        Quantitative Biology - Neurons and Cognition
q-bio.OT        Quantitative Biology - Other
q-bio.PE        Quantitative Biology - Populations and Evolution
q-bio.QM        Quantitative Biology - Quantitative Methods
q-bio.SC        Quantitative Biology - Subcellular Processes
q-bio.TO        Quantitative Biology - Tissues and Organs
cs.AR   Computer Science - Architecture
cs.AI   Computer Science - Artificial Intelligence
cs.CL   Computer Science - Computation and Language
cs.CC   Computer Science - Computational Complexity
cs.CE   Computer Science - Computational Engineering; Finance; and Science
cs.CG   Computer Science - Computational Geometry
cs.GT   Computer Science - Computer Science and Game Theory
cs.CV   Computer Science - Computer Vision and Pattern Recognition
cs.CY   Computer Science - Computers and Society
cs.CR   Computer Science - Cryptography and Security
cs.DS   Computer Science - Data Structures and Algorithms
cs.DB   Computer Science - Databases
cs.DL   Computer Science - Digital Libraries
cs.DM   Computer Science - Discrete Mathematics
cs.DC   Computer Science - Distributed; Parallel; and Cluster Computing
cs.GL   Computer Science - General Literature
cs.GR   Computer Science - Graphics
cs.HC   Computer Science - Human-Computer Interaction
cs.IR   Computer Science - Information Retrieval
cs.IT   Computer Science - Information Theory
cs.LG   Computer Science - Learning
cs.LO   Computer Science - Logic in Computer Science
cs.MS   Computer Science - Mathematical Software
cs.MA   Computer Science - Multiagent Systems
cs.MM   Computer Science - Multimedia
cs.NI   Computer Science - Networking and Internet Architecture
cs.NE   Computer Science - Neural and Evolutionary Computing
cs.NA   Computer Science - Numerical Analysis
cs.OS   Computer Science - Operating Systems
cs.OH   Computer Science - Other
cs.PF   Computer Science - Performance
cs.PL   Computer Science - Programming Languages
cs.RO   Computer Science - Robotics
cs.SE   Computer Science - Software Engineering
cs.SD   Computer Science - Sound
cs.SC   Computer Science - Symbolic Computation
nlin.AO Nonlinear Sciences - Adaptation and Self-Organizing Systems
nlin.CG Nonlinear Sciences - Cellular Automata and Lattice Gases
nlin.CD Nonlinear Sciences - Chaotic Dynamics
nlin.SI Nonlinear Sciences - Exactly Solvable and Integrable Systems
nlin.PS Nonlinear Sciences - Pattern Formation and Solitons
math.AG Mathematics - Algebraic Geometry
math.AT Mathematics - Algebraic Topology
math.AP Mathematics - Analysis of PDEs
math.CT Mathematics - Category Theory
math.CA Mathematics - Classical Analysis and ODEs
math.CO Mathematics - Combinatorics
math.AC Mathematics - Commutative Algebra
math.CV Mathematics - Complex Variables
math.DG Mathematics - Differential Geometry
math.DS Mathematics - Dynamical Systems
math.FA Mathematics - Functional Analysis
math.GM Mathematics - General Mathematics
math.GN Mathematics - General Topology
math.GT Mathematics - Geometric Topology
math.GR Mathematics - Group Theory
math.HO Mathematics - History and Overview
math.IT Mathematics - Information Theory
math.KT Mathematics - K-Theory and Homology
math.LO Mathematics - Logic
math.MP Mathematics - Mathematical Physics
math.MG Mathematics - Metric Geometry
math.NT Mathematics - Number Theory
math.NA Mathematics - Numerical Analysis
math.OA Mathematics - Operator Algebras
math.OC Mathematics - Optimization and Control
math.PR Mathematics - Probability
math.QA Mathematics - Quantum Algebra
math.RT Mathematics - Representation Theory
math.RA Mathematics - Rings and Algebras
math.SP Mathematics - Spectral Theory
math.ST Mathematics - Statistics
math.SG Mathematics - Symplectic Geometry
astro-ph        Astrophysics
cond-mat.dis-nn Physics - Disordered Systems and Neural Networks
cond-mat.mes-hall       Physics - Mesoscopic Systems and Quantum Hall Effect
cond-mat.mtrl-sci       Physics - Materials Science
cond-mat.other  Physics - Other
cond-mat.soft   Physics - Soft Condensed Matter
cond-mat.stat-mech      Physics - Statistical Mechanics
cond-mat.str-el Physics - Strongly Correlated Electrons
cond-mat.supr-con       Physics - Superconductivity
gr-qc   General Relativity and Quantum Cosmology
hep-ex  High Energy Physics - Experiment
hep-lat High Energy Physics - Lattice
hep-ph  High Energy Physics - Phenomenology
hep-th  High Energy Physics - Theory
math-ph Mathematical Physics
nucl-ex Nuclear Experiment
nucl-th Nuclear Theory
physics.acc-ph  Physics - Accelerator Physics
physics.ao-ph   Physics - Atmospheric and Oceanic Physics
physics.atom-ph Physics - Atomic Physics
physics.atm-clus        Physics - Atomic and Molecular Clusters
physics.bio-ph  Physics - Biological Physics
physics.chem-ph Physics - Chemical Physics
physics.class-ph        Physics - Classical Physics
physics.comp-ph Physics - Computational Physics
physics.data-an Physics - Data Analysis; Statistics and Probability
physics.flu-dyn Physics - Fluid Dynamics
physics.gen-ph  Physics - General Physics
physics.geo-ph  Physics - Geophysics
physics.hist-ph Physics - History of Physics
physics.ins-det Physics - Instrumentation and Detectors
physics.med-ph  Physics - Medical Physics
physics.optics  Physics - Optics
physics.ed-ph   Physics - Physics Education
physics.soc-ph  Physics - Physics and Society
physics.plasm-ph        Physics - Plasma Physics
physics.pop-ph  Physics - Popular Physics
physics.space-ph        Physics - Space Physics
quant-ph        Quantum Physics
'''

class ArxivSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'arxiv'
        self.utils = Utils()
        self.batch_size = 300
        self.load_history_files = 2
        self.incremental_mode = False
        self.rawid_version_dict = {}
        self.incremental_file = ''

    def encode_feedparser_dict(self, d):
        """   
        helper function to get rid of feedparser bs with a deep copy. 
        I hate when libs wrap simple things in their own classes.
        """
        if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
          j = {} 
          for k in d.keys():
            j[k] = self.encode_feedparser_dict(d[k])
          return j
        elif isinstance(d, list):
          l = []
          for k in d:
            l.append(self.encode_feedparser_dict(k))
          return l
        else:
          return d        

    def parse_arxiv_url(self, url):
        """ 
        examples is http://arxiv.org/abs/1512.08756v2
        we want to extract the raw id and the version
        """
        ix = url.rfind('/')
        idversion = url[ix+1:].strip() # extract just the id (and the version)
        if idversion.find('v') != -1:
            parts = idversion.split('v')
            assert len(parts) == 2, 'error parsing url ' + url
            return parts[0], int(parts[1])  
            #return idversion[0 : idversion.find('v')], 1
        return idversion , 1

    def getCounts(self):
        counts = []
        path = '../db/eecs/papers/arxiv'
        if os.path.exists(path) and os.path.isdir(path):
            for item in os.listdir(path):
                num = item.replace('arxiv', '')
                num = num[0 : num.rfind('-')]
                try:
                    num = int(num)
                except Exception:
                    continue
                counts.append(num)
            counts = sorted(counts, reverse=True)
        return counts

    def incrementalUpdate(self, all_papers):
        incremental_list = []
        for paper in all_papers:
            rawid, version = self.parse_arxiv_url(paper['id'])
            published = paper['published'][0 : paper['published'].find('T')].strip() 
            old_published = self.rawid_version_dict.items()[randint(0, len(self.rawid_version_dict) - 1)][1]
            if not self.rawid_version_dict.has_key(rawid): #and published >= old_published:
                #print published + ' >= ' + old_published
                print 'rawid ' + rawid + ' not in db'
                incremental_list.append(paper)
        print len(incremental_list)
        if len(incremental_list) > 0:
            incfile = self.open_db(self.incremental_file, True)
            self.savePapers(incfile, incremental_list, len(incremental_list))
            self.close_db(incfile)

            return True             
        return False

    def doWork(self):
        base_url = 'http://export.arxiv.org/api/query?' # base api query url
        #cats = ['cs.CV', 'cs.LG', 'cs.CL', 'cs.NE', 'stat.ML', 'cs.DC', 'cs.RO', 'cs.AI', 'cs.AR'] 
        #cats = ['cs.DC', 'cs.RO', 'cs.AI', 'cs.AR'] 

        for cats in [['cs.CV', 'cs.LG', 'cs.CL', 'cs.NE', 'stat.ML'], ['cs.DC', 'cs.RO', 'cs.AI', 'cs.AR']]:

            # main loop where we fetch the new results
            start = 0
            results_per_iteration = 100
            max_result = 18900
            search_query = ''
            for cat in cats:
                if cat == cats[len(cats) -1]:
                    search_query += 'cat:' + cat
                else:
                    search_query += 'cat:' + cat + '+OR+'

            print 'Searching arXiv for %s' % (search_query, )
            all_papers = []
            num_added_total = start
            exception = False
            counts = self.getCounts()
            print counts
            if len(counts) >  0 and counts[len(counts) - 1] == self.batch_size:
                self.incremental_mode = True
                start = 0
            if self.incremental_mode:
                print 'incremental update mode'
                if len(self.rawid_version_dict) == 0:
                    print 'loading history file'
                    files = []
                    for i in range(0, len(counts)):
                        files.append('../db/eecs/papers/arxiv/arxiv' + str(counts[i])+ '-arxiv2017')

                    for fileName in files:

                        f = open(fileName, 'rU')
                        lines = f.readlines()
                        for line in lines:
                            record = PaperRecord(line)
                            rawid, version = self.parse_arxiv_url(record.get_url().replace('.pdf', ''))
                            self.rawid_version_dict[str(rawid)] = record.get_published().strip()

                        f.close()
                for k, v in self.rawid_version_dict.items():
                    print k + ' ' + v
                print len(self.rawid_version_dict)

                self.incremental_file = self.get_file_name('eecs/papers/arxiv/arxiv' + str(self.getCounts()[0] + self.batch_size)+ '-inc', self.school)
                if os.path.exists(self.incremental_file):
                    os.remove(self.incremental_file)

            for i in range(start, max_result, results_per_iteration):
               
                print "Results %i - %i" % (i,i+results_per_iteration)
                query = 'search_query=%s&sortBy=lastUpdatedDate&start=%i&max_results=%i' % (search_query,
                                                                     i, results_per_iteration)
                response = None
                try:
                    print 'requesting ' + base_url+query
                    #response = urllib.urlopen(base_url+query).read()
                    response = requests.get(base_url+query).text
                except Exception as e:
                    exception = True
                    print e
                #response = self.requestWithProxy(base_url+query).text
                parse = feedparser.parse(response)
                num_added = 0
                num_skipped = 0
                for e in parse.entries:
            
                    j = self.encode_feedparser_dict(e)
              
                    # extract just the raw arxiv id and version for this paper
                    rawid, version = self.parse_arxiv_url(j['id'])
                    j['_rawid'] = rawid
                    j['_version'] = version
                    j['title'] = self.utils.removeDoubleSpace(j['title'].replace('\n', '')).strip()
                    print j['title'].encode('utf-8')
                    #print j['id'].replace('abs', 'pdf')
              
                    #print j['authors']
                    #print j['arxiv_primary_category']['term']
                    #print j['published']
                    #print j['summary'].replace('\n', '')
                    all_papers.append(j)
                    num_added += 1
                    num_added_total += 1
              
                if (i+results_per_iteration) % self.batch_size == 0 and exception == False:
                    if self.incremental_mode:
                        if self.incrementalUpdate(all_papers) == False:
                            all_papers = []
                            break
                    else:
                        id_stuff = str(max_result - num_added_total + self.batch_size)
                        self.save("eecs/papers/arxiv/arxiv" + id_stuff, all_papers, id_stuff)
                    all_papers = []
                #   print some information
                #print 'Added %d papers, already had %d.' % (num_added, num_skipped)
                if len(parse.entries) == 0:
                    print 'Received no results from arxiv. Rate limiting? Exitting. Restart later maybe.'
                    print response
                    break
            
            
                print 'Sleeping for %i seconds' % (30.0 , )
                time.sleep(30.0 + random.uniform(0, 3))  
            
            if self.incremental_mode:
                if len(all_papers) > 0:
                    self.incrementalUpdate(all_papers)
                self.processIncrementalFile()

            if not self.incremental_mode and len(all_papers) > 0 and exception == False:
                self.save("eecs/papers/arxiv/arxiv" + str(num_added_total), all_papers, num_added_total)

    def processIncrementalFile(self):
        if os.path.exists(self.incremental_file):
            f = open(self.incremental_file, 'rU')
            lines = f.readlines()
            f.close()

            if len(lines) >= self.batch_size:
                self.utils.sortLines(lines)
                while (len(lines) > 0):
                    write_lines = lines[len(lines) - self.batch_size : ]
                    counts = self.getCounts()
                    number = ''
                    if len(lines) < self.batch_size:
                        number = str(counts[0] + self.batch_size) + "-inc"
                    else:
                        number = str(counts[0] + self.batch_size)
                    self.saveIncrementalPapers(number, write_lines) 

                    lines = lines[0 : len(lines) - self.batch_size]
                os.remove(self.incremental_file)
                    
    def saveIncrementalPapers(self, fileNumber, lines):

        file_name = self.get_file_name("eecs/papers/arxiv/arxiv" + fileNumber, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp") 
        self.count = 0

        for line in lines:
            self.count += 1
            record = Record(line)
            rawid = self.parse_arxiv_url(record.get_url().strip())[0].replace('.', '-')
            self.write_db(f, 'arxiv-' + rawid, record.get_title().strip(), record.get_url().strip(),
                              record.get_describe().strip())


        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def save(self, subject, papers, id_stuff):
        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")

        self.savePapers(f, papers, id_stuff)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def savePapers(self, f, papers, id_stuff):
        self.count = 0

        for paper in papers:
            self.count += 1
            authors = "author:"
            for author in paper['authors']:
                if len(author['name'].strip()) < 35:
                    authors += author['name'].strip().replace('|', '')
                else:
                    authors += author['name'].strip()[0 : 20].replace('|', '')
                if author != paper['authors'][len(paper['authors']) - 1]:
                    authors += ", "
                 
            category = "category:"
            for tag in paper['tags']:
                if len(tag['term']) < 20:
                    category += tag['term'].replace('\n', '').replace(',', ' ').strip() + ' '

            published = "published:" + paper['published'][0 : paper['published'].find('T')]
            summary = "summary:" + self.utils.removeDoubleSpace(paper['summary'].replace('\n', ' ').replace('|', ' ')).strip()

            desc = 'id:' + paper['_rawid'].strip() + ' ' + authors + ' ' + category + ' ' + published + ' ' + summary + ' version:' + str(paper['_version'])
            
            self.write_db(f, 'arxiv-' + paper['_rawid'].replace('.', '-'), paper['title'],
                      paper['id'][0: paper['id'].rfind('v')].strip(), desc)


start = ArxivSpider()
start.doWork()
