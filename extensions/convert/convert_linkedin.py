#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)

from linkedin_v2 import linkedin


import subprocess


API_KEY = '81aiu9e423wugx'
API_SECRET = 'fULH60an5QJFLWw8'
RETURN_URL = 'http://localhost:5000/linkedin/callback'
application = None


def convert_v2(source, crossrefQuery='', token=''):
    global application

    if token == '':

        authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authorization_url = authentication.authorization_url

        authorization_url = authorization_url.replace('%20r_fullprofile', '').replace('%20rw_groups', '').replace('%20w_messages', '').replace('%20r_contactinfo', '').replace('%20r_network', '').replace('%20rw_nus', '%20w_share')

        #print authorization_url

        cmd = 'open "' + authorization_url + '"'
        print cmd
        msg = subprocess.check_output(cmd, shell=True)

    else:

        authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authentication.authorization_code = token


        access_token = authentication.get_access_token()

        print access_token[0]
        application = linkedin.LinkedInApplication(authentication=authentication, token=access_token[0])


    if application != None:

        print application.get_profile()


        #print application.get_profile(member_id='%5B%2213609%22%5D')


    return ''

def convert(source, crossrefQuery='', token=''):
    global application

    if token == '':

        authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authorization_url = authentication.authorization_url

        authorization_url = authorization_url.replace('%20r_fullprofile', '').replace('%20rw_groups', '').replace('%20w_messages', '').replace('%20r_contactinfo', '').replace('%20r_network', '%20rw_company_admin').replace('%20rw_nus', '%20w_share')

        #print authorization_url

        cmd = 'open "' + authorization_url + '"'
        print cmd
        msg = subprocess.check_output(cmd, shell=True)

    else:

        authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authentication.authorization_code = token


        access_token = authentication.get_access_token()

        print access_token[0]
        application = LinkedInApplication(authentication=authentication, token=access_token[0])


    if application != None:

        #print application.get_profile()

        #response = application.make_request('GET', 'https://api.linkedin.com/v1/people/~')



        #response = application.make_request('GET', 'https://api.linkedin.com/v1/companies::(universal-name=dog)')

        #https://stackoverflow.com/questions/30409219/linkedin-api-unable-to-view-any-company-profile
        response = application.get_companies(universal_names='naughty dog')


        print str(response)


    return ''

def convert_v3(source, crossrefQuery='', token=''):
    global application

    if token == '':

        authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authorization_url = authentication.authorization_url

        authorization_url = authorization_url.replace('%20r_fullprofile', '').replace('%20rw_groups', '').replace('%20w_messages', '').replace('%20r_contactinfo', '').replace('%20r_network', '').replace('%20rw_nus', '%20w_share')

        #print authorization_url

        cmd = 'open "' + authorization_url + '"'
        print cmd
        msg = subprocess.check_output(cmd, shell=True)

    else:

        authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())

        authentication.authorization_code = token


        access_token = authentication.get_access_token()

        print access_token[0]

        headers = {'auth' : token}

        r = requests.get('https://api.linkedin.com/v2/me?oauth2_access_token=' + access_token[0], headers=headers)

        print r.text

    return ''


def main(argv):
    source = ''
    crossrefQuery = ''
    token = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:t:', ["url", "crossrefQuery", 'token'])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a
        if o in ('-t', '--token'):
            token = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery, token=token)


if __name__ == '__main__':
    main(sys.argv)
    