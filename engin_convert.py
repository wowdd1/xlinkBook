#!/usr/bin/env python

import json
from record import PriorityRecord

data = '\
{"Google":{"icon":"https://www.google.com/favicon.ico","url":"https://www.google.com/search?q=%s","sub":{"Web":"https://www.google.com/search?q=%s","Images":"https://www.google.com/images?hl=en&source=imghp&q=%s","Videos":"https://www.google.com/search?q=%s&tbm=vid","News":"http://www.google.com/search?q=%s&tbs=nws:1","Maps":"http://maps.google.com/maps?q=%s","Books":"http://www.google.com/search?q=%s&tbs=bks:1","Shopping":"https://www.google.com/search?q=%s&tbm=shop","Define":"http://www.google.com/search?q=define:%s","Translate":"http://translate.google.com/translate_t?q=%s"}},"Bing":{"icon":"https://www.bing.com/favicon.ico","url":"https://bing.com/search?q=%s","sub":{"Web":"https://bing.com/search?q=%s","Images":"https://www.bing.com/images/search?q=%s","News":"https://www.bing.com/news/search?q=%s","Videos":"https://www.bing.com/videos/search?q=%s","Maps":"https://www.bing.com/maps/?q=%s"}},"Yahoo":{"icon":"http://www.yahoo.com/favicon.ico","url":"http://search.yahoo.com/search?p=%s","sub":{"Web":"http://search.yahoo.com/search?p=%s","Images":"http://images.search.yahoo.com/search/images?p=%s","News":"http://news.search.yahoo.com/search/news?p=%s","Videos":"http://video.search.yahoo.com/search/video?p=%s","Answers":"http://answers.yahoo.com/search/search_result?p=%s","Sports":"http://sports.search.yahoo.com/search?p=%s"}},"DuckDuckGo":{"icon":"https://duckduckgo.com/favicon.ico","url":"https://duckduckgo.com/?q=%s","sub":{}},"Wikipedia":{"icon":"http://www.wikipedia.org/favicon.ico","url":"http://www.wikipedia.org/w/index.php?search=%s","sub":{"Wikipedia":"http://www.wikipedia.org/w/index.php?search=%s","Dictionary":"http://wiktionary.org/w/index.php?search=%s","Wikinews":"http://wikinews.org/w/index.php?search=%s"}},"Videos":{"icon":"https://www.youtube.com/favicon.ico","url":"https://www.google.com/search?q=%s&tbm=vid","sub":{"Youtube":"https://www.youtube.com/results?search_query=%s","Hulu":"http://www.hulu.com/search?query=%s","Dailymotion":"http://www.dailymotion.com/relevance/search/%s","Metacafe":"http://www.metacafe.com/videos_about/%s","Vimeo":"http://vimeo.com/search?q=%s"}},"Twitter":{"icon":"https://twitter.com/favicon.ico","url":"https://twitter.com/search?q=%s","sub":{}},"WolframAlpha":{"icon":"http://www.wolframalpha.com/favicon.ico","url":"http://www.wolframalpha.com/input/?i=%s","sub":{}}}'

'''
f = open('/Users/zd/json')
jobj = json.loads(''.join(f.readlines()))

#print jobj

search_engin_dict = {}
f = open('db/metadata/engin_list')
for line in f.readlines():
    #print line.strip()
    record = PriorityRecord(line.strip())
    search_engin_dict[record.get_title().strip()] = record
f.close()

count = 0
search_engin_dict_new = {}
for j in jobj.keys():
    #print j
    #print jobj[j]['sub']
    for item in jobj[j]['sub'].items():
        count += 1
        priority = '0'
        title = item[0].strip()
        if title.find(',') != -1:
            priority = title[title.find(',') + 1 : ].strip()
            title = title[0 : title.find(',')] 
        if priority.strip() == '':
            priority = '0'
        if search_engin_dict.has_key(title) and priority == '0':
            priority = search_engin_dict[title].get_priority().strip()
        if search_engin_dict_new.has_key(title):
            line = search_engin_dict_new[title].line + ' ' + j
        else:
            line = 'engin-' + str(count) + ' | ' + title + ' | ' + item[1] + ' | priority:' + priority+ ' description:' + j
        search_engin_dict_new[title] = PriorityRecord(line)


count = 0
for k, record in  search_engin_dict_new.items():
    count += 1
    #print record.line.encode('utf-8')
    line = 'engin-' + str(count) + ' | ' + record.get_title().strip() + ' | ' + record.get_url().strip() + ' | ' + record.get_describe().strip()
    print line.encode('utf-8')
       

'''
search_engin_type_engin_dict = {}

f = open('db/metadata/engin_list')
for line in f.readlines():
    #print line.strip()
    record = PriorityRecord(line.strip())
    #print record.get_priority()
    #print record.get_description()
    if record.get_title() != '':
        desc = record.get_description().strip()
        categorys = desc.split(' ')
        for category in categorys:
            if search_engin_type_engin_dict.has_key(category):
                search_engin_type_engin_dict[category].append(record)
            else:
                search_engin_type_engin_dict[category] = [record]

#print search_engin_type_engin_dict

json_str = '{'
for category, records in search_engin_type_engin_dict.items():
    if category == '':
        continue
    json_str += '"' + category + '":{ "icon": "", "url":"", "sub":{'
    for r in records:
        #print r.line
        #print r.get_priority()
        url = r.get_url().strip()
        if url.find('%s') == -1:
            url += '%s'
        json_str += '"' + r.get_title().strip() + ',' + r.get_priority() + '":' + '"' + url + '"'
        if r != records[len(records) - 1]:
            json_str += ','
    json_str += '}}'
    if category != search_engin_type_engin_dict.items()[len(search_engin_type_engin_dict.items()) - 1][0]:
        json_str += ','
json_str += '}'
print json_str
f.close()
