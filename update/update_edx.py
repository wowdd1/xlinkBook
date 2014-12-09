#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from common import *

dir_name = "edx/"

#edx
print "downloading edx course info"
r = requests.get("https://www.edx.org/search/api/all")


print "loading data..."
jobj = json.loads(r.text)

truncateUrlData(dir_name)
url_f = open_url_file(dir_name)
file_name = get_file_name(dir_name + "eecs")
file_lines = countFileLineNum(file_name)
f = open_db(file_name + ".tmp")
count = 0

print "processing json and write data to file..."
for item in jobj:
    for subject in item["subjects"]:
        if subject == "Computer Science" or subject == "Electronics" or subject == "Statistics & Data Analysis":
            title = item["l"].strip() + " (" + item["schools"][0].strip() + ")"
            title = delZh(title)
            count = count + 1
            write_db(f, item["code"].strip() + " " + title)
            write_db_url(url_f, item["code"].strip(), item["url"], title)

close_db(f)
close_url_file(url_f)
if file_lines != count and count > 0:
    do_upgrade_db(file_name)
    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
else:
    cancel_upgrade(file_name)
    print "no need upgrade\n"



