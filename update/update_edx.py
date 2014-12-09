#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "edx/"
edx_subject = [\
"Architecture",
"Art & Culture",
"Biology & Life Sciences",
"Business & Management",
"Chemistry",
"Communication",
"Computer Science",
"Design",
"Economics & Finance",
"Education",
"Electronics",
"Energy & Earth Sciences",
"Engineering",
"Environmental Studies",
"Ethics",
"Food & Nutrition",
"Health & Safety",
"History",
"Humanities",
"Law",
"Literature",
"Math",
"Medicine",
"Music",
"Philanthropy",
"Philosophy & Ethics",
"Physics",
"Science",
"Social Sciences",
"Statistics & Data Analysis"]

#edx

def match_subject(subject, subjects):
    for sub in subjects:
        if sub != "" and sub.strip() == subject:
            return True

    return False


def getEdxOnlineCourse(subject, json_obj):
    for obj in json_obj:
        if match_subject(subject, obj["subjects"]):
            file_name = get_file_name(dir_name + subject)
            file_lines = countFileLineNum(file_name)
            f = open_db(file_name + ".tmp")
            count = 0

            print "processing json and write data to file..."
            for item in json_obj:
                title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
                title = delZh(title)
                count = count + 1
                write_db(f, item["code"].strip() + " " + title)
                write_db_url(url_f, item["code"].strip(), item["url"], title)

            close_db(f)
            if file_lines != count and count > 0:
                do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
            else:
                cancel_upgrade(file_name)
                print "no need upgrade\n" 
    



print "downloading edx course info"
r = requests.get("https://www.edx.org/search/api/all")


print "loading data..."
jobj = json.loads(r.text)

truncateUrlData(dir_name)
url_f = open_url_file(dir_name)


for subject in edx_subject:
    if subject != "":
        getEdxOnlineCourse(subject, jobj)

close_url_file(url_f)


