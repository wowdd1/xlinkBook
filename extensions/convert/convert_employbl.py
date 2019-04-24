#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
import twitter
import os
import subprocess

placemarkList = []

def toKML(title, coordinates, homepage, description, earthUrl='', iconUrl=''):
    global placemarkList
    description = description.replace('"', '').replace("'", '').replace('\n', ' ').replace('\t', ' ').replace('&', '')
    title = title.replace('"', '').replace("'", '').replace('\n', ' ').replace('\t', ' ').replace('&', '')

    homepage = homepage.replace('"', '').replace("'", '').replace('\n', ' ').replace('\t', ' ')

    earthLink = ''
    iconLink = ''
    if earthUrl != '':
        earthLink = '<a href="' + earthUrl.encode('utf-8') + '">' + earthUrl.encode('utf-8') + '</a><br>'
    if iconUrl != '':
        iconLink = '<img src="' + iconUrl.encode('utf-8') + '" height="200" width="auto" />'
    result = '<Placemark>\n\
                  <name>' + title.encode('utf-8') + '</name>\n\
                  <description><![CDATA[' + iconLink + '<br><br><a href="' + homepage.encode('utf-8') + '">' + homepage.encode('utf-8') + '</a><br>' + earthLink  + description.encode('utf-8') + ']]></description>\n\
                  <styleUrl>#icon-1727-E65100</styleUrl>\n\
                  <ExtendedData>\n\
                    <Data name="gx_media_links">\n\
                      <value>' + iconUrl.encode('utf-8') + '</value>\n\
                    </Data>\n\
                  </ExtendedData>\n\
                  <Point>\n\
                    <coordinates>\n\
                      ' + coordinates.encode('utf-8') + ',0\n\
                    </coordinates>\n\
                  </Point>\n\
              </Placemark>\n'

    placemarkList.append(result)
def convert(source, crossrefQuery=''):

    global placemarkList

    locationList = ['San%20Francisco', 'East%20Bay', 'South%20Bay', 'North%20Bay', 'Peninsula', 'Sacramento']
    #locationList = ['South%20Bay', 'Peninsula', 'Sacramento']
    #locationList = ['San%20Francisco']
    #locationList = ['East%20Bay']
    #locationList = ['South%20Bay']
    #locationList = ['North%20Bay']
    #locationList = ['Peninsula']
    #locationList = ['Sacramento']
    placemarkList = []
    companyDict = {}
    for location in locationList:
        api = 'https://employbl.com/api/companies?tags=&location=' + location + '&page='
        r = requests.get(api + '1')
        jObj = json.loads(r.text)
    
        for item in jObj['data']:
            key = str(item['name']) + str(item['latitude']) + str(item['longitude'])
            #print key
            #print item
            
            if companyDict.has_key(key):
                #print 'has:' + key
                continue
            else:
                companyDict[key] = item['name']
            #print item['name']
            url = 'https://employbl.com/companies/' + item['name'].replace(' ', '-').encode('utf-8')
            #url = 'https://www.google.com/maps/@' + str(item['latitude']) + ',' + str(item['longitude'])
            url = 'https://earth.google.com/web/@' + str(item['latitude']) + ',' + str(item['longitude'])
            iconUrl = 'https://logo.clearbit.com/' + item['website']
            #toKML(item['name'], str(item['longitude']) + ',' + str(item['latitude']), 'http://' + item['website'], item['description'], earthUrl=url, iconUrl=iconUrl)
            line = ' | ' + item['name'].encode('utf-8') + ' |  ' + url + ' | website:homepage(http://' + item['website'].encode('utf-8') + ') description:' + item['description'].replace('\n\n', ' ').encode('utf-8') + ' ' + location
            print line

        
        page = 1
        while jObj['next_page_url'] != None:
            page += 1
            r = requests.get(api + str(page))
            jObj = json.loads(r.text)
            for item in jObj['data']:
                key = str(item['name']) + str(item['latitude']) + str(item['longitude'])
                #print key
                #print item

                if companyDict.has_key(key):
                    #print 'has:' + key
                    continue
                else:
                    companyDict[key] = item['name']
                url = 'https://employbl.com/companies/' + item['name'].replace(' ', '-').encode('utf-8')
                #url = 'https://www.google.com/maps/@' + str(item['latitude']) + ',' + str(item['longitude'])
                url = 'https://earth.google.com/web/@' + str(item['latitude']) + ',' + str(item['longitude'])
                iconUrl = 'https://logo.clearbit.com/' + item['website']
                toKML(item['name'], str(item['longitude']) + ',' + str(item['latitude']), 'http://' + item['website'], item['description'], earthUrl=url, iconUrl=iconUrl)

                line = ' | ' + item['name'].encode('utf-8') + ' |  ' + url + ' | website:homepage(http://' + item['website'].encode('utf-8') + ') description:' + item['description'].replace('\n\n', ' ').encode('utf-8') + ' ' + location
                print line


    if False and len(placemarkList) > 0:
        print 'export kml'
        kmlHead = '<?xml version="1.0" encoding="UTF-8"?>\n\
                  <kml xmlns="http://www.opengis.net/kml/2.2">\n\
                   <Document>\n\
                     <name>World</name>\n\
                     <description/>\n\
                     <Style id=\"icon-1727-E65100-normal\">\n\
                       <IconStyle>\n\
                         <color>ff0051e6</color>\n\
                         <scale>1</scale>\n\
                         <Icon>\n\
                           <href>https://logo.clearbit.com/www.adyen.com</href>\n\
                         </Icon>\n\
                       </IconStyle>\n\
                       <LabelStyle>\n\
                         <scale>0</scale>\n\
                       </LabelStyle>\n\
                     </Style>\n\
                     <Style id="icon-1727-E65100-highlight">\n\
                       <IconStyle>\n\
                         <color>ff0051e6</color>\n\
                         <scale>1</scale>\n\
                         <Icon>\n\
                           <href>https://logo.clearbit.com/www.adyen.com</href>\n\
                         </Icon>\n\
                       </IconStyle>\n\
                       <LabelStyle>\n\
                         <scale>1</scale>\n\
                       </LabelStyle>\n\
                     </Style>\n\
                     <StyleMap id="icon-1727-E65100">\n\
                       <Pair>\n\
                         <key>normal</key>\n\
                         <styleUrl>#icon-1727-E65100-normal</styleUrl>\n\
                       </Pair>\n\
                       <Pair>\n\
                         <key>highlight</key>\n\
                         <styleUrl>#icon-1727-E65100-highlight</styleUrl>\n\
                       </Pair>\n\
                     </StyleMap>\n\
                     <Folder>\n\
                       <name>Italy Walking Tours</name>'
        kmlEnd = ' </Folder>\n\
                    </Document>\n\
                    </kml>'

        subPlacemarkList = placemarkList

        first = True
        count = 0
        while len(placemarkList) > 0:
            count += 1
            if len(placemarkList) > 100:

                subPlacemarkList = placemarkList[0 : 100]
                placemarkList = placemarkList[100 :]
            else:
                subPlacemarkList = placemarkList
                placemarkList = []

            f = open('/Users/wowdd1/Downloads/kml' + str(count) + '.kml', 'w')
            f.write('\n'.join([kmlHead] + subPlacemarkList + [kmlEnd]))
            f.close()

        #subprocess.check_output("echo '" + '\n'.join(placemarkList) + "' > /Users/wowdd1/Downloads/kml.kml", shell=True)
      
    
    #return 'ok'

def main(argv):
    source = ''
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:', ["url", "crossrefQuery"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)

if __name__ == '__main__':
    main(sys.argv)