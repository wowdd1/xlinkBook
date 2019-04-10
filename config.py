#!/usr/bin/env python
# -*- coding: utf-8-*- 

class Config():
    
    #default_db = 'db'
    default_subject = 'eecs'

    default_db = 'db' #'2016-db'

    user_name = 'wowdd1'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    #SSR
    proxies1 = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087",
    }

    proxies2 = {
        "http": "http://127.0.0.1:8787",
        "https": "http://127.0.0.1:8787",
    }


    proxies3 = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
    }

    proxies4 = {
        "http": "http://127.0.0.1:8087",
        "https": "http://127.0.0.1:8087",
    }
    
    proxies = proxies4

    
    igon_authorized = True

    engin_list_file = 'db/metadata/engin_list'
    engin_type_file = 'db/metadata/engin_type'
    engin_extension_file = 'db/metadata/engin_extension'

    smart_link_style = 'font-family:San Francisco;'
    # enable urlFromServer  enhancedLink(..., urlFromServer=True)
    # engin query order smart_link_engin -> smart_engin_for_tag -> smart_engin_for_extension
    smart_link_engin = 'glucky' #'google'
    default_engin_searchbox = 'zhihu'

    igon_log_for_modules = ['star', 'exclusive', 'content', 'bookmark'] #dialog
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
    recommend_engin_dict = {} #{'multimedia-library' : 'google baidu'}
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
    default_library_filter = ''
    #default_library_filter = 'Video Game#orGame Engine#orRendering Engine'
    #default_library = ''
    default_library = 'multimedia-library'#'ai-library'
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

    search_mode = True

    searchinLoopSearch = False

    autoAppendDescFilterCategory = False

    tagAliasDict = {'desc:' : 'description:',\
                    'tag:' : 'alias:'}

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
                        #'.epub' : '/Applications/iBooks.app/Contents/MacOS/iBooks',\
                        '.epub' : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',\
                        '.key' : '/Applications/Keynote.app/Contents/MacOS/Keynote',\
                        '*' : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}

    # ==== extension ====
    one_page_path_root = "file:///Users/" + user_name + "/dev/xlb_env/xlinkBook/"
    output_data_to_new_tab_path = 'db/other/'
    # reference
    reference_filter = ''
    reference_contain = ''
    reference_igon_case = True
    reference_smart_link_max_text_len = 120
    reference_smart_link_br_len = 120
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
    history_show_link_count = True

    #exclusive
    exclusive_crossref_path = ['db/library']
    exclusive_local_db_path = 'db/' + default_subject
    exclusive_default_tab = {'twitter' : 'convert'}
    exclusive_append_mode = False


    #filefinder
    filefinder_dirs = ['~/Downloads', 'db']
    filefinder_netdisk_engin = ['pan.baidu', 'onedrive'] #drive  onedrive dropbox
    filefinder_sort_by_count = True


    #preview
    preview_url_args = '' #'?start=' #'?start=0&tag='
    preview_next_page = ''
    preview_page_step = 1
    preview_page_start = 1
    preview_page_max = 4
    preview_frame_width = 471
    preview_frame_height = 700
    preview_frame_check = True
    preview_dict = {ip_adress : {'frame_width' : 770},\
                    'news.baidu' : {'frame_check' : False},\
                    'fhyx' : {'url_args' : '?p=', 'page_step' : 1, 'url_is_base' : True, 'page_max' : 11, 'frame_height' : 2200}}

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
    convert_url_is_base = False
    convert_url_args = '' #'?start=' #'?start=0&tag='
    convert_url_args_2 = ''
    convert_next_page = ''
    convert_no_url_args_4_1st_page = False
    convert_page_step = 1
    convert_page_start = 1
    convert_page_max = 4
    convert_page_to_end = False
    convert_tag = 'a' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 0
    convert_split_column_number = 0
    convert_top_item_number = 0
    convert_output_data_to_new_tab = False
    convert_output_data_to_temp = True
    convert_output_data_format = ''
    convert_cut_start = ''
    convert_cut_start_offset = 0
    convert_cut_end = ''
    convert_cut_end_offset = 0
    convert_cut_to_desc = ''
    convert_remove = []
    convert_replace = {}
    convert_append = ''
    convert_cut_max_len = 1000
    convert_script = ''
    convert_script_custom_ui = False
    convert_smart_engine = 'glucky'
    convert_sort = False
    convert_div_width_ratio = 0 #7.6
    convert_div_height_ratio = 0 #31.8
    convert_show_url_icon = False
    convert_priority = 0 # for sort result from multi source
    convert_stat_enable = False
    convert_stat_field = ['url']
    convert_confirm_argv = False
    convert_removal = True

    convert_pass2 = False
    convert_tag_pass2 = ''
 
    #'''
    convert_engin_dict = {}

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
    website_icons = {'.pdf' : 'http://icons.iconarchive.com/icons/iynque/flat-ios7-style-documents/256/pdf-icon.png',\
                 '.dir' : 'http://cdn.osxdaily.com/wp-content/uploads/2014/05/users-folder-mac-osx.jpg',\
                 'delete' : 'https://cdn2.iconfinder.com/data/icons/duo-toolbar-signs/512/erase-512.png',\
                 'back' : 'https://cdn3.iconfinder.com/data/icons/line/36/undo-512.png',\
                 'data' : 'https://cdn3.iconfinder.com/data/icons/linecons-free-vector-icons-pack/32/data-512.png',\
                 'zoom' : 'https://cdn0.iconfinder.com/data/icons/controls-and-navigation-arrows-1/24/26-512.png',\
                 'homepage' : 'http://grupojvr.com.mx/web/wp-content/uploads/2014/08/Direcci%C3%B3n-azul.png',\
                 'url' : 'https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png',\
                 'website' : 'https://image.flaticon.com/icons/png/128/12/12195.png',\
                 'preview' : 'https://cdn0.iconfinder.com/data/icons/beauty-and-spa-3/512/120-512.png',\
                 'sync' : 'https://cdn.iconscout.com/icon/premium/png-512-thumb/sync-315-382207.png',\
                 'quickaccess' : 'https://images.vexels.com/media/users/3/134216/isolated/preview/cf4ce046e6c36febdf54eaf5b41ffa1f-icono-de-trazo-de-la-estrella-38-by-vexels.png',\
                 'clickcount' : 'http://www.freepngimg.com/download/mouse_cursor_click/1-2-click-free-download-png.png',\
                 'idea' : 'http://icons.iconarchive.com/icons/iconsmind/outline/256/Idea-2-icon.png',\
                 'remark' : 'http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png',\
                 'alias' : 'http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png',\
                 'youtube' : 'https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png',\
                 'y-video' : 'https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png',\
                 'y-channel' : 'https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png',\
                 'y-channel2' : 'https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png',\
                 'y-playlist' : 'https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png',\
                 'amazon' : 'https://cdn2.mhpbooks.com/2016/06/Amazon-icon.png',\
                 'csdn' : 'http://a2.mzstatic.com/us/r30/Purple71/v4/99/61/36/996136cc-f759-5c0c-4531-ee0c6fec786a/icon175x175.png',\
                 'coursera': 'http://techraze.com/wp-content/uploads/2015/06/Coursera-APK-1.png',\
                 'edx' : 'https://icon.apkmirrordownload.com/org.edx.mobile.png',\
                 'udacity' : 'https://www.uplabs.com/assets/integrations/udacity-92b3b2525603489c7c5f325491d0ff44652631210086bb2ab082b897b9b39da0.png',\
                 'github' : 'https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png',\
                 'github-explore' : 'https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png',\
                 'sourcegraph' : 'https://sourcegraph.com/.assets/img/sourcegraph-mark.svg',\
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
                 'reddit-guide' : 'http://icons.iconarchive.com/icons/uiconstock/socialmedia/128/Reddit-icon.png',\
                 'zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'z-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 't-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'c-zhihu' : 'http://a3.mzstatic.com/us/r30/Purple6/v4/6e/e3/2b/6ee32b96-56d5-27b8-ea7a-998dae663ce7/icon175x175.png',\
                 'videolectures' : 'http://ftp.acc.umu.se/mirror/addons.superrepo.org/v7/addons/plugin.video.videolectures.net/icon.png',\
                 'weixin' : 'http://img4.imgtn.bdimg.com/it/u=972460576,3713596294&fm=21&gp=0.jpg',\
                 'chuansong' : 'https://chuansongme.com/static/img/logo-blue.png',\
                 'weibo' : 'https://cdn4.iconfinder.com/data/icons/materia-flat-social-free/24/038_032_sina_weibo_social_network_android_material-512.png',\
                 'twitter' : 'http://itouchappreviewers.com/wp-content/uploads/2015/01/twitter-logo_22.png',\
                 'slack' : 'https://cdn0.iconfinder.com/data/icons/tuts/256/slack_alt.png',\
                 'facebook' : 'http://img.25pp.com/uploadfile/app/icon/20160505/1462390862727305.jpg',\
                 'fb-group' : 'http://img.25pp.com/uploadfile/app/icon/20160505/1462390862727305.jpg',\
                 'g-plus' : 'https://www.easystorehosting.com/wp-content/uploads/2015/06/GooglePlus-Logo-Official.png',\
                 'instagram' : 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/240px-Instagram_icon.png',\
                 'localhost' : 'https://publicportal.teamsupport.com/Images/file.png',\
                 'crossref' : 'https://publicportal.teamsupport.com/Images/file.png',\
                 'command' : 'https://cdn0.iconfinder.com/data/icons/cosmo-multimedia/40/terminal_application-512.png',\
                 'iqiyi' : 'https://images-na.ssl-images-amazon.com/images/I/71ABWNB-YML._SL500_AA300_.png',\
                 'linkedin' : 'https://blogs.cornell.edu/info2040/files/2016/09/LinkedinII-2f706bu.png',\
                 'v.qq' : 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=311155846,3382957541&fm=23&gp=0.jpg',\
                 'douyu' : 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=791058301,37936658&fm=23&gp=0.jpg',\
                 'pan.baidu' : 'http://img0.imgtn.bdimg.com/it/u=3595078885,1850864109&fm=23&gp=0.jpg',\
                 'cnblog' : 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2371619540,33511528&fm=27&gp=0.jpg',\
                 'youku' : 'http://pluspng.com/img-png/logo-youku-png-i-was-invited-by-youku-to-join-this-logo-refresh-project-drawing-this-illustration-gave-me-lots-of-fun-hope-you-guys-like-it-300.png',\
                 'zeef' : 'https://zeef.io/image/24118/300/s?1432128680548',\
                 'discord' : 'http://www.nirthpanter.net/uploads/4/7/2/8/47284995/discord_3_orig.png',\
                 'twitch' : 'https://cdn1.iconfinder.com/data/icons/micon-social-pack/512/twitch-512.png',\
                 'bilibili' : 'http://images.firstpost.com/wp-content/uploads/2017/09/BiliBili-380px.png',\
                 'artstation' : 'https://cdn4.iconfinder.com/data/icons/social-media-2210/24/Artstation-512.png',\
                 'slideshare' : 'http://icons.iconarchive.com/icons/limav/flat-gradient-social/256/Slideshare-icon.png',\
                 'google' : 'https://cdn4.iconfinder.com/data/icons/new-google-logo-2015/400/new-google-favicon-512.png',\
                 'flickr' : 'https://www.icrisat.org/wp-content/uploads/flickr-icon-300x300.png',\
                 'pinterest' : 'https://cdn0.iconfinder.com/data/icons/Pinterest/256/Pinterest_Favicon.png',\
                 'jianshu' : 'https://upload.jianshu.io/collections/images/1956/icon_jianshu.png?imageMogr2/auto-orient/strip|imageView2/1/w/240/h/240',\
                 'archive.org' : 'http://richmondsfblog.com/wp-content/uploads/2016/11/internet-archive-squarelogo.png',\
                 'tieba' : 'https://cdn4.iconfinder.com/data/icons/chinas-social-share-icons/256/cssi_tieba-512.png',\
                 'appveyor' : 'https://www.appveyor.com/assets/img/appveyor-logo-256.png',\
                 'baiduyun' : 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1517551378&di=77dfd3111d5e7b16ea262c3ce893656e&imgtype=jpg&er=1&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F0114ed5945efb4a8012193a3dced37.png',\
                 'mixer' : 'https://mixer.com/_latest/assets/images/main/logos/merge-on-black.png',\
                 'douban' : 'https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg',\
                 'doulist' : 'https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg',\
                 'patreon' : 'http://www.comixlaunch.com/wp-content/uploads/2016/08/patreon-logo-05.jpg',\
                 'steam' : 'http://media.moddb.com/images/members/1/927/926352/profile/steam.png',\
                 'stackexchange' : 'https://cdn.sstatic.net/Sites/stackexchange/img/apple-touch-icon@2.png',\
                 'vine' : 'http://media.idownloadblog.com/wp-content/uploads/2014/03/Vine-1.4.8-for-iOS-app-icon-small-e1404946147708.png',\
                 'nico' : 'https://ddnavi.com/wp-content/uploads/2013/02/img_540644_19961289_0.png',\
                 'wikia' : 'https://images.wikia.com/central/images/b/bc/Wiki.png',\
                 'channel9' : 'https://raw.githubusercontent.com/camalot/plugin.video.microsoft.channel9/master/icon.png',\
                 'soundcloud' : 'http://icons.iconarchive.com/icons/xenatt/minimalism/256/App-SoundCloud-icon.png',\
                 'bitbucket' : 'https://cdn.iconscout.com/icon/free/png-256/bitbucket-226075.png',\
                 'goodreads' : 'https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/goodreads-512.png',\
                 'band' : 'https://upload.wikimedia.org/wikipedia/commons/3/30/2._BAND_Icon.png',\
                 'wordpress' : 'http://nereg.lib.ms.us/wp-content/uploads/2017/04/blog-icon.png',\
                 'blogspot' : 'http://nereg.lib.ms.us/wp-content/uploads/2017/04/blog-icon.png',\
                 'gamepedia' : 'https://static-cdn.jtvnw.net/jtv_user_pictures/gamepedia-profile_image-34322c6bfe2db55c-70x70.png',\
                 'tumblr' : 'https://upload.wikimedia.org/wikipedia/commons/2/2d/New_tumblr_logo.png',\
                 'inoreader' : 'https://images.sftcdn.net/images/t_app-logo-l,f_auto,dpr_auto/p/d83b2000-9b61-11e6-ad29-00163ec9f5fa/1756659416/inoreader-logo.png',\
                 'keybase' : 'https://keybase.io/images/icons/icon-keybase-logo-48.png',\
                 'telegram' : 'https://cdn2.iconfinder.com/data/icons/telegram/154/logotype-telegram-round-blue-logo-512.png',\
                 'iptv.zone' : 'https://iptv.zone/en/images/design/logo256x256.png',\
                 'pscp' : 'https://www.pscp.tv/v/images/largepin.svg',\
                 'relationship' : 'https://cdn3.iconfinder.com/data/icons/glyph/227/Relationship-512.png',\
                 'category' : 'https://cdn2.iconfinder.com/data/icons/shopping-e-commerce-4/100/SC-14-512.png',\
                 'commonlounge' : 'https://d1qb2nb5cznatu.cloudfront.net/startups/i/2529968-d8d3cb035697ed9bf0643bfc8f7406a1-medium_jpg.jpg?buster=1504069939',\
                 'searchin' : 'https://cdn0.iconfinder.com/data/icons/set-of-books-and-reading/32/search-book-512.png',\
                 'meetup' : 'https://www.shareicon.net/data/256x256/2015/09/25/106943_media_512x512.png',\
                 'tagboard' : 'https://cdn-images-1.medium.com/max/1200/1*Dn6hWx7acm7DwYJFnMDAhg.png',\
                 'crunchbase' : 'https://global-uploads.webflow.com/5726ee0d78d342c0529ee26c/594859000194a27e3600ae53_icon-crunchbase.svg',\
                 'disqus' : 'https://i2.wp.com/www.betterhostreview.com/wp-content/uploads/disqus.jpg'}