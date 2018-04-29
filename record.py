#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08
#utf-8 gb2312

from config import Config
import os


class Record():
    default_line = " | | | "
    def __init__(self, line):
        self.line = line
        if line == "":
            self.line = self.default_line
        if line.find('|') == -1:
            self.line =  " | " + line.replace('\n', '') + " | | "
        self.file_path = ''

    def set_path(self, path):
        self.file_path = path[path.find('db') : ]

    def get_path(self):
        return self.file_path

    def get_default_line(self):
        return self.default_line

    def get_pos(self, pos):
        if pos == 1:
            return self.line.find('|')
        else:
            return self.line.find('|', self.get_pos(pos - 1) + 1)
        return -1 

    def get_id(self):
        return self.line[0 : self.get_pos(1)]

    def get_title(self):
        return self.line[self.get_pos(1) + 1 : self.get_pos(2)]

    def get_url(self):
        url = self.line[self.get_pos(2) + 1 : self.get_pos(3)]
        if url != None and url.find(Config.ip_adress) != -1:
            url = url.strip()
            if url.find('column=') == -1:
                url += '&column=' + Config.column_num
            if url.find('width=') == -1:
                url += '&width=' + Config.default_width

        return url            

    def get_describe(self):
        desc = self.line[self.get_pos(3) + 1 : ].replace('|', '').replace('\n', '')
        #if Config.hiden_record_id:
        #    desc = 'id:' + self.get_id().strip() + ' ' + desc
        if desc.startswith(' ') == False:
            desc = ' ' + desc
        return desc

    def get_desc_field(self, utils, resourceType, resourceField, toDesc=False):

        if resourceType != '':
            rtValue = utils.reflection_call('record', 'WrapRecord', 'get_tag_content', self.line, {'tag' : resourceType})
            #print '===' + rtValue
            if rtValue != None and rtValue.find(resourceField + '(') != -1:
                itemList = []
                if rtValue.find(',') != -1:
                    itemList = rtValue.split(',')
                else:
                    itemList = [rtValue]
                for rtItem in itemList:
                    if rtItem.strip().startswith(resourceField + '('):
                        if toDesc:
                            print ')))))))'
                            desc = utils.valueText2Desc(rtItem, prefix=False)
                            print desc
                            return desc
                        else:
                            return rtItem
        return ''

    def get_desc_field2(self, utils, resourceField, tagList, library='', toDesc=False, prefix=True):
        desc = self.get_describe()

        print resourceField

        resourceField = resourceField.lower()
        start = 0
        data = ''
        while True:

            end = utils.next_pos(desc, start, 1000, tagList, library=library) 

            if end > 0:
                item = desc[start : end].encode('utf-8')
    
                if item.lower().find(resourceField + '(') != -1:
                    dataSplit = []
                    #print '++++++++'
                    
                    if item.find(',') != -1:
                        dataSplit = item.split(',')
                    else:
                        dataSplit = [item]
                    for d in dataSplit:
                        d = d.strip()
                        print d
                        if d.lower().find(':' + resourceField + '(') != -1:
                            data = d[d.lower().find(':' + resourceField + '(') + 1 :]
                            break
                        elif d.lower().startswith(resourceField + '('):
                            data = d
                            break
                    if data != '' and toDesc:
                        data = utils.valueText2Desc(data, prefix=prefix)

                start = end

            if end >= len(desc):
                break

        return data



    def get_desc_field3(self, utils, resourceField, tagList, library='', toDesc=False, prefix=True):
        desc = self.get_describe()

        print resourceField

        resourceField = resourceField.lower()
        start = 0
        dataList = []


        resourceType = ''
        while True:

            end = utils.next_pos(desc, start, 1000, tagList, library=library) 

            if end > 0:
                item = desc[start : end].encode('utf-8')
                item = item[item.find(':') + 1 :]
    
                if item.lower().find(resourceField) != -1:
                    dataSplit = []
                    #print '++++++++'
                    #print item
                    resourceType = item[0 : item.find(':')].strip()
                    data = ''
                    data2 = ''
                    data2Pre = resourceType
                    if item.find(',') != -1:
                        dataSplit = item.split(',')
                    else:
                        dataSplit = [item]
                    #print dataSplit
                    for d in dataSplit:
                        d = d.strip()
                        value = ''
                        text = ''
                        if utils.getValueOrTextCheck(d):
                            value = utils.getValueOrText(d, returnType='value')
                            text = utils.getValueOrText(d, returnType='text')                    
                        #print '---111->' + d
                        if d.lower().startswith(resourceField + '(') or text.lower().find(resourceField) != -1:
                            #print '---333->' + d
                            data = self.connectField(data, d)
                            break
                        elif utils.getValueOrTextCheck(d):
                            #print '---444->' + d

                            if text.lower().find(resourceField) != -1:
                                print '---555->' + d
                                data2 = self.connectField(data2, d)
                                continue                        
                            elif value.lower().find(resourceField) != -1:
                                d = self.get_desc_field3_value2data(utils, value, resourceField, d)
                                #print '---666->' + d
                                data2 = self.connectField(data2, d)
                                continue


                    if data != '':
                        #print data
                        data = self.vaildField(data)
                        if toDesc:
                            dataList.append(utils.valueText2Desc(data, prefix=prefix))
                        else:
                            dataList(data)
                        data = ''
                    
                    if data2 != '':
                        data2 = self.vaildField(data2)
                        print 'resourceType--->' + resourceType
                        print 'data2<---' + data2
                        if utils.getValueOrTextCheck(data2):

                            if data2.find('+') != -1:
                                data2 = data2
                                print 'data221<---' + data2
                            else:
                                value = utils.getValueOrText(data2, returnType='value')
                                if utils.getValueOrTextCheck(value):
                                    #print 'dadasd--->' + data2
                                    data2 = data2
                                else:
                                    data2 = resourceField + '(' + data2Pre + '+' + data2 + ')'
                        

                        else:
                            data2 = resourceField + '(' + data2Pre + '+' + data2 + ')'
                        
                            print 'data222<---' + data2
                        if toDesc:
                            for d in self.validFieldList(data2):
                                dataList.append(utils.valueText2Desc(d, prefix=prefix))
                        else:
                            dataList(data2)
                    
                        
                start = end

            if end >= len(desc):
                break



        return dataList

    def connectField(self, data, field):
        if data != '':
            return data + '+' + field
        else:
            return data + field + '+'

    def vaildField(self, data):
        #print '---->vaildField:' + data
        data = data.replace('++', '+')
        if data.endswith('+'):
            data = data[0 : len(data) - 1]


        return data

    def validFieldList(self, data2):

        #print 'validFieldList:' + data2
        fList = []
        if data2.find('))+') != -1:
            while data2.find('))+') != -1:
                data = data2[0 : data2.find('))+') + 2]
                data2 = data2[data2.find('))+') + 3 :]
                fList.append(self.vaildField(data))

            if data2 != '':
                fList.append(data2)
        else:
            fList.append(self.vaildField(data2))

        return fList




    def get_desc_field3_value2data(self, utils, value, resourceField, originData):

        print 'begin----->' + value
        data = ''
        valueList = []
        originText = utils.getValueOrText(originData, returnType='text')

        if value.find('+') != -1:
            valueList = value.split('+')
        else:
            valueList = [value]
        #print valueList
        for v in valueList:
            if utils.getValueOrTextCheck(v):
                text = utils.getValueOrText(v, returnType='text')
                value = utils.getValueOrText(v, returnType='value')
                #print text
                if text.lower().find(resourceField) != -1:

                    #print originData
                    if utils.isAccountTag(originText, utils.tag.tag_list_account):
                        data += originData + '+'
                    else:    
                        data += v + '+'
                    #print 'data-->' + data
                elif value.lower().find(resourceField) != -1:
                    #print 'value--====>' + value
                    if value.find('+') == -1 and value.find('*') != -1:
                        if utils.getValueOrTextCheck(v):
                            text = utils.getValueOrText(v, returnType='text')
                            value = utils.getValueOrText(v, returnType='value')
                        subValue = ''
                        for v in value.split('*'):
                            if v.lower().find(resourceField) != -1:
                                subValue += v + '*'
                        if subValue.endswith('*'):
                            subValue = subValue[0: len(subValue) - 1]

                        #print 'subValue=====>' + subValue
                        result = text + '(' + subValue + ')'

                        #print 'result--===>' + result
                        if result != '':
                            data += result + '+'
                    elif utils.getValueOrTextCheck(value):

                        subText = utils.getValueOrText(v, returnType='text')
                        subValue = utils.getValueOrText(v, returnType='value')
                        

                        result = self.get_desc_field3_value2data(utils, subValue, resourceField, v)

                        #print 'result-->' + result
                        if result != '':
                            data += self.vaildField(result) + '+'
                    else:
                        #print 'v--===>' + v
                        data += v + '+'
                        print data 
            else:

                if v.lower().find(resourceField.lower()) != -1:

                    print 'originData--->' + originData
                    return originData
                #data += v + '+'

        data = self.vaildField(data)
        print 'end----->' + data
        return data


    def editRecord(self, utils, rID, record, originFileName, library, resourceType=''):

        newid = record.get_id().strip()
        title = record.get_title().strip()
        url = record.get_url().strip()
        desc = record.get_describe().strip()

        newline = ''
        if rID.startswith('custom-') and newid != None:
            desc = desc.replace('id:' + newid, '').strip()
            newline = newid + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        else:
            newline = rID + ' | ' + title + ' | ' + url + ' | ' + desc + '\n'
        print 'newline:'
        print newline
        if os.path.exists(library):
            f = open(library, 'rU')
            all_lines = []
            for line in f.readlines():
                if rID != line[0 : line.find('|')].strip():
                    all_lines.append(line)
                else:
                    print 'old line:'
                    print line
                    all_lines.append(newline)

                    form = utils.getExtensionCommandArgs(rID, '', '', 'record', 'history', 'sync', library)
                    form['oldLine'] = line
                    form['newLine'] = newline
                    form['resourceType'] = resourceType
                    #print form
                    utils.handleExtension(form)
                    #self.syncHistory(line, newline, originFileName)
            f.close()

            utils.write2File(library, all_lines)
            
            return True
        return False    

    def getHistoryFile(self, fileName):
        if fileName.find('/') != -1:
            fileName = fileName[fileName.rfind('/') + 1 :]
        return 'extensions/history/data/'+ fileName + '-history'



    def edit_desc_field2(self, utils, record, resourceType, fieldName, editedData, tagList, library=''):
        editRID = record.get_id().strip()
        title = record.get_title().strip()
        url = record.get_url().strip()
        desc = record.get_describe().strip()
        if resourceType != None:
            resourceType = resourceType.strip()
        
        newData = 'id:' + editRID + ' title:' + title + ' url:' + url + ' ' 

        start = 0
        #print 'resourceType:' + resourceType    
        #print 'fieldName:' + fieldName
        #print desc
        print '---------------------->'
        while True:

            end = utils.next_pos(desc, start, 1000, tagList, library=library) 

            if end > 0:
                item = desc[start : end]

                #print 'item:' + item
                #print fieldName+'('
                #print 'index:' + str(item.find(fieldName+'('))
                index = item.lower().find(fieldName.lower() + '(')

                if resourceType != None and resourceType != '' and item.strip().startswith(resourceType + ':') == False and index == -1:
                    #print '========'

                    #print item.strip()
                    #print resourceType + ':'
                    #print item.strip().startswith(resourceType + ':')

                    newData += ' ' + item.strip()
                elif index != -1:
                    dataSplit = []
                    #print '++++++++'
                    if item.find(',') != -1:
                        dataSplit = item.split(',')
                    else:
                        dataSplit = [item]


                    data = ''
                    count = 0
                    print dataSplit
                    for d in dataSplit:
                        #print 'd--->' + d
                        count += 1
                        d = d.strip()

                        if d.find(':' + fieldName + '(') != -1:
                            print '---->' + data
                            data += d[0 : d.find(':' + fieldName + '(') + 1] + editedData

                            print '<----' + data
                        elif d.startswith(fieldName + '('):
                            print '---->' + data
                            data += editedData
                            print '<----' + data
                        else:
                            data += d
                        if count != len(dataSplit):
                            data += ', '

                        #print d

                    newData += ' ' + data.strip() 

                else:
                    newData += ' ' + item.strip()
                
                start = end

            if end >= len(desc):
                break

        print '<----------------------'

        #print newData



        '''
        dataSplit =  desc.split(',')
        count = 0
        for item in dataSplit:
            count += 1

            start = item.find(fieldName+'(')
            if start != -1:

                frontData = ''
                endData = ''

                dataPart = []

                end = utils.next_pos(item, 0, 1000, tagList, library=library) 
                if end > 0:

                    endData = item[end :]
                    item = item[0 : end]
                #print '---->' + item
                newItem = item.strip()
                start = newItem.find(fieldName+'(')
                
                if start == 0:
                    newData += ' ' + editedData.strip()
                else:
                    newData += item[0: item.find(':'+fieldName+'(') + 1] + editedData

                if endData != '':
                    newData = newData.strip() + ' ' + endData
                #print '---->' + newData

            else:
                newData += item

            if count != len(dataSplit):
                newData += ','
        print newData
        '''
        return newData

    def edit_desc_field():

        return False

    def valid(self, line):
        pos = line.find('|')
        if pos != -1:
            pos = line.find('|', pos + 1)
        else:
            pos = -1
        if pos != -1:
            pos = line.find('|', pos + 1)
        else:
            pos = -1
        if pos != -1:
            return True
        print line + ' ' + str(pos)
        return False
        

class Category():
    def __init__(self):
        self.book = "book"
        self.journal = "journal"
        self.paper = "paper"
        self.course = "course"
        self.project = "project"
        self.slide = "slide"
        self.code = "code"
        self.dataset = "dataset"
        self.patent = "patent"
        self.people = "people"
        self.blog = "blog"
        self.review = "review"
        self.website = "website"
        self.engin = "engin"
        self.tools = "tools"

    def match(self, desc, category):
        index = desc.find('category:')
        if index != -1 and desc.find(category, index + 1) != -1:
            print category + ' match'
            return True
        print  category + ' not match ' + desc
        return False

    def containMatch(self, key, category):
        if key.find(category) != -1:
            print category + ' match'
            return True
        return False

class Tag():
    def __init__(self):
        self.tag_id = "id:"
        self.tag_title = 'title:'
        self.tag_url = 'url:'
        self.tag_videourl = 'videourl:'
        self.tag_author = 'author:'
        self.tag_winner = "winner:"
        self.tag_ratings = 'ratings:'
        self.tag_term = 'term:'
        self.tag_prereq = 'prereq:'
        self.tag_prerequisites = 'prerequisites:'
        self.tag_toprepo = 'toprepo:'
        self.tag_project = 'project:'
        self.tag_university = 'university:'
        self.tag_available = 'available:'
        self.tag_level = 'level:'
        self.tag_features = 'features:'
        self.tag_instructors = 'instructors:'
        self.tag_professor = 'professor:'
        self.tag_faculty = 'faculty:'
        self.tag_investigator = 'investigator:'
        self.tag_researcher = 'researcher:'
        self.tag_adviser = 'adviser:'
        self.tag_scientist = 'scientist:'
        self.tag_phd = 'phd:'
        self.tag_people = 'people:'
        self.tag_follow = 'follow:'
        self.tag_description = 'description:'
        self.tag_textbook = 'textbook:'
        self.tag_book = 'book:'
        self.tag_bible = 'bible:'
        self.tag_paper = 'paper:'
        self.tag_homepage = 'homepage:'
        self.tag_organization = 'organization:'
        self.tag_platform = 'platform:'
        self.tag_specialization = 'specialization:'
        self.tag_journal = "journal:"
        self.tag_tutorial = 'tutorial:'
        self.tag_dataset = 'dataset:'

        self.tag_priority = "priority:"
        self.tag_parentid = "parentid:"
       
        self.tag_category = "category:"
        self.tag_summary = "summary:"
        self.tag_published = "published:"
        self.tag_version = "version:"

        self.tag_path = "path:"
        self.tag_icon = "icon:"

        self.tag_shortname = "shortname:"

        self.tag_ceo = 'ceo:'
        self.tag_cso = 'cso:'
        self.tag_cto = 'cto:'
        self.tag_cio = "cio:"
        self.tag_cfo = 'cfo:'
        self.tag_cmo = 'cmo:'
        self.tag_cco = 'cco:'
        self.tag_cbo = 'cbo:'
        self.tag_coo = 'coo:'
        self.tag_cpo = 'cpo:'
        self.tag_founder = 'founder:'
        self.tag_vp = 'vp:'
        self.tag_investor = 'investor:'
        self.tag_stockholder = 'stockholder:'
        self.tag_foundation = 'foundation:'
        self.tag_programmer = 'programmer:'
        self.tag_engineer = 'engineer:'
        self.tag_developer = 'developer:'
        self.tag_hacker = 'hacker:'
        self.tag_product = "product:"
        self.tag_designer = 'designer:'
        self.tag_artist = 'artist:'
        self.tag_writer = 'writer:'
        self.tag_leader = 'leader:'
        self.tag_director = 'director:'
        self.tag_consultant = 'consultant:'
        self.tag_community = 'community:'
        self.tag_conference = 'conference:'
        self.tag_workshop = 'workshop:'
        self.tag_challenge = 'challenge:'
        self.tag_company = 'company:'
        self.tag_startup = 'startup:'
        self.tag_lab = 'lab:'
        self.tag_team = 'team:'
        self.tag_institute = 'institute:'
        self.tag_foundation = 'foundation:'
        self.tag_summit = 'summit:'
        self.tag_alias = 'alias:'
        self.tag_slack = 'slack:'
        self.tag_workast = 'workast:'
        self.tag_gitter = 'gitter:'
        self.tag_twitter = 'twitter:'
        self.tag_mastodon = 'mastodon:'
        self.tag_social_tag = 'social-tag:'
        self.tag_youtube = 'youtube:'
        self.tag_github = 'github:'
        self.tag_gitlab = 'gitlab:'
        self.tag_insight = 'insight:'
        self.tag_vimeo = 'vimeo:'
        self.tag_g_group = 'g-group:'
        self.tag_g_plus = 'g-plus:'
        self.tag_medium = 'medium:'
        self.tag_goodreads = 'goodreads:'
        self.tag_fb_group = 'fb-group:'
        self.tag_fb_pages = 'fb-pages:'
        self.tag_meetup = 'meetup:'
        self.tag_huodongxing = "huodongxing:"
        self.tag_y_video = 'y-video:'
        self.tag_y_channel = 'y-channel:'
        self.tag_y_channel2 = 'y-channel2:'
        self.tag_y_playlist = 'y-playlist:'
        self.tag_award = 'award:'
        self.tag_website = 'website:'
        self.tag_url = 'url:'
        self.tag_memkite = 'memkite:'
        self.tag_blog = 'blog:'
        self.tag_linkedin = 'linkedin:'
        self.tag_l_group = 'l-group:'
        self.tag_alternativeto = 'alternativeto:'
        self.tag_clone = 'clone:'
        self.tag_docker = 'docker:'
        self.tag_stackexchange = 'stackexchange:'
        self.tag_zhihu = 'zhihu:'
        self.tag_t_zhihu = 't-zhihu:'
        self.tag_z_zhihu = 'z-zhihu:'
        self.tag_c_zhihu = 'c-zhihu:'
        self.tag_blogspot = 'blogspot:'
        self.tag_bitbucket = 'bitbucket:'
        self.tag_sourceforge = 'sourceforge:'
        self.tag_business = 'business:'
        self.tag_country = 'country:'
        self.tag_price = "price:"
        self.tag_date = 'date:'
        self.tag_advisor = 'advisor:'
        self.tag_intern = 'intern:'
        self.tag_facebook = 'facebook:'
        self.tag_vk = 'vk:'
        self.tag_reddit = 'reddit:'
        self.tag_weibo = 'weibo:'
        self.tag_job = 'job:'
        self.tag_alliance = 'alliance:'
        self.tag_slideshare = 'slideshare:'
        self.tag_crossref = 'crossref:'
        self.tag_contentref = 'contentref:'
        self.tag_vimeopro = 'vimeopro:'
        self.tag_atlassian = 'atlassian:'
        self.tag_weixin = 'weixin:'
        self.tag_qq_group = 'qq-group:'
        self.tag_discuss = 'discuss:'
        self.tag_localdb = 'localdb:'
        self.tag_engintype = 'engintype:'
        self.tag_keyword = 'keyword:'
        self.tag_udacity = 'udacity:'
        self.tag_review = 'review:'
        self.tag_instagram = 'instagram:'
        self.tag_leiphone = 'leiphone:'
        self.tag_businessinsider = 'businessinsider:'
        self.tag_freenode = 'freenode:'
        self.tag_videolectures = 'videolectures:'
        self.tag_techtalks = 'techtalks:'
        self.tag_universe = 'universe:'
        self.tag_agent = 'agent:'
        self.tag_survey = 'survey:'
        self.tag_series = 'series:'
        self.tag_specialization = 'specialization:'
        self.tag_program = 'program:'
        self.tag_douyu = 'douyu:'
        self.tag_digg = 'digg:'
        self.tag_twitch = 'twitch:'
        self.tag_steam = 'steam:'
        self.tag_ustream = 'ustream:'
        self.tag_csdnlib = 'csdnlib:'
        self.tag_blogcsdn = 'blog.csdn:'
        self.tag_cnblog = 'cnblog:'
        self.tag_iqiyi = 'iqiyi:'
        self.tag_flipboard = 'flipboard:'
        self.tag_channel9 = 'channel9:'
        self.tag_panopto = 'panopto:'
        self.tag_piazza = 'piazza:'
        self.tag_expert = 'expert:'
        self.tag_pcpartpicker = 'pcpartpicker:'
        self.tag_baijiahao = 'baijiahao:'
        self.tag_dean = "dean:"
        self.tag_jianshu = "jianshu:"
        self.tag_15yan = '15yan:'
        self.tag_nucleus = 'nucleus:'
        self.tag_youku = 'youku:'
        self.tag_zaker = 'zaker:'
        self.tag_v_qq = 'v-qq:'
        self.tag_sohu = 'sohu:'
        self.tag_nbviewer = 'nbviewer:'
        self.tag_flagship = 'flagship:'
        self.tag_toutiao = 'toutiao:'
        self.tag_leaderboard = 'leaderboard:'
        self.tag_benchmark = 'benchmark:'
        self.tag_baiduyun = 'baiduyun:'
        self.tag_inke = 'inke:'
        self.tag_sayit = 'sayit:'
        self.tag_kaggle = 'kaggle:'
        self.tag_soundcloud = 'soundcloud:'
        self.tag_expo = 'expo:'
        self.tag_bilibili = 'bilibili:'
        self.tag_acfun = 'acfun:'
        self.tag_archive_org = 'archive.org:'
        self.tag_zeef = 'zeef:'
        self.tag_g_cores = 'g-cores:'
        self.tag_tieba = 'tieba:'
        self.tag_discord = 'discord:'
        self.tag_mixer = 'mixer:'
        self.tag_periscope = 'periscope:'
        self.tag_flickr = 'flickr:'
        self.tag_vine = 'vine:'
        self.tag_tudou = 'tudou:'
        self.tag_patreon = 'patreon:'
        self.tag_g_youtube = 'g-youtube:'
        self.tag_douban = 'douban:'
        self.tag_doulist = 'doulist:'
        self.tag_click_count = 'clickcount:'
        self.tag_artstation = 'artstation:'
        self.tag_appveyor = 'appveyor:'
        self.tag_gamesradar = 'gamesradar:'
        self.tag_opencollective = 'opencollective:'
        self.tag_gamejolt = 'gamejolt:'
        self.tag_onetab = 'onetab:'
        self.tag_nico = 'nico:'
        self.tag_wordpress = 'wordpress:'
        self.tag_photobucket = 'photobucket:'
        self.tag_stumble = 'stumble:'
        self.tag_disqus = 'disqus:'
        self.tag_waffle = 'waffle:'
        self.tag_pinterest = 'pinterest:'
        self.tag_deviantart = 'deviantart:'

        #for multimedia
        self.tag_co_president = "co-president:"
        self.tag_creative_director = "creative-director:"
        self.tag_art_director = "art-director:"
        self.tag_game_director = "game-director:"
        self.tag_editor = "editor:"
        self.tag_lead_programmer = "lead-programmer:"
        self.tag_programmer = "programmer:"
        self.tag_graphics_programmer = "graphics-programmer:"
        self.tag_lead_game_designer = "lead-game-designer:"
        self.tag_game_designer = "game-designer:"
        self.tag_user_interface_designer = "user-interface-designer:"
        self.tag_lead_artist = "lead-artist:"
        self.tag_lead_character_artist = "lead-character-artist:"
        self.tag_concept_artist = "concept-artist:"
        self.tag_lead_animation = "lead-animation:"
        self.tag_lead_gameplay_animator = "lead-gameplay-animator:"
        self.tag_animator = "animator:"
        self.tag_musician_composer = "musician-composer:"
        self.tag_lead_audio = "lead-audio:"
        self.tag_lead_environment_artist = "lead-environment-artist:"
        self.tag_environment_artist = "environment-artist:"
        self.tag_lead_lighting_artist = "lead-lighting-artist:"
        self.tag_lighting_artist = "lighting-artist:"
        self.tag_lead_visual_effects_artist = "lead-visual-effects-artist:"
        self.tag_visual_effects_artist = "visual-effects-artist:"
        self.tag_single_player_quality = "single-player-quality:"
        self.tag_assurance_manager = "assurance-manager:"
        self.tag_technical_art_director = "technical-art-director:"
        self.tag_actor = "actor:"
        self.tag_communication_director = "communication-director:"
        self.tag_lead_designer = "lead-designer:"
        self.tag_lead_cinematic_animator = "lead-cinematic-animator:"
        self.tag_publisher = 'publisher:'
        self.tag_studio = 'studio:'
        self.tag_producer = 'producer:'
        #for multimedia

        game_tags = [self.tag_co_president, self.tag_creative_director, self.tag_art_director, self.tag_game_director, self.tag_editor, self.tag_lead_programmer, self.tag_programmer, self.tag_graphics_programmer, self.tag_lead_game_designer, self.tag_game_designer, self.tag_user_interface_designer, self.tag_lead_artist, self.tag_lead_character_artist, self.tag_concept_artist, self.tag_lead_animation, self.tag_lead_gameplay_animator, self.tag_animator, self.tag_musician_composer, self.tag_lead_audio, self.tag_lead_environment_artist, self.tag_environment_artist, self.tag_lead_lighting_artist, self.tag_lighting_artist, self.tag_lead_visual_effects_artist, self.tag_visual_effects_artist, self.tag_single_player_quality, self.tag_assurance_manager, self.tag_technical_art_director, self.tag_actor, self.tag_communication_director, self.tag_lead_designer, self.tag_lead_cinematic_animator, self.tag_publisher, self.tag_studio, self.tag_producer]

        self.tag_map = {'multimedia-library' : game_tags, '3A-game-library' : game_tags}


        self.tag_list = [self.tag_id, self.tag_title, self.tag_url, self.tag_videourl, self.tag_author, self.tag_winner, self.tag_ratings, self.tag_term,\
                         self.tag_prereq, self.tag_prerequisites, self.tag_toprepo, self.tag_project, self.tag_university,\
                         self.tag_available, self.tag_level, self.tag_features, self.tag_instructors, self.tag_professor,\
                         self.tag_faculty, self.tag_investigator, self.tag_researcher, self.tag_adviser, self.tag_scientist, self.tag_phd, \
                         self.tag_people, self.tag_follow, self.tag_description, self.tag_textbook, self.tag_book, self.tag_bible, self.tag_paper, \
                         self.tag_homepage, self.tag_organization, self.tag_platform, self.tag_specialization, self.tag_journal, self.tag_tutorial, \
                         self.tag_dataset, self.tag_priority, self.tag_parentid, self.tag_category, self.tag_summary, self.tag_published, self.tag_version, \
                         self.tag_path, self.tag_icon, self.tag_shortname, self.tag_ceo, self.tag_cso, self.tag_cto, self.tag_cio, self.tag_cfo, self.tag_cmo, \
                         self.tag_cco, self.tag_cbo, self.tag_coo, self.tag_cpo, self.tag_founder, self.tag_vp, self.tag_investor, self.tag_stockholder, self.tag_foundation, \
                         self.tag_programmer, self.tag_engineer, self.tag_developer, self.tag_hacker, self.tag_product, self.tag_designer, self.tag_artist, self.tag_writer, \
                         self.tag_leader, self.tag_director, self.tag_community, self.tag_conference, self.tag_workshop, self.tag_challenge, self.tag_company, self.tag_startup, \
                         self.tag_lab, self.tag_team, self.tag_institute, self.tag_foundation, self.tag_summit, self.tag_alias, self.tag_slack, self.tag_workast, self.tag_gitter, self.tag_twitter, self.tag_mastodon, self.tag_social_tag,\
                         self.tag_youtube, self.tag_github, self.tag_gitlab, self.tag_insight, self.tag_vimeo, self.tag_g_group, self.tag_g_plus, self.tag_medium, self.tag_goodreads, self.tag_fb_group, self.tag_fb_pages, \
                         self.tag_meetup, self.tag_huodongxing, self.tag_y_video, self.tag_y_channel, self.tag_y_channel2, self.tag_y_playlist, self.tag_award, self.tag_website, self.tag_url, self.tag_memkite, \
                         self.tag_blog, self.tag_linkedin, self.tag_l_group, self.tag_alternativeto, self.tag_clone, self.tag_docker, self.tag_stackexchange, self.tag_zhihu, self.tag_t_zhihu, self.tag_z_zhihu, self.tag_c_zhihu, self.tag_blogspot, self.tag_bitbucket, \
                         self.tag_sourceforge, self.tag_business, self.tag_country, self.tag_price, self.tag_date, self.tag_advisor, self.tag_intern, self.tag_facebook, self.tag_vk, self.tag_reddit, \
                         self.tag_weibo, self.tag_job, self.tag_alliance, self.tag_slideshare, self.tag_crossref, self.tag_contentref, self.tag_vimeopro, self.tag_atlassian, self.tag_qq_group, self.tag_discuss, \
                         self.tag_weixin, self.tag_localdb, self.tag_engintype, self.tag_keyword, self.tag_udacity, self.tag_review, self.tag_instagram, self.tag_leiphone, self.tag_businessinsider, \
                         self.tag_freenode, self.tag_videolectures, self.tag_techtalks, self.tag_universe, self.tag_agent, self.tag_survey, self.tag_series, self.tag_specialization, self.tag_program, self.tag_douyu, \
                         self.tag_digg, self.tag_twitch, self.tag_steam, self.tag_ustream, self.tag_csdnlib, self.tag_cnblog, self.tag_iqiyi, self.tag_flipboard, self.tag_channel9, self.tag_panopto, self.tag_piazza, self.tag_expert, self.tag_blogcsdn, \
                         self.tag_pcpartpicker, self.tag_baijiahao, self.tag_dean, self.tag_jianshu, self.tag_15yan, self.tag_consultant, self.tag_nucleus, self.tag_youku, self.tag_zaker, self.tag_v_qq, self.tag_sohu, \
                         self.tag_nbviewer, self.tag_flagship, self.tag_toutiao, self.tag_leaderboard, self.tag_benchmark, self.tag_baiduyun, self.tag_inke, self.tag_sayit, self.tag_kaggle, self.tag_soundcloud, self.tag_expo, \
                         self.tag_bilibili, self.tag_acfun, self.tag_archive_org, self.tag_zeef, self.tag_g_cores, self.tag_tieba, self.tag_discord, self.tag_mixer, self.tag_periscope, self.tag_flickr, self.tag_vine, self.tag_tudou, self.tag_patreon, self.tag_g_youtube, \
                         self.tag_douban, self.tag_doulist, self.tag_click_count, self.tag_artstation, self.tag_appveyor, self.tag_gamesradar, self.tag_opencollective, self.tag_gamejolt, self.tag_onetab, self.tag_nico, self.tag_wordpress, self.tag_photobucket, self.tag_stumble, self.tag_disqus,\
                         self.tag_waffle, self.tag_pinterest, self.tag_deviantart]

        self.tag_list_short = ["d:"]

        self.tag_list_account = {self.tag_slack :  'https://%s.slack.com/',\
                        self.tag_workast : 'https://%s.workast.io/',\
                        self.tag_gitter :  'https://gitter.im/%s/home',\
                        self.tag_twitter :  'https://twitter.com/%s',\
                        self.tag_mastodon : 'https://mastodon.gamedev.place/%s',\
                        self.tag_github :  'https://www.github.com/%s/',\
                        self.tag_gitlab : 'https://gitlab.com/%s',\
                        self.tag_insight : 'https://insight.io/github.com/%s',\
                        self.tag_youtube :  'https://www.youtube.com/%s/videos',\
                        self.tag_vimeo :  'https://vimeo.com/%s',\
                        self.tag_g_group :  'https://groups.google.com/forum/#!forum/%s',\
                        self.tag_medium :  'https://medium.com/%s',\
                        self.tag_goodreads :  'http://www.goodreads.com/user/show/%s',\
                        self.tag_fb_group :  'https://www.facebook.com/groups/%s/',\
                        self.tag_fb_pages : 'https://www.facebook.com/search/str/%s/keywords_pages',\
                        self.tag_vk : 'https://vk.com/%s',\
                        self.tag_meetup :  'https://www.meetup.com/%s/',\
                        self.tag_huodongxing : 'http://www.huodongxing.com/people/%s',\
                        self.tag_y_video : 'https://www.youtube.com/watch?v=%s',\
                        self.tag_y_channel :  'https://www.youtube.com/channel/%s/videos',\
                        self.tag_y_channel2 : 'https://www.youtube.com/c/%s/videos',\
                        self.tag_y_playlist : 'https://www.youtube.com/playlist?list=%s',\
                        self.tag_memkite :  'http://memkite.com/%s/',\
                        self.tag_linkedin : 'https://www.linkedin.com/%s',\
                        self.tag_l_group :  'https://www.linkedin.com/groups/%s/profile',\
                        self.tag_docker :  'https://hub.docker.com/r/%s/',\
                        self.tag_stackexchange : 'https://%s.stackexchange.com',\
                        self.tag_zhihu :  'https://www.zhihu.com/%s',\
                        self.tag_t_zhihu : 'https://www.zhihu.com/topic/%s',\
                        self.tag_z_zhihu : 'https://zhuanlan.zhihu.com/%s',\
                        self.tag_c_zhihu : 'https://www.zhihu.com/collection/%s',\
                        self.tag_blogspot : 'http://%s.blogspot.com/',\
                        self.tag_bitbucket :  'https://bitbucket.org/%s/',\
                        self.tag_sourceforge : 'https://sourceforge.net/projects/%s',\
                        self.tag_facebook :  'https://www.facebook.com/%s/?fref=nf',\
                        self.tag_reddit :  'https://www.reddit.com/r/%s/',\
                        self.tag_weibo : 'http://weibo.com/%s',\
                        self.tag_slideshare : 'http://www.slideshare.net/%s/presentations',\
                        self.tag_vimeopro : 'https://vimeopro.com/%s',\
                        self.tag_atlassian : 'https://%s.atlassian.net/wiki/discover/all-updates',\
                        self.tag_discuss  : 'http://discuss.%s.com/',\
                        self.tag_udacity : 'https://%s.udacity.com/',\
                        self.tag_instagram : 'https://www.instagram.com/%s/',\
                        self.tag_leiphone : 'http://www.leiphone.com/category/%s',\
                        self.tag_businessinsider : 'http://www.businessinsider.com/%s',\
                        self.tag_freenode : 'https://webchat.freenode.net/?room=%s',\
                        self.tag_videolectures : 'http://videolectures.net/%s/',\
                        self.tag_techtalks : 'http://techtalks.tv/%s/',\
                        self.tag_universe : 'https://www.universe.com/events/%s',\
                        self.tag_douyu : 'https://yuba.douyu.com/%s',\
                        self.tag_digg : 'http://digg.com/channel/%s',\
                        self.tag_twitch : 'https://www.twitch.tv/%s',\
                        self.tag_steam : 'http://steamcommunity.com/%s',\
                        self.tag_ustream : 'https://www.ustream.tv/%s',\
                        self.tag_csdnlib : 'http://lib.csdn.net/base/%s/structure',\
                        self.tag_blogcsdn : 'http://blog.csdn.net/%s',\
                        self.tag_cnblog : 'http://www.cnblogs.com/%s',\
                        self.tag_iqiyi : 'http://www.iqiyi.com/u/%s/v',\
                        self.tag_flipboard : 'https://flipboard.com/%s',\
                        self.tag_channel9 : 'https://channel9.msdn.com/Events/%s/',\
                        self.tag_panopto : 'https://%s.panopto.com/Panopto/Pages/Sessions/List.aspx',\
                        self.tag_piazza : 'https://piazza.com/%s',\
                        self.tag_pcpartpicker : 'http://pcpartpicker.com/%s',\
                        self.tag_baijiahao : 'https://baijiahao.baidu.com/feed/source/%s',\
                        self.tag_jianshu : 'http://www.jianshu.com/u/%s',\
                        self.tag_15yan : 'http://www.15yan.com/i/%s/',\
                        self.tag_nucleus : 'https://meetnucleus.com/%s',\
                        self.tag_youku : 'http://i.youku.com/i/%s==/videos',\
                        self.tag_zaker : 'http://www.myzaker.com/source/%s',\
                        self.tag_v_qq : 'http://v.qq.com/vplus/%s/videos',\
                        self.tag_sohu : 'http://mp.sohu.com/profile?xpt=%s',\
                        self.tag_nbviewer : 'http://nbviewer.jupyter.org/%s',\
                        self.tag_toutiao  : 'http://www.toutiao.com/%s/',\
                        self.tag_baiduyun : 'https://pan.baidu.com/share/home?uk=%s',\
                        #self.tag_baiduyun : 'https://www.sopanpan.com/user/%s-0.html',\
                        self.tag_sayit : 'https://sayit.%s',\
                        self.tag_kaggle : 'https://www.kaggle.com/%s',\
                        self.tag_soundcloud : 'https://soundcloud.com/%s',\
                        self.tag_bilibili : 'https://space.bilibili.com/%s/#/video',\
                        self.tag_acfun : 'http://www.acfun.cn/u/%s.aspx',\
                        self.tag_archive_org : 'https://archive.org/details/%s',\
                        self.tag_zeef : 'https://%s.zeef.com/%s',\
                        self.tag_g_cores : 'http://www.g-cores.com/users/%s',\
                        self.tag_tieba : 'https://tieba.baidu.com/f?kw=%s',\
                        self.tag_discord : 'https://discordapp.com/channels/%s/',
                        self.tag_mixer : 'https://mixer.com/%s',\
                        self.tag_periscope : 'https://www.periscope.tv/%s',\
                        self.tag_flickr : 'https://www.flickr.com/photos/%s/',\
                        self.tag_vine : 'https://vine.co/%s?mode=grid',\
                        self.tag_tudou : 'http://id.tudou.com/i/%s/videos',\
                        self.tag_patreon : 'https://www.patreon.com/%s',
                        self.tag_g_youtube : 'https://gaming.youtube.com/user/%s',\
                        self.tag_g_plus : 'https://plus.google.com/%s',\
                        self.tag_douban : 'https://www.douban.com/people/%s/',\
                        self.tag_doulist : 'https://www.douban.com/doulist/%s',\
                        self.tag_artstation : 'https://www.artstation.com/%s',\
                        self.tag_appveyor : 'https://ci.appveyor.com/project/%s/build/artifacts',\
                        self.tag_gamesradar : 'http://www.gamesradar.com/author/%s/',\
                        self.tag_opencollective : 'https://opencollective.com/%s',\
                        self.tag_gamejolt : 'https://gamejolt.com/%s',\
                        self.tag_onetab : 'https://www.one-tab.com/page/%s',\
                        self.tag_nico : 'http://www.nicovideo.jp/user/%s/video',\
                        self.tag_wordpress : 'https://%s.wordpress.com/',\
                        self.tag_photobucket : 'http://s446.photobucket.com/user/%s/library/',\
                        self.tag_stumble : 'http://www.stumbleupon.com/%s',\
                        self.tag_disqus : 'https://disqus.com/home/forum/%s',\
                        self.tag_waffle : 'https://waffle.io/%s',\
                        self.tag_pinterest : 'https://www.pinterest.com/%s',\
                        self.tag_deviantart : 'https://%s.deviantart.com/'}

        #account_mode only for people or organization
        self.tag_list_account_mode = [self.tag_instructors, self.tag_author, self.tag_organization, self.tag_university, self.tag_winner, self.tag_professor, self.tag_conference, self.tag_cto, self.tag_cio, self.tag_cfo, self.tag_cmo, self.tag_cco, self.tag_cbo, self.tag_coo, self.tag_cpo, self.tag_company, self.tag_engineer, self.tag_institute, self.tag_director, self.tag_ceo, self.tag_vp, self.tag_startup, self.tag_investor, self.tag_scientist, self.tag_faculty, self.tag_investigator, self.tag_researcher, self.tag_people, self.tag_investor, self.tag_follow, self.tag_lab, self.tag_developer, self.tag_designer, self.tag_artist, self.tag_writer, self.tag_programmer, self.tag_title, self.tag_advisor, self.tag_intern, self.tag_zhihu, self.tag_leader]
        
        self.tag_list_direct_link = [self.tag_website]

        self.tag_list_smart_link = [self.tag_path, self.tag_id, self.tag_project, self.tag_paper, self.tag_instructors, self.tag_author, self.tag_organization, self.tag_university, self.tag_winner, self.tag_alias, self.tag_professor, self.tag_conference, self.tag_cto, self.tag_cso, self.tag_cio, self.tag_cfo, self.tag_cmo, self.tag_cco, self.tag_cbo, self.tag_coo, self.tag_cpo, self.tag_company, self.tag_engineer, self.tag_institute, self.tag_director, self.tag_ceo, self.tag_vp, self.tag_startup, self.tag_investor, self.tag_scientist, self.tag_faculty, self.tag_investigator, self.tag_researcher, self.tag_phd, self.tag_people, self.tag_award, self.tag_website, self.tag_investor, self.tag_follow, self.tag_lab, self.tag_developer, self.tag_product, self.tag_designer, self.tag_artist, self.tag_writer, self.tag_programmer, self.tag_blog, self.tag_alternativeto, self.tag_clone, self.tag_title, self.tag_advisor, self.tag_intern, self.tag_facebook, self.tag_challenge, self.tag_job, self.tag_leader, self.tag_alliance, self.tag_crossref, self.tag_founder, self.tag_dataset, self.tag_weixin, self.tag_localdb, self.tag_engintype, self.tag_keyword, self.tag_review, self.tag_agent, self.tag_survey, self.tag_series, self.tag_specialization, self.tag_program, self.tag_bible, self.tag_expert, self.tag_dean, self.tag_consultant, self.tag_flagship, self.tag_textbook, self.tag_expo, self.tag_social_tag]

    tagListCache = {}
    def get_tag_list(self, library):
        #print 'get_tag_list:' + library

        if self.tagListCache.has_key(library):
            return self.tagListCache[library]

        result = self.tag_list
        if self.tag_map.has_key(library):
            result =  self.tag_list + self.tag_map[library] #+ self.tag_list_account.keys()

        self.tagListCache[library] = result
        return result

    smartLinkCache = {}
    def get_list_smart_link(self, library):
        #print 'get_list_smart_link:' + library

        if self.smartLinkCache.has_key(library):
            return self.smartLinkCache[library]

        result = self.tag_list_smart_link
        if self.tag_map.has_key(library):
            result = self.tag_list_smart_link + self.tag_map[library]
        self.smartLinkCache[library] = result
        return result



class WrapRecord(Record):

    def __init__(self, line):
        Record.__init__(self, line)
        self.describe = self.to_unicode(self.get_describe())
        self.tag = Tag()

    def next_tag_pos(self, pos, max_pos, library=''):
        min_pos = len(self.describe) + 1
        for t in self.tag.get_tag_list(library):
            next_pos = self.describe.lower().find(t, pos + 1)
            if next_pos != -1 :
                if max_pos:
                    return next_pos
                elif next_pos < min_pos and next_pos > pos:
                    min_pos = next_pos

        if min_pos != len(self.describe) + 1:
            return min_pos
        else:
            return -1

    def get_tag_content(self, tag, max_pos=False, library=''):
        tag = ' ' + tag.strip()
        if tag.endswith(':') == False:
            tag = tag + ':'
            
        start_pos = self.describe.lower().find(tag)
        #print self.describe.lower()
        #print start_pos
        #print self.describe.lower()[start_pos :]
        if start_pos != -1:
            end_pos = self.next_tag_pos(start_pos + len(tag), max_pos, library=library)
            if end_pos != -1:
                #print start_pos 
                #print end_pos
                #print self.describe.lower()[start_pos :end_pos]
                return self.describe[start_pos + len(tag) : end_pos].strip()
            else:
                return self.describe[start_pos + len(tag) : ]

        return None

    def to_unicode(self, value):
        if not isinstance(value, basestring):
            value = str(value)
        if not isinstance(value, unicode):
            value = unicode(value, "UTF-8", "strict")
        return value

class LibraryRecord(WrapRecord):
    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_path(self):
        return self.get_tag_content(self.tag.tag_path)

class CategoryRecord(WrapRecord):
    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_category(self):
        return self.get_tag_content(self.tag.tag_category)

class PaperRecord(WrapRecord):
    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_author(self):
        return self.get_tag_content(self.tag.tag_author)

    def get_category(self):
        return self.get_tag_content(self.tag.tag_category)

    def get_summary(self):
        return self.get_tag_content(self.tag.tag_summary)

    def get_published(self):
        return self.get_tag_content(self.tag.tag_published)

    def get_version(self):
        return self.get_tag_content(self.tag.tag_version)



class PriorityRecord(WrapRecord):

    def __init__(self, line):
        WrapRecord.__init__(self, line)

    def get_priority(self):
        return self.get_tag_content(self.tag.tag_priority)


    def get_description(self):
        return self.get_tag_content(self.tag.tag_description)

    def get_icon(self):
        return self.get_tag_content(self.tag.tag_icon)

class EnginRecord(PriorityRecord):
    def __init__(self, line):
        PriorityRecord.__init__(self, line)

    def get_description(self):
        return self.get_tag_content(self.tag.tag_description)

    def get_shortname(self):
        return self.get_tag_content(self.tag.tag_shortname)


class ReferenceRecord(PriorityRecord):
    def __init__(self, line):
        PriorityRecord.__init__(self, line)

class ContentRecord(PriorityRecord):
    def __init__(self, line):
        PriorityRecord.__init__(self, line)

    def get_parentid(self):
        return self.get_tag_content(self.tag.tag_parentid)


class CourseRecord(PriorityRecord):

    def __init__(self, line):
        PriorityRecord.__init__(self, line)

    def get_videourl(self):
        return self.get_tag_content(self.tag.tag_videourl)

    def get_author(self):
        return self.get_tag_content(self.tag.tag_author)

    def get_ratings(self):
        return self.get_tag_content(self.tag.tag_ratings)

    def get_term(self):
        return self.get_tag_content(self.tag.tag_term)

    def get_prereq(self):
        return self.get_tag_content(self.tag.tag_prereq)

    def get_toprepo(self):
        return self.get_tag_content(self.tag.tag_toprepo)

    def get_project(self):
        return self.get_tag_content(self.tag.tag_project)

    def get_university(self):
        return self.get_tag_content(self.tag.tag_university)

    def get_available(self):
        return self.get_tag_content(self.tag.tag_available)

    def get_level(self):
        return self.get_tag_content(self.tag.tag_level)

    def get_features(self):
        return self.get_tag_content(self.tag.tag_features)

    def get_instructors(self):
        return self.get_tag_content(self.tag.tag_instructors)

    def get_description(self):
        return self.get_tag_content(self.tag.tag_description)

    def get_textbook(self):
        content = self.get_tag_content(self.tag.tag_textbook, True)
        if content != None:
            return content.replace(self.tag.tag_textbook, '')
        return content

    def get_paper(self):
        return self.get_tag_content(self.tag.tag_paper)

    def get_homepage(self):
        return self.get_tag_content(self.tag.tag_homepage)

    def get_organization(self):
        return self.get_tag_content(self.tag.tag_organization)

    def get_platform(self):
        return self.get_tag_content(self.tag.tag_platform)

    def get_specialization(self):
        return self.get_tag_content(self.tag.tag_specialization)
   
    def get_journal(self):
        return self.get_tag_content(self.tag.tag_journal)



'''
r = CourseRecord('id | title | url | prereq:prereqxxx project:projectxxx university:universityxxx available:availablexxx level:levelxxx features:featuresxxx instructors:instructorsxxx textbook:textbook111 textbook:textbook222 description:descriptionxxx')

print r.get_prereq()
print r.get_project()
print r.get_university()
print r.get_available()
print r.get_level()
print r.get_features()
print r.get_instructors()
print r.get_description()
print r.get_textbook()
'''

#r = Record("id | title | url | describe")

#print r.get_id()
#print r.get_title()
#print r.get_describe()
#print r.get_url()
