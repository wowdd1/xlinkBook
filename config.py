#!/usr/bin/env python
# -*- coding: utf-8-*- 

class Config():
    
    default_subject = 'eecs'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    # enable urlFromServer  enhancedLink(..., urlFromServer=True)
    # engin query order smart_link_engin -> smart_engin_for_tag -> smart_engin_for_extension
    smart_link_engin = 'google' #'glucky'


    smart_engin_lucky_mode_for_account = True
    smart_engin_for_tag = {}
    '''
    smart_engin_for_tag = {'instructors' : ['twitter', 'youtube'],\
                           'university' : 'youtube',\
                           'professor' : ['phdtree', 'glucky'],\
                           'g-plus' : 'plus.google',\
                           'company' : 'glucky',\
                           'website' : 'glucky',\
                           'director' : ['twitter', 'glucky']}
                           #'topic' : ''}
    '''
    
    smart_engin_for_extension = {'' : ''}

    #smart_engin_for_dialog = ['google', 'youtube', 'twitter', 'baidu']
    smart_engin_for_dialog = []
    command_for_dialog = ['add2library', 'exclusive']
    recommend_engin_type_for_dialog = 'star' #ref db/metadata/engin_type

    smart_link_max_text_len = 60
    smart_link_br_len = 80
    replace_with_smart_link = False

    page_item_count = 63

    recommend_engin = True
    recommend_engin_num = 20
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
    bookmark_page_item_count = 12

    #filefinder
    filefinder_dirs = ['~/Downloads', 'db']

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
    convert_tag = 'td' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 0
    convert_split_column_number = 0
    convert_hiden_engin_section = False
    convert_output_data_to_new_tab = False
    convert_output_data_format = ''
    #'''