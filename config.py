#!/usr/bin/env python
# -*- coding: utf-8-*- 

class Config():
    
    default_subject = 'eecs'

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"

    smart_link_engin = 'google'
    smart_link_max_text_len = 60
    smart_link_br_len = 80
    replace_with_smart_link = False

    recommend_engin = True
    recommend_engin_num = 18
    recommend_engin_type = 'star' #ref db/metadata/engin_type

    start_library_title = 'add some record from here!'
    start_library_url = 'http://' + ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3'

    #default_library = ''
    #default_library = 'ai-library'
    #default_library = 'information-library'
    #default_library = 'cognitive-library'
    default_library = 'neuro-library'
    #default_library = 'gene-library'
    #default_library = 'math-phys-chem-library'
    #default_library = 'business-finance-library'
    #default_library = 'medical-library'
    #default_library = 'energy-library'
    #default_library = 'military-library'
    #default_library = 'universe-library'
    #default_library = 'earth-library'
    #default_library = 'social-library'
    #default_library = 'frontier-library'
    #default_library = 'research-library'
    #default_library = 'humanities-library'

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
    second_default_tab = ''#'figures'

    default_width = "79"
    column_num = "1"
    custom_cell_len = 88 
    split_length = custom_cell_len + 15
    custom_cell_row = 5
    cell_len=89  #  cell_len >= course_num_len + 1 + course_name_len + 3
    course_name_len=70
    course_num_len=10
    color_index=0
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

    
    background = ''

    fav_links = { 'papers' : ip_adress + '/?db=eecs/papers/&key=?',\
		  'civilization' : ip_adress + '/?db=other/&key=civilization2016&column=2',\
          'bioRxiv' : 'cshsymposium.com/biorxiv/chartdailydetail.php',\
		  #'github' : ip_adress + '/?db=eecs/projects/github/&key=?',\
          'rss' : ip_adress + '/?db=rss/&key=rss2016',\
          'disk' : ip_adress + '/?db=other/&key=disk2016',\
          'degree' : ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3',\
          #'members' : ip_adress + '/?db=rank/&key=members2016&column=2',\
          'rank' : ip_adress + '/?db=rank/&key=?',\
          #'rank' : ip_adress + '/?db=rank/&key=?',\
		  'youtube' :  ip_adress + '/?db=videos/&key=youtube2016&column=3'}
		  #'eecs' :  ip_adress + '/?db=eecs/&key=?'}
          #'library' : ip_adress + '/?db=library/&key=?'}
		  #'neuroscience' : ip_adress + '/?db=neuroscience/&key=?'}

    
    # ==== extension ====
    # convert
    '''
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
    '''
    #'''
    convert_url_args = '' #'?start=' #'?start=0&tag='
    convert_page_step = 0
    convert_page_start = 0
    convert_page_max = 10
    convert_page_to_end = False
    convert_tag = '' #"div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 6
    convert_split_column_number = 0
    #'''

    delete_from_char = ''
    delete_forward = True
