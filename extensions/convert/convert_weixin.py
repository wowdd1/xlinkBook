#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import re
import random


#https://github.com/Chyroc/WechatSogou 基于搜狗微信搜索的微信公众号爬虫接口


page_max = 27
def convert(source, crossrefQuery=''):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
    r = requests.get(source, headers=header)

    soup = BeautifulSoup(r.text)

    gzh = ''
    if source.find('sogou') != -1:
        p = soup.find('p', class_='info')
        gzh = p.text.encode('utf-8').replace('微信号：', '').strip()
    else:

        p = soup.find('p', class_='profile_account')

        gzh = p.text[p.text.find(':') + 1 :].strip().encode('utf-8')
    #gzh = 'gzh'
    if gzh != '':
        cookie = getCookie()
        getContent(cookie, gzlist=[gzh], maxPage=page_max)
    return


def getCookie():
    post = {}

    driver = webdriver.Chrome(executable_path='/Users/wowdd1/dev/xlb_env/xlinkbook/chromedriver')
    driver.get('https://mp.weixin.qq.com/')
    time.sleep(2)
    driver.find_element_by_xpath("./*//input[@name='account']").clear()
    driver.find_element_by_xpath("./*//input[@name='account']").send_keys('developergf@gmail.com')
    driver.find_element_by_xpath("./*//input[@name='password']").clear()
    driver.find_element_by_xpath("./*//input[@name='password']").send_keys('z19861111d')
    # 在自动输完密码之后记得点一下记住我
    time.sleep(2)
    driver.find_element_by_xpath("./*//a[@title='点击登录']").click()
    # 拿手机扫二维码！
    time.sleep(10)
    driver.get('https://mp.weixin.qq.com/')
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    #with open('cookie.txt', 'w+') as f:
    #    f.write(cookie_str)

    return cookie_str



def getContent(cookie, maxPage=20, gzlist=[]):
    
    url = 'https://mp.weixin.qq.com'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }

    #with open('cookie.txt', 'r', encoding='utf-8') as f:
    #    cookie = f.read()
    cookies = json.loads(cookie)
    response = requests.get(url=url, cookies=cookies)
    #print response.url
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    for query in gzlist:
        query_id = {
            'action': 'search_biz',
            'token' : token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5',
        }
        search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
        #print search_response
        lists = search_response.json().get('list')[0]
        fakeid = lists.get('fakeid')
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        max_num = appmsg_response.json().get('app_msg_cnt')
        if max_num == None:
            return
        num = int(int(max_num) / 5)
        begin = 0
        while num + 1 > 0 :
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            #print('翻页###################',begin)
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            if fakeid_list == None:
                return
            for item in fakeid_list:
                line = ' | ' + item['title'] + ' | ' + item['link'] + ' | '
                #print(item.get('link'))
                print line.encode('utf-8')
            num -= 1
            begin = int(begin)
            if begin / 5 >= maxPage:
                return
            begin+=5
            time.sleep(2)

def main(argv):
    source = ''
    crossrefQuery = ''
    global page_max
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:p:', ["url", "crossrefQuery", 'page_max'])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a
        if o in ('-p', '--page_max'):
            page_max = int(a)


    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    