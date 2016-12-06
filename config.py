#!/usr/bin/env python
# -*- coding: utf-8-*- 

class Config():
    
    default_subject = 'eecs'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    # enable urlFromServer  enhancedLink(..., urlFromServer=True)
    # engin query order smart_link_engin -> smart_engin_for_tag -> smart_engin_for_extension
    smart_link_engin = 'glucky' #'google'


    smart_engin_lucky_mode_for_account = True
    smart_engin_for_tag_batch_open = False
    
    #smart_engin_for_tag = {}

    smart_engin_for_tag = {'weixin' : 'weixin'}
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
    command_for_dialog = ['add2library', 'exclusive']
    recommend_engin_type_for_dialog = 'star' #ref db/metadata/engin_type

    smart_link_max_text_len = 60
    smart_link_br_len = 80
    replace_with_smart_link = False

    page_item_count = 100#63

    recommend_engin = True
    recommend_engin_num = 22
    recommend_engin_type = 'star' #ref db/metadata/engin_type

    start_library_title = 'add some record from here!'
    start_library_url = 'http://' + ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3'

    #default_library = ''
    default_library = 'ai-library'
    #default_library = 'engineering-library'
    #default_library = 'multimedia-library'
    #default_library = 'cognitive-library'
    #default_library = 'neuro-library'
    #default_library = 'gene-library'
    #default_library = 'math-library'
    #default_library = 'phys-library'
    #default_library = 'chem-library'
    #default_library = 'business-finance-library'
    #default_library = 'medical-library'
    #default_library = 'energy-library'
    #default_library = 'military(NBC)-library'
    #default_library = 'universe-library'
    #default_library = 'earth-library'
    #default_library = 'social-library'
    #default_library = 'frontier-library'
    #default_library = 'research-library'
    #default_library = 'humanities-art-library'
    #default_library = 'thought-political-library'

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

    default_tab = 'content'
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

    background = ''
    #background = 'https://datacdn.soyo.or.kr/wcont/uploads/2016/02/02164057/alphago_01.jpg'

    fav_links = { 'papers' : ip_adress + '/?db=eecs/papers/&key=?',\
		  'civilization' : ip_adress + '/?db=other/&key=civilization2016&column=2',\
          'bioRxiv' : 'cshsymposium.com/biorxiv/chartdailydetail.php',\
          'rss' : ip_adress + '/?db=rss/&key=rss2016',\
          #'disk' : ip_adress + '/?db=other/&key=disk2016',\
          'github' : ip_adress + '/?db=eecs/projects/github/&key=?',\
          #'ipynb' : 'localhost:8888/tree',\
          #'degree' : ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3',\
          #'members' : ip_adress + '/?db=rank/&key=members2016&column=2',\
          'rank' : ip_adress + '/?db=rank/&key=?',\
          #'rank' : ip_adress + '/?db=rank/&key=?',\
		  'youtube' :  ip_adress + '/?db=videos/&key=youtube2016&column=3'}
		  #'eecs' :  ip_adress + '/?db=eecs/&key=?'}
          #'library' : ip_adress + '/?db=library/&key=?'}
		  #'neuroscience' : ip_adress + '/?db=neuroscience/&key=?'}



    delete_from_char = ''
    delete_forward = True

    # ==== extension ====
    output_data_to_new_tab_path = 'db/other/'
    # reference
    reference_filter = ''
    reference_contain = ''
    reference_igon_case = True
    reference_hiden_engin_section = True
    reference_output_data_to_new_tab = False
    reference_output_data_format = ''

    # bookmark
    bookmark_file_path = "/Users/zd/Downloads/chrome_bookmarks.json"
    bookmark_hiden_engin_section = True
    bookmark_output_data_to_new_tab = False
    bookmark_output_data_format = ''
    bookmark_page_item_count = [16, 14, 12]

    #exclusive
    exclusive_crossref_path = ['db/library']
    exclusive_local_db_path = 'db/' + default_subject

    #filefinder
    filefinder_dirs = ['~/Downloads', 'db']
    filefinder_netdisk_engin = 'pan.baidu'
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
    convert_page_step = 0
    convert_page_start = 0
    convert_page_max = 10
    convert_page_to_end = False
    convert_tag = 'a' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = "@"
    convert_start = 0
    convert_split_column_number = 0
    convert_output_data_to_new_tab = False
    convert_output_data_format = ''
    #'''


    #=====icon====
    enable_website_icon = True
    website_icons = {'.pdf' : 'https://cdn4.iconfinder.com/data/icons/CS5/128/ACP_PDF%202_file_document.png',\
                 'youtube' : 'https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png',\
                 'amazon' : 'http://elianeelias.com/coda/wp-content/uploads/2013/05/Amazon-icon.png',\
                 'csdn' : 'http://a2.mzstatic.com/us/r30/Purple71/v4/99/61/36/996136cc-f759-5c0c-4531-ee0c6fec786a/icon175x175.png',\
                 'coursera': 'http://techraze.com/wp-content/uploads/2015/06/Coursera-APK-1.png',\
                 'edx' : 'https://icon.apkmirrordownload.com/org.edx.mobile.png',\
                 'udacity' : 'https://www.uplabs.com/assets/integrations/udacity-92b3b2525603489c7c5f325491d0ff44652631210086bb2ab082b897b9b39da0.png',\
                 'github' : 'https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png',\
                 'arxiv' : 'http://www.thetelegraphic.com/img/icon-arxiv.png',\
                 'khan' : 'http://academics.cehd.umn.edu/mobile/wp-content/uploads/2013/10/khan-academy-icon.png',\
                 'medium' : 'https://memoriaelectrika.files.wordpress.com/2015/10/mediumlogo002.png',\
                 'mit': 'https://1.bp.blogspot.com/-fhwcWQmSJk4/VsMJ_NzuasI/AAAAAAAAAAo/qoBFDEJLnwI/w800-h800/images.png',\
                 'stanford' : 'https://identity.stanford.edu/overview/images/emblems/SU_New_BlockStree_2color.png',
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
                 'videolectures' : 'http://ftp.acc.umu.se/mirror/addons.superrepo.org/v7/addons/plugin.video.videolectures.net/icon.png'}