#!/usr/bin/env python
# -*- coding: utf-8-*- 

class Config():
    
    #default_db = 'db'
    default_subject = 'eecs'

    default_db = 'db' #'2016-db'

    user_name = 'wowdd1'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    proxies = {
        "http": "http://127.0.0.1:8087",
        "https": "http://127.0.0.1:8087",
    }

    proxies2 = {
        "http": "http://127.0.0.1:8787",
        "https": "http://127.0.0.1:8787",
    }


    proxies3 = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
    }
    
    igon_authorized = True

    engin_list_file = 'db/metadata/engin_list'
    engin_type_file = 'db/metadata/engin_type'
    engin_extension_file = 'db/metadata/engin_extension'

    smart_link_style = 'font-family:San Francisco;'
    # enable urlFromServer  enhancedLink(..., urlFromServer=True)
    # engin query order smart_link_engin -> smart_engin_for_tag -> smart_engin_for_extension
    smart_link_engin = 'glucky' #'google'
    default_engin_searchbox = 'zhihu'

    igon_log_for_modules = ['star', 'exclusive', 'content'] #dialog
    more_button_for_history_module = True

    smart_engin_lucky_mode_for_account = True
    smart_engin_for_tag_batch_open = False
    smart_engin_for_command_batch_open = ['twitter', 'baidu', 'amazon']
    max_account_for_tag_batch_open = 10
    open_all_link_in_one_page = True
    open_all_link_in_frameset_mode = False
    max_last_open_urls = 7
    
    recommend_engin = True
    recommend_engin_num = 23
    recommend_engin_num_dialog = 10
    recommend_engin_num_dialog_row = 5
    recommend_engin_type = 'star' #ref db/metadata/engin_type
    recommend_engin_by_tag = False

    #smart_engin_for_tag = {}

    smart_engin_for_tag = {'weixin' : ['weixin.so', 'weixinla', 'chuansong', 'toutiao', 'weibo', 'qoofan.com', 'glucky'],\
                           'fb-pages' : ['fb-pages', 'glucky'],\
                           'baijiahao' : ['baijiahao'],\
                           'conference' : ['glucky', 'google', 'd:event'],\
                           'social-tag' : 'd:socialtag'}
    '''

    smart_engin_for_tag = {'instructors' : ['twitter', 'youtube'],\
                           'university' : 'youtube',\
                           'professor' : ['phdtree', 'glucky'],\
                           'g-plus' : 'plus.google',\
                           'company' : 'glucky',\
                           'website' : 'glucky',\
                           'director' : ['twitter', 'glucky'],\
                           'job' : ['google', 'd:job']}
                           #'topic' : ''}
    '''
    
    #smart_engin_for_extension = {'' : ''}

    #smart_engin_for_dialog = ['google', 'youtube', 'twitter', 'baidu']
    smart_engin_for_dialog = []
    command_for_dialog = ['add2library', 'add2qa', 'trace', 'kgraph', 'exclusive']
    command_for_tag_dialog = ['tolist', 'merger']

    recommend_engin_type_for_dialog = '' #'star' #ref db/metadata/engin_type

    smart_link_max_text_len = 60
    smart_link_br_len = 60
    replace_with_smart_link = False

    page_item_count = 100#63

    start_library_title = 'add some record from here!'
    start_library_url = 'http://' + ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3'

    menu_library_list = ['ai-library', 'multimedia-library', 'mind-library', 'neuro-library', 'gene-library', 'math-library', 'phys-library', 'chem-library', 'business-finance-library', 'engineering-library', 'product-library', 'manage-library', 'art-library']
    #default_library = ''
    default_library = 'ai-library'
    #default_library = 'engineering-library'
    #default_library = 'multimedia-library'
    #default_library = 'mind-library'
    #default_library = 'neuro-library'
    #default_library = 'gene-library'
    #default_library = 'math-library'
    #default_library = 'phys-library'
    #default_library = 'chem-library'
    #default_library = 'business-finance-library'
    #default_library = 'medical-library'
    #default_library = 'energy-library'
    #default_library = 'aerospace-library'
    #default_library = 'universe-library'
    #default_library = 'earth-library'
    #default_library = 'social-library'
    #default_library = 'art-library'
    #default_library = 'literature-library'
    #default_library = 'manage-library'
    #default_library = 'thought-library'
    #default_library = 'media-library'
    #default_library = 'telecom-library'
    #default_library = 'manufacture-library'
    #default_library = 'traffic-library'
    #default_library = 'retail-library'
    #default_library = 'building-library'
    #default_library = 'life-library'
    #default_library = 'sport-library'
    #default_library = 'entertainment-library'
    #default_library = 'military-library'
    #default_library = 'product-library'
    #default_library = 'research-library'


    #show random preview when click nav link

    track_mode = False

    disable_default_engin = True

    disable_nav_engins = True # it take 2s for gen nav engins html
  
    disable_thumb = "false"

    disable_icon = True

    disable_star_engin = False

    disable_reference_image = False 
   
    hiden_record_id = True
    hiden_record_id_commandline = False
    hiden_parentid_record = True

    hiden_engins = True
    
    center_content = False
    
    content_margin_left = '15px'
    content_margin_top = '10px'

    split_height = 2
    title_font_size = 0

    #do not show nav links, only show extension links
    extension_mode = False

    #handle by handleQueryNavTab of app.py first
    default_tab = 'history' #'content'
    second_default_tab = 'bookmark'#'figures'

    default_width = "54" #"79"
    column_num = "3"
    custom_cell_len = 88 
    split_length = custom_cell_len + 15
    custom_cell_row_list = [50, 40, 30]
    cell_len = 89  #  cell_len >= course_num_len + 1 + course_name_len + 3
    course_name_len = 70
    course_num_len = 10
    color_index = 0
    output_with_color = False
    output_with_style = False
    output_with_describe = False
    output_navigation_links = False
    merger_result = False
    top_row = 0
    old_top_row = 0
    max_links_row = 10
    max_nav_link_row = 11
    max_nav_links_row = 7
    default_links_row = 2    

    css_style_type = 0
    plugins_mode = False

    auto_library_cell_len = False

    display_all_library = True

    hiden_content_after_search = True
    background_after_click = '#E9967A' ##CCEEFF
    fontsize_after_click = ''

    fav_links = { #'arxiv' : ip_adress + '/?db=eecs/papers/arxiv/&key=?',\
		  'civilization' : ip_adress + '/?db=other/&key=civilization2018&column=2',\
          #'bioRxiv' : 'cshsymposium.com/biorxiv/chartdailydetail.php',\
          'db' : ip_adress + '/?db=?',\
          #'rss' : ip_adress + '/?db=rss/&key=rss2016',\
          #'disk' : ip_adress + '/?db=other/&key=disk2016',\
          #'github' : ip_adress + '/?db=eecs/projects/github/&key=?',\
          #'ipynb' : 'localhost:8888/tree',\
          #'degree' : ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3',\
          #'members' : ip_adress + '/?db=rank/&key=members2016&column=2',\
          'rank' : ip_adress + '/?db=rank/&key=?',\
          #'paperbot' : 'https://web.paperbot.ai/',\
          #'iris.ai' : 'https://the.iris.ai/explore',\
          'roadmap' : ip_adress + '/?db=other/&key=roadmap',\
          'frontier' : ip_adress + '/?db=other/&key=frontier2018'}
		  #'eecs' :  ip_adress + '/?db=eecs/&key=?'}
          #'library' : ip_adress + '/?db=library/&key=?'}
		  #'neuroscience' : ip_adress + '/?db=neuroscience/&key=?'}


    distribution = False
    slack_token = ['xoxb', '156129958533', 'YdIXSA2syy7ipacDQo6cr03j']

    delete_from_char = ''
    delete_forward = True


    application_dict = {'.ppt' : '/Applications/Preview.app/Contents/MacOS/Preview',\
                        '.pptx' : '/Applications/Preview.app/Contents/MacOS/Preview',\
                        '.epub' : '/Applications/iBooks.app/Contents/MacOS/iBooks',\
                        '*' : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}

    # ==== extension ====
    one_page_path_root = "file:///Users/" + user_name + "/dev/xlb_env/xlinkBook/"
    output_data_to_new_tab_path = 'db/other/'
    # reference
    reference_filter = ''
    reference_contain = ''
    reference_igon_case = True
    reference_hiden_engin_section = True
    reference_output_data_to_new_tab = False
    reference_output_data_format = ''

    # bookmark
    bookmark_file_path = "/Users/" + user_name + "/Downloads/chrome_bookmarks.json"
    bookmark_hiden_engin_section = True
    bookmark_output_data_to_new_tab = False
    bookmark_output_data_format = ''
    bookmark_page_item_count = [16, 14, 12]

    #history
    history_file_path = "/Users/" + user_name + "/Downloads/chrome_history.json"
    history_hiden_engin_section = True
    hidtory_sort_type = 0 #0: click count 1: url 2: title
    history_show_click_count = False
    history_enable_subitem_log = False
    history_enable_quick_access = True
    history_quick_access_item_count = 5
    history_quick_access_name = 'Quick Access'

    #exclusive
    exclusive_crossref_path = ['db/library']
    exclusive_local_db_path = 'db/' + default_subject
    exclusive_default_tab = {'twitter' : 'convert'}


    #filefinder
    filefinder_dirs = ['~/Downloads', 'db']
    filefinder_netdisk_engin = ['pan.baidu', 'onedrive'] #drive  onedrive dropbox
    filefinder_sort_by_count = True

    #content
    content_hiden_engin_section = True

    # convert
    ''' default config
    convert_url_args = '' #'?start=' #'?start=0&tag='
    convert_page_step = 0
    convert_page_start = 0
    convert_page_max = 600
    convert_page_to_end = True
    convert_page_custom_parse = False
    convert_tag = 'tr' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 0
    convert_split_column_number = 0
    convert_hiden_engin_section = True
    convert_output_data_to_new_tab = False
    convert_output_data_format = ''
    '''
    #'''
    convert_url_args = '' #'?start=' #'?start=0&tag='
    convert_page_step = 1
    convert_page_start = 1
    convert_page_max = 4
    convert_page_to_end = False
    convert_tag = '' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 0
    convert_split_column_number = 0
    convert_output_data_to_new_tab = False
    convert_output_data_format = ''
    convert_cut_start = ''
    convert_cut_start_offset = 0
    convert_cut_end = ''
    convert_cut_end_offset = 0
    convert_remove = []
    convert_cut_max_len = 1000
    convert_script = ''
    convert_script_custom_ui = False
    convert_smart_engine = ''
    convert_sort = False

    # url keyword + args
    # resource type + args
    convert_dict = {'reddit' : {'url_args' : '', 'page_step' : convert_page_step, 'page_start' : convert_page_start,\
                                 'page_max' : convert_page_max, 'page_to_end' : convert_page_to_end, 'tag' : 'a#title',\
                                 'min_num' : convert_min_num, 'max_num' : convert_max_num, 'filter' : convert_filter,\
                                 'contain' : convert_contain, 'start' : convert_start, 'split_column_number' : convert_split_column_number,\
                                 'output_data_to_new_tab' : convert_output_data_to_new_tab, 'output_data_format' : convert_output_data_format},\
                    'quora' : {'script' : 'convert_quora.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'www.zhihu' : {'script' : 'convert_zhihu.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'zhuanlan' : {'url_args' : '?limit=100&offset=', 'tag' : 'span#PostListItem-title', 'page_start' : 0, 'page_step' : 0},\
                    'collection' : {'url_args' : '?page=', 'tag' : 'h2#zm-item-title', 'page_start' : 1, 'page_step' : 1, 'page_max' : 21},\
                    'csdn' : {'url_args' : '/article/list/', 'tag' : 'h3#blog-title'},\
                    'gdcvault' : {'url_args' : '', 'tag' : 'div#conference_info', 'cut_start' : '20', 'cut_start_offset' : 2, 'cut_end' : 'by', 'remove' : ['(Presented', '(Prese'] , 'split_column_number' : 40, 'cut_max_len' : 73},\
                    'nips' : {'tag' : 'li', 'min_num' : 15, 'split_column_number' : 100, 'cut_end' : ',', 'cut_max_len' : 80},\
                    'twitter' : {'script' : 'convert_twitter.py', 'script_custom_ui' : False, 'split_column_number' : 12},\
                    'igdb' : {'script' : 'convert_igdb.py', 'script_custom_ui' : True, 'split_column_number' : 12},\
                    'gamefromscratch' : {'url_args' : '?page=', 'tag' : 'a#posttitlelink', 'page_start' : 1, 'page_step' : 1, 'page_max' : 10},\
                    'uwa4d' : {'url_args' : 'page/', 'tag' : 'h2#post-title', 'page_start' : 1, 'page_step' : 1, 'page_max' : 30, 'page_to_end' : True, 'contain' : '虚幻', 'split_column_number' : 40 },\
                    'deepmind' : {'url_args' : '?page=', 'tag' : 'a#faux-link-block--link', 'page_start' : 1, 'page_step' : 1, 'page_max' : 10},\
                    'blog' : {'script' : 'convert_blog.py', 'script_custom_ui' : True},\
                    'gputechconf' : {'tag' : 'span#anchortitle', 'split_column_number' : 40, 'smart_engine' : 'gtc', 'cut_max_len' : 73},\
                    'github' : {'script' : 'convert_github.py', 'script_custom_ui' : False, 'split_column_number' : 12}}
    #'''

    #=====bk====
    background = 0
    backgrounds = ['',\
                    'http://img.blog.csdn.net/20161213000422101',\
                    'https://datacdn.soyo.or.kr/wcont/uploads/2016/02/02164057/alphago_01.jpg',\
                    'http://img.blog.csdn.net/20150506120021512?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd293ZGQx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center',\
                    'http://img.blog.csdn.net/20161227171638323',\
                    'http://images.njcw.com/upload/2011-5/201105071635561829723_w.jpg',\
                    'http://www.caneis.com.tw/link/info/Middle_East_info/Egypt/images/Cairo-007-1.jpg',\
                    'https://cdn-images-1.medium.com/max/2000/1*BTGKRLq55y8Hld9pyvarXg.png',\
                    'http://st.depositphotos.com/1007919/3724/i/950/depositphotos_37248955-stock-photo-binary-background.jpg',\
                    'http://amazingstuff.co.uk/wp-content/uploads/2012/02/scale_of_the_universe_2.png',\
                    'https://curiositando.files.wordpress.com/2014/12/cervello_destro1.jpg',\
                    'http://img1.voc.com.cn/UpLoadFile/2013/03/05/201303051655526838.jpg',\
                    'http://p1.pstatp.com/large/530000529b6125ce87c',\
                    'http://zdnet4.cbsistatic.com/hub/i/r/2016/06/01/8a90fae5-22f7-480b-9ea5-a4f6252e7ed0/resize/1170x878/d756410179b9c71086b1496f4b924556/001.jpg',\
                    'http://tc.sinaimg.cn/maxwidth.2048/tc.service.weibo.com/s9_rr_itc_cn/000254925dab8674da3fb790364ddcf0.png']

    #=====icon====
    enable_website_icon = True
    website_icons = {'.pdf' : 'https://cdn4.iconfinder.com/data/icons/CS5/128/ACP_PDF%202_file_document.png',\
                 '.dir' : 'http://cdn.osxdaily.com/wp-content/uploads/2014/05/users-folder-mac-osx.jpg',\
                 'delete' : 'https://cdn2.iconfinder.com/data/icons/duo-toolbar-signs/512/erase-512.png',\
                 'homepage' : 'http://grupojvr.com.mx/web/wp-content/uploads/2014/08/Direcci%C3%B3n-azul.png',\
                 'url' : 'http://vintaytime.com/wp-content/uploads/2017/02/url-shortener-icon.png',\
                 'website' : 'https://image.flaticon.com/icons/png/128/12/12195.png',\
                 'sync' : 'https://d1ueyc5nx1it61.cloudfront.net/4ca92ab816119221027.png',\
                 'quickaccess' : 'https://winaero.com/blog/wp-content/uploads/2016/12/Quick-Access-Icon-256.png',\
                 'clickcount' : 'http://www.freepngimg.com/download/mouse_cursor_click/1-2-click-free-download-png.png',\
                 'idea' : 'https://d30y9cdsu7xlg0.cloudfront.net/png/62335-200.png',\
                 'remark' : 'http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png',\
                 'youtube' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'y-video' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'y-channel' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'y-channel2' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'y-playlist' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'amazon' : 'https://media.licdn.com/mpr/mpr/shrink_200_200/AAEAAQAAAAAAAAUqAAAAJGFmYjUxMmQ3LWUyNDUtNGJmMy04Nzc4LWRmYzE1YTExMDY2YQ.png',\
                 'csdn' : 'http://a2.mzstatic.com/us/r30/Purple71/v4/99/61/36/996136cc-f759-5c0c-4531-ee0c6fec786a/icon175x175.png',\
                 'coursera': 'http://techraze.com/wp-content/uploads/2015/06/Coursera-APK-1.png',\
                 'edx' : 'https://icon.apkmirrordownload.com/org.edx.mobile.png',\
                 'udacity' : 'https://www.uplabs.com/assets/integrations/udacity-92b3b2525603489c7c5f325491d0ff44652631210086bb2ab082b897b9b39da0.png',\
                 'github' : 'https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png',\
                 'insight' : 'https://insight.io/assets/images/logo/lambda-color.svg',\
                 'arxiv' : 'http://www.thetelegraphic.com/img/icon-arxiv.png',\
                 'khan' : 'http://academics.cehd.umn.edu/mobile/wp-content/uploads/2013/10/khan-academy-icon.png',\
                 'medium' : 'https://memoriaelectrika.files.wordpress.com/2015/10/mediumlogo002.png',\
                 'mit': 'https://1.bp.blogspot.com/-fhwcWQmSJk4/VsMJ_NzuasI/AAAAAAAAAAo/qoBFDEJLnwI/w800-h800/images.png',\
                 'stanford' : 'https://d9tyu2epg3boq.cloudfront.net/institutions/stanford.png',
                 'berkeley' : 'http://www.berkeley.edu/brand/img/seals/ucbseal_139_540.png',\
                 'cmu' : 'http://www.wholeren.com/wp-content/uploads/2015/04/Carnegie_Mellon_University_CMU_1015361.png',\
                 'harvard' : 'http://tusm.3daystartup.org/files/2013/03/harvard.png',\
                 'oxford' : 'http://cdn.shopify.com/s/files/1/0581/9089/products/neck_label_option_1.png?v=1456393100',\
                 'cambridge' : 'http://a5.mzstatic.com/us/r30/Purple1/v4/6a/cf/d8/6acfd890-9467-f907-5092-5198e091fe04/icon256.png',\
                 'wikipedia' : 'http://vignette3.wikia.nocookie.net/everythingmarioandluigi/images/e/e8/Wikipedia_icon.png/revision/latest?cb=20130709180530',\
                 'stackoverflow' : 'http://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a',\
                 'quora' : 'https://cdn4.iconfinder.com/data/icons/miu-flat-social/60/quora-128.png',\
                 'reddit' : 'http://icons.iconarchive.com/icons/uiconstock/socialmedia/128/Reddit-icon.png',\
                 'zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'z-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 't-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'c-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'videolectures' : 'http://ftp.acc.umu.se/mirror/addons.superrepo.org/v7/addons/plugin.video.videolectures.net/icon.png',\
                 'weixin' : 'http://img4.imgtn.bdimg.com/it/u=972460576,3713596294&fm=21&gp=0.jpg',\
                 'weibo' : 'http://img4.imgtn.bdimg.com/it/u=173132403,536146045&fm=21&gp=0.jpg',\
                 'twitter' : 'http://itouchappreviewers.com/wp-content/uploads/2015/01/twitter-logo_22.png',\
                 'slack' : 'https://cdn0.iconfinder.com/data/icons/tuts/256/slack_alt.png',\
                 'facebook' : 'http://img.25pp.com/uploadfile/app/icon/20160505/1462390862727305.jpg',\
                 'fb-group' : 'http://img.25pp.com/uploadfile/app/icon/20160505/1462390862727305.jpg',\
                 'g-plus' : 'http://upsidebusiness.com/blog/wp-content/uploads/2015/05/google-plus.jpg',\
                 'instagram' : 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/240px-Instagram_icon.png',\
                 'localhost' : 'https://publicportal.teamsupport.com/Images/file.png',\
                 'iqiyi' : 'https://images-na.ssl-images-amazon.com/images/I/71ABWNB-YML._SL500_AA300_.png',\
                 'linkedin' : 'https://blogs.cornell.edu/info2040/files/2016/09/LinkedinII-2f706bu.png',\
                 'v.qq' : 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=311155846,3382957541&fm=23&gp=0.jpg',\
                 'douyu' : 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=791058301,37936658&fm=23&gp=0.jpg',\
                 'pan.baidu' : 'http://img0.imgtn.bdimg.com/it/u=3595078885,1850864109&fm=23&gp=0.jpg',\
                 'cnblog' : 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2371619540,33511528&fm=27&gp=0.jpg',\
                 'youku' : 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1278976984,3400181597&fm=26&gp=0.jpg',\
                 'zeef' : 'https://zeef.io/image/24118/300/s?1432128680548',\
                 'discord' : 'http://www.nirthpanter.net/uploads/4/7/2/8/47284995/discord_3_orig.png',\
                 'twitch' : 'https://pbs.twimg.com/profile_images/979112299188445184/CiC_MYdI_400x400.jpg',\
                 'bilibili' : 'http://images.firstpost.com/wp-content/uploads/2017/09/BiliBili-380px.png',\
                 'slideshare' : 'http://expandedramblingscom-oxyllvbag8y7yalm1.stackpathdns.com/wp-content/uploads/2013/07/slideshare.jpg',\
                 'google' : 'https://www.nbr.co.nz/sites/default/files/styles/article_full_300w/public/blog_post_img/Google-Logo.jpg',\
                 'flickr' : 'http://clave7.webcindario.com/logo_flickr_01.png',\
                 'pinterest' : 'https://cdn0.iconfinder.com/data/icons/Pinterest/256/Pinterest_Favicon.png',\
                 'jianshu' : 'http://cdn2.jianshu.io/assets/web/logo-58fd04f6f0de908401aa561cda6a0688.png',\
                 'archive.org' : 'http://richmondsfblog.com/wp-content/uploads/2016/11/internet-archive-squarelogo.png',\
                 'tieba' : 'https://cdn4.iconfinder.com/data/icons/chinas-social-share-icons/256/cssi_tieba-512.png',\
                 'appveyor' : 'https://www.appveyor.com/assets/img/appveyor-logo-256.png',\
                 'baiduyun' : 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1517551378&di=77dfd3111d5e7b16ea262c3ce893656e&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0114ed5945efb4a8012193a3dced37.png',\
                 'mixer' : 'https://mixer.com/_latest/assets/images/main/logos/merge-on-black.png',\
                 'douban' : 'https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg',\
                 'doulist' : 'https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg',\
                 'patreon' : 'http://www.comixlaunch.com/wp-content/uploads/2016/08/patreon-logo-05.jpg',\
                 'steam' : 'http://media.moddb.com/images/members/1/927/926352/profile/steam.png',\
                 'vine' : 'http://media.idownloadblog.com/wp-content/uploads/2014/03/Vine-1.4.8-for-iOS-app-icon-small-e1404946147708.png',\
                 'nico' : 'https://ddnavi.com/wp-content/uploads/2013/02/img_540644_19961289_0.png',\
                 'workast' : 'https://cdn.workast.io/prod/images/logo-nobg.7dfc9186.svg',\
                 'disqus' : 'https://i2.wp.com/www.betterhostreview.com/wp-content/uploads/disqus.jpg'}