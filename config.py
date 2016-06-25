#!/usr/bin/env python


class Config():

    #ip_adress="172.16.14.82"
    ip_adress="localhost:5000"
    
    #show random preview when click nav link
    track_mode = False

    disable_default_engin = True
  
    disable_thumb = "false"

    disable_icon = True

    disable_star_engin = False

    disable_reference_image = False 
   
    hiden_record_id = True

    hiden_engins = True
    
    center_content = False
    
    content_margin_left = '15px'
    split_height = '2px'

    #do not show nav links, only show extension links
    extension_mode = False

    default_tab = 'content'
    second_default_tab = 'figures'


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
    max_links_row = 9
    max_nav_link_row = 11
    max_nav_links_row = 7
    default_links_row = 2    

    css_style_type = 6
    plugins_mode = False
