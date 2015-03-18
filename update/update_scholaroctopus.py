#!/usr/bin/env python


from spider import *

class ScholarOctopusSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'ScholarOctopus'

    def doWork(self):
        r = requests.get('http://cs.stanford.edu/people/karpathy/scholaroctopus/out.json')
        jobj = json.loads(r.text)
        paper_dict = {}
        for paper in jobj:
            key = paper['conference'] + '-' + str(paper['year'])
            if paper_dict.get(key, '')  == '':
                paper_dict[key] = []
            paper_dict[key].append(paper)

        for key, v in sorted([(k,paper_dict[k]) for k in sorted(paper_dict.keys())]):
            #print key + ' paper:' + str(len(paper_dict[key]))
            print 'processing ' + key
            file_name = self.get_file_name("eecs/" + self.school.lower() + '/' + key, self.school.lower())
            file_lines = self.countFileLineNum(file_name)
            if file_lines == len(v):
                print school + ' no need upgrade\n'
                return
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for paper in sorted(v, key=lambda item : item['title']):
                self.count += 1
                paper_id = key.lower() + '-' + str(self.count)
                self.write_db(f, paper_id, paper['title'], paper['pdf'], 'author:' + ', '.join(paper['authors']))
                print paper_id + ' ' + paper['title']

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

start = ScholarOctopusSpider()
start.doWork()
