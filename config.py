#!/usr/bin/env python
# -*- coding: utf-8-*-


class Config:

    # default_db = 'db'
    default_subject = "eecs"

    default_db = "db"  #'2016-db'

    user_name = "wowdd1"

    # ip_adress="172.16.14.82"
    # ip_adress="localhost:5000"

    localPort = "5000"
    remotePort = "5555"
    ip_adress = "localhost:" + localPort

    proxyPort = "7891"

    # SSR
    proxies1 = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087",
    }
    # Trojan
    # proxies1 = {
    #    "http": "http://127.0.0.1:10887",
    #    "https": "http://127.0.0.1:10887",
    # }

    proxies2 = {
        "http": "http://127.0.0.1:8787",
        "https": "http://127.0.0.1:8787",
    }

    proxies3 = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",
    }

    proxies4 = {
        "http": "http://192.168.10.103:7890",
        "https": "https://192.168.10.103:7890",
    }

    proxies = proxies4

    igon_authorized = True

    engin_list_file = "db/metadata/engin_list"
    engin_type_file = "db/metadata/engin_type"
    engin_extension_file = "db/metadata/engin_extension"

    # smart_link_style = "font-family:San Francisco;"
    smart_link_style = "font-family:PingFang SC;"
    # smart_link_style = "font-family:New York;"
    # smart_link_style = "font-family:MonoLisa;"
    # enable urlFromServer  enhancedLink(..., urlFromServer=True)
    # engin query order smart_link_engin -> smart_engin_for_tag -> smart_engin_for_extension
    smart_link_engin = "glucky"  #'google'
    default_engin_searchbox = "zhihu"

    igon_log_for_modules = ["star", "exclusive", "content", "bookmark"]  # dialog
    more_button_for_history_module = True

    smart_engin_lucky_mode_for_account = True
    smart_engin_for_tag_batch_open = False
    smart_engin_for_command_batch_open = ["twitter", "baidu", "amazon"]
    max_account_for_tag_batch_open = 10
    open_all_link_in_one_page = True
    open_all_link_in_frameset_mode = False
    max_last_open_urls = 7

    recommend_engin = True
    recommend_engin_num = 32
    recommend_engin_num_dialog = 10
    recommend_engin_num_dialog_row = 5
    recommend_engin_type = "star"  # ref db/metadata/engin_type
    recommend_engin_dict = {}  # {'multimedia-library' : 'google baidu'}
    recommend_engin_by_tag = False

    # smart_engin_for_tag = {}

    smart_engin_for_tag = {
        "weixin": [
            "weixin.so",
            "weixinla",
            "chuansong",
            "toutiao",
            "weibo",
            "qoofan.com",
            "glucky",
        ],
        "fb-pages": ["fb-pages", "glucky"],
        "baijiahao": ["baijiahao"],
        "conference": ["glucky", "google", "d:event"],
        "social-tag": "d:socialtag",
    }
    """

    smart_engin_for_tag = {'instructors' : ['twitter', 'youtube'],\
                           'university' : 'youtube',\
                           'professor' : ['phdtree', 'glucky'],\
                           'g-plus' : 'plus.google',\
                           'company' : 'glucky',\
                           'website' : 'glucky',\
                           'director' : ['twitter', 'glucky'],\
                           'job' : ['google', 'd:job']}
                           #'topic' : ''}
    """

    # smart_engin_for_extension = {'' : ''}

    # smart_engin_for_dialog = ['google', 'youtube', 'twitter', 'baidu']
    smart_engin_for_dialog = []
    command_for_dialog = ["add2library", "add2qa", "trace", "kgraph", "exclusive"]
    command_for_tag_dialog = ["tolist", "merger"]

    recommend_engin_type_for_dialog = ""  #'star' #ref db/metadata/engin_type

    smart_link_max_text_len = 60
    smart_link_br_len = 60
    replace_with_smart_link = False

    page_item_count = 100  # 63

    start_library_title = "add some record from here!"
    start_library_url = (
        "http://" + ip_adress + "/?db=other/&key=degree-chart-mit2016&column=3"
    )

    menu_library_list = [
        "ai-library",
        "multimedia-library",
        "mind-library",
        "neuro-library",
        "gene-library",
        "math-library",
        "phys-library",
        "chem-library",
        "business-finance-library",
        "engineering-library",
        "product-library",
        "manage-library",
        "art-library",
    ]
    default_library_filter = ""
    # default_library_filter = 'Video Game#orGame Engine#orRendering Engine'
    # default_library = ''
    default_library = "multimedia-library"  #'ai-library'
    # default_library = 'engineering-library'
    # default_library = 'multimedia-library'
    # default_library = 'mind-library'
    # default_library = 'neuro-library'
    # default_library = 'gene-library'
    # default_library = 'math-library'
    # default_library = 'phys-library'
    # default_library = 'chem-library'
    # default_library = 'business-finance-library'
    # default_library = 'medical-library'
    # default_library = 'energy-library'
    # default_library = 'aerospace-library'
    # default_library = 'universe-library'
    # default_library = 'earth-library'
    # default_library = 'social-library'
    # default_library = 'art-library'
    # default_library = 'literature-library'
    # default_library = 'manage-library'
    # default_library = 'thought-library'
    # default_library = 'media-library'
    # default_library = 'telecom-library'
    # default_library = 'manufacture-library'
    # default_library = 'traffic-library'
    # default_library = 'retail-library'
    # default_library = 'building-library'
    # default_library = 'life-library'
    # default_library = 'sport-library'
    # default_library = 'entertainment-library'
    # default_library = 'military-library'
    # default_library = 'product-library'
    # default_library = 'research-library'

    # show random preview when click nav link

    search_mode = True

    searchinLoopSearch = False

    autoAppendDescFilterCategory = False

    tagAliasDict = {"desc:": "description:", "tag:": "alias:"}

    track_mode = False

    disable_default_engin = True

    disable_nav_engins = True  # it take 2s for gen nav engins html

    disable_thumb = "false"

    disable_icon = True

    disable_star_engin = False

    disable_reference_image = False

    hiden_record_id = True
    hiden_record_id_commandline = False
    hiden_parentid_record = True

    hiden_engins = True

    center_content = False

    content_margin_left = "15px"
    content_margin_top = "10px"

    split_height = 2
    title_font_size = 0

    # do not show nav links, only show extension links
    extension_mode = False

    # handle by handleQueryNavTab of app.py first
    default_tab = "history"  #'content'
    second_default_tab = "bookmark"  #'figures'

    default_width = "54"  # "79"
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
    background_after_click = "#E9967A"  ##CCEEFF
    fontsize_after_click = ""

    fav_links = {  #'arxiv' : ip_adress + '/?db=eecs/papers/arxiv/&key=?',\
        "civilization": ip_adress
        + "/?db=other/&key=civilization2018&column=2",  #'bioRxiv' : 'cshsymposium.com/biorxiv/chartdailydetail.php',\
        "db": ip_adress + "/?db=?",  #'rss' : ip_adress + '/?db=rss/&key=rss2016',\
        #'disk' : ip_adress + '/?db=other/&key=disk2016',\
        #'github' : ip_adress + '/?db=eecs/projects/github/&key=?',\
        #'ipynb' : 'localhost:8888/tree',\
        #'degree' : ip_adress + '/?db=other/&key=degree-chart-mit2016&column=3',\
        #'members' : ip_adress + '/?db=rank/&key=members2016&column=2',\
        "rank": ip_adress
        + "/?db=rank/&key=?",  #'paperbot' : 'https://web.paperbot.ai/',\
        #'iris.ai' : 'https://the.iris.ai/explore',\
        "roadmap": ip_adress + "/?db=other/&key=roadmap",
        "frontier": ip_adress + "/?db=other/&key=frontier2018",
    }
    #'eecs' :  ip_adress + '/?db=eecs/&key=?'}
    #'library' : ip_adress + '/?db=library/&key=?'}
    #'neuroscience' : ip_adress + '/?db=neuroscience/&key=?'}

    distribution = False
    slack_token = ["xoxb", "156129958533", "YdIXSA2syy7ipacDQo6cr03j"]

    delete_from_char = ""
    delete_forward = True

    application_dict = {
        ".ppt": "/Applications/Preview.app/Contents/MacOS/Preview",
        ".pptx": "/Applications/Preview.app/Contents/MacOS/Preview",  #'.py' : '/Applications/Sublime Text.app/Contents/MacOS/Sublime Text',\
        #'.epub' : '/Applications/iBooks.app/Contents/MacOS/iBooks',\
        ".epub": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ".key": "/Applications/Keynote.app/Contents/MacOS/Keynote",
        ".mp4": "/Applications/IINA.app/Contents/MacOS/IINA",  #'*' : '/Applications/Microsoft Edge Canary.app/Contents/MacOS/Microsoft Edge Canary'}
        "*": "/Applications/Thorium.app/Contents/MacOS/Thorium",
    }
    #'*' : '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}

    application_protocol_dict = {"hook://": "open"}

    enable_save_onhover_url = False
    # ==== extension ====
    one_page_path_root = "file:///Users/" + user_name + "/dev/xlb_env/xlinkBook/"
    output_data_to_new_tab_path = "db/other/"
    # reference
    reference_filter = ""
    reference_contain = ""
    reference_igon_case = True
    reference_smart_link_max_text_len = 120
    reference_smart_link_br_len = 120
    reference_hiden_engin_section = True
    reference_output_data_to_new_tab = False
    reference_output_data_format = ""

    # bookmark
    # bookmark_file_path = "/Users/" + user_name + "/Downloads/chrome_bookmarks.json"
    bookmark_file_path = (
        "/home/wowdd1/.xlb-env/xlinkBook/extensions/bookmark/chrome_bookmarks.json"
    )
    bookmark_hiden_engin_section = True
    bookmark_output_data_to_new_tab = False
    bookmark_output_data_format = ""
    bookmark_page_item_count = [16, 14, 12]

    # history
    history_file_path = "/Users/" + user_name + "/Downloads/chrome_history.json"
    history_hiden_engin_section = True
    hidtory_sort_type = 0  # 0: click count 1: url 2: title
    history_show_click_count = False
    history_enable_subitem_log = False
    history_enable_quick_access = True
    history_quick_access_item_count = 5
    history_quick_access_name = "Quick Access"
    history_show_link_count = True

    # exclusive
    exclusive_crossref_path = ["db/library"]
    exclusive_local_db_path = "db/" + default_subject
    exclusive_default_tab = {"twitter": "convert"}
    exclusive_append_mode = False

    # edit
    sync_data_to_cloud = True

    # filefinder
    filefinder_dirs = ["~/Downloads", "db"]
    filefinder_netdisk_engin = ["pan.baidu", "onedrive"]  # drive  onedrive dropbox
    filefinder_sort_by_count = True

    # preview
    preview_url_args = ""  #'?start=' #'?start=0&tag='
    preview_next_page = ""
    preview_page_step = 1
    preview_page_start = 1
    preview_page_max = 4
    preview_frame_width = 471
    preview_frame_height = 700
    preview_frame_check = True
    preview_dict = {
        ip_adress: {"frame_width": 770},
        "news.baidu": {"frame_check": False},
        "fhyx": {
            "url_args": "?p=",
            "page_step": 1,
            "url_is_base": True,
            "page_max": 11,
            "frame_height": 2200,
        },
    }

    # content
    content_hiden_engin_section = True

    # convert
    """ default config
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
    """
    #'''
    convert_url_is_base = False
    convert_url_args = ""  #'?start=' #'?start=0&tag='
    convert_url_args_2 = ""
    convert_next_page = ""
    convert_no_url_args_4_1st_page = False
    convert_page_step = 1
    convert_page_start = 1
    convert_page_max = 4
    convert_page_to_end = False
    convert_tag = "a"  # "div#title"  # tag#class or tag
    convert_min_num = 0
    convert_max_num = 1000
    convert_filter = ""
    convert_contain = ""
    convert_start = 0
    convert_split_column_number = 0
    convert_top_item_number = 0
    convert_output_data_to_new_tab = False
    convert_output_data_to_temp = True
    convert_output_data_format = ""
    convert_cut_start = ""
    convert_cut_start_offset = 0
    convert_cut_end = ""
    convert_cut_end_offset = 0
    convert_cut_to_desc = ""
    convert_remove = []
    convert_replace = {}
    convert_append = ""
    convert_cut_max_len = 1000
    convert_script = ""
    convert_script_custom_ui = False
    convert_smart_engine = "glucky"
    convert_sort = False
    convert_div_width_ratio = 0  # 7.6
    convert_div_height_ratio = 0  # 31.8
    convert_show_url_icon = False
    convert_priority = 0  # for sort result from multi source
    convert_stat_enable = False
    convert_stat_field = ["url"]
    convert_confirm_argv = False
    convert_removal = True

    convert_pass2 = False
    convert_tag_pass2 = ""

    #'''
    convert_engin_dict = {}

    convert_lazyload = 0

    # =====bk====
    background = 0
    backgrounds = [
        "",
        "http://img.blog.csdn.net/20161213000422101",
        "https://datacdn.soyo.or.kr/wcont/uploads/2016/02/02164057/alphago_01.jpg",
        "http://img.blog.csdn.net/20150506120021512?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd293ZGQx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center",
        "http://img.blog.csdn.net/20161227171638323",
        "http://images.njcw.com/upload/2011-5/201105071635561829723_w.jpg",
        "http://www.caneis.com.tw/link/info/Middle_East_info/Egypt/images/Cairo-007-1.jpg",
        "https://cdn-images-1.medium.com/max/2000/1*BTGKRLq55y8Hld9pyvarXg.png",
        "http://st.depositphotos.com/1007919/3724/i/950/depositphotos_37248955-stock-photo-binary-background.jpg",
        "http://amazingstuff.co.uk/wp-content/uploads/2012/02/scale_of_the_universe_2.png",
        "https://curiositando.files.wordpress.com/2014/12/cervello_destro1.jpg",
        "http://img1.voc.com.cn/UpLoadFile/2013/03/05/201303051655526838.jpg",
        "http://p1.pstatp.com/large/530000529b6125ce87c",
        "http://zdnet4.cbsistatic.com/hub/i/r/2016/06/01/8a90fae5-22f7-480b-9ea5-a4f6252e7ed0/resize/1170x878/d756410179b9c71086b1496f4b924556/001.jpg",
        "http://tc.sinaimg.cn/maxwidth.2048/tc.service.weibo.com/s9_rr_itc_cn/000254925dab8674da3fb790364ddcf0.png",
    ]

    # =====icon====
    enable_website_icon = True
    website_icons = {
        ".pdf": "http://icons.iconarchive.com/icons/iynque/flat-ios7-style-documents/256/pdf-icon.png",
        ".dir": "https://blog.macsales.com/wp-content/uploads/2017/04/Folder-Apps-icon.png",
        "delete": "https://cdn2.iconfinder.com/data/icons/color-svg-vector-icons-part-2/512/erase_delete_remove_wipe_out-512.png",
        "save": "https://icons.veryicon.com/png/o/miscellaneous/utility/save-44.png",
        "back": "https://cdn3.iconfinder.com/data/icons/line/36/undo-512.png",
        "data": "https://cdn3.iconfinder.com/data/icons/linecons-free-vector-icons-pack/32/data-512.png",
        "class": "https://cdn3.iconfinder.com/data/icons/developer-files-1-add-on/48/v-07-512.png",
        "run": "https://cdn2.iconfinder.com/data/icons/ico-nic-script/128/Script_Code_Html_Macro_Source_Command_Batch_Shell_Procedure_Function_Php_Css_Javascript_Roll_Scroll_Text_Document_Play_Run_Execute_Playback_Test_Launch-512.png",
        "edit": "http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png",
        "edit2": "https://cdn3.iconfinder.com/data/icons/cool-application-icons/512/pencil-512.png",
        "zoom": "https://cdn0.iconfinder.com/data/icons/controls-and-navigation-arrows-1/24/26-512.png",
        "zoom-more": "https://cdn3.iconfinder.com/data/icons/ui-9/512/zoom_in-512.png",
        "grid": "https://cdn4.iconfinder.com/data/icons/solid-pt-1/48/Artboard_19-512.png",
        "list": "https://cdn4.iconfinder.com/data/icons/lineo/100/menu-512.png",
        "group": "https://cdn2.iconfinder.com/data/icons/pittogrammi/142/88-512.png",
        "help": "https://cdn4.iconfinder.com/data/icons/vectory-symbols/40/help_1-512.png",
        "clustering": "https://cdn0.iconfinder.com/data/icons/coding-and-programming/64/cluster-group-similar-occuring-together-512.png",
        "question": "https://cdn1.iconfinder.com/data/icons/superthick-app-ui/128/about-question-mark-512.png",
        "tabs": "https://cdn0.iconfinder.com/data/icons/internet/512/e53-512.png",
        "search": "https://upload.wikimedia.org/wikipedia/commons/3/36/Search_Icon.png",
        "add": "https://www.freeiconspng.com/uploads/add-icon--line-iconset--iconsmind-29.png",
        "homepage": "http://grupojvr.com.mx/web/wp-content/uploads/2014/08/Direcci%C3%B3n-azul.png",
        "url": "https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png",
        "website": "https://cdn4.iconfinder.com/data/icons/software-line/32/software-line-02-512.png",
        "preview": "https://cdn0.iconfinder.com/data/icons/beauty-and-spa-3/512/120-512.png",
        "sync": "https://cdn.iconscout.com/icon/premium/png-512-thumb/sync-315-382207.png",
        "quickaccess": "https://images.vexels.com/media/users/3/134216/isolated/preview/cf4ce046e6c36febdf54eaf5b41ffa1f-icono-de-trazo-de-la-estrella-38-by-vexels.png",
        "clickcount": "http://www.freepngimg.com/download/mouse_cursor_click/1-2-click-free-download-png.png",
        "idea": "http://icons.iconarchive.com/icons/iconsmind/outline/256/Idea-2-icon.png",
        "remark": "http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png",
        "alias": "http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png",
        "youtube": "https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png",
        "y-video": "https://cdn-icons-png.flaticon.com/512/408/408706.png",
        "y-channel": "https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png",
        "y-channel2": "https://cdn1.iconfinder.com/data/icons/google_jfk_icons_by_carlosjj/512/youtube.png",
        "y-playlist": "https://cdn-icons-png.freepik.com/256/18904/18904010.png?semt=ais_white_label",
        "y-stream": "https://i.pinimg.com/474x/e9/f2/74/e9f274f615609782b5b7277a410c950c.jpg",
        "rutube": "https://www.geoclip.ru/wp-content/uploads/2025/04/rutube2-300x300.png",
        "r-playlist": "https://www.geoclip.ru/wp-content/uploads/2025/04/rutube2-300x300.png",
        "r-video": "https://www.geoclip.ru/wp-content/uploads/2025/04/rutube2-300x300.png",
        "pornhub": "https://img.icons8.com/color/512/pornhub.png",
        "randomstreetview": "https://cdn-1.webcatalog.io/catalog/random-street-view/random-street-view-icon-filled-256.png?v=1747108310570",
        "amazon": "https://cdn2.mhpbooks.com/2016/06/Amazon-icon.png",
        "csdn": "http://i5.res.meizu.com/fileserver/app_icon/10168/516778ee566f4d8990eeba4af2993468.png",
        "blog.csdn": "http://i5.res.meizu.com/fileserver/app_icon/10168/516778ee566f4d8990eeba4af2993468.png",
        "coursera": "http://techraze.com/wp-content/uploads/2015/06/Coursera-APK-1.png",
        "edx": "https://icon.apkmirrordownload.com/org.edx.mobile.png",
        "udacity": "https://www.uplabs.com/assets/integrations/udacity-92b3b2525603489c7c5f325491d0ff44652631210086bb2ab082b897b9b39da0.png",
        "social": "https://png.pngtree.com/element_our/sm/20180630/sm_5b37e98164221.jpg",
        "news": "https://cdn-icons-png.flaticon.com/512/21/21601.png",
        "github": "https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png",
        "ossinsight": "https://pbs.twimg.com/profile_images/1552204750778933248/-th9IlGt_400x400.jpg",
        "huggingface": "https://huggingface.co/front/assets/huggingface_logo-noborder.svg",
        "hugging_face": "https://huggingface.co/front/assets/huggingface_logo-noborder.svg",
        "linux_do": "https://avatars.githubusercontent.com/u/160804563?s=200&v=4",
        "paperswithcode": "https://paperswithcode.com/static/logo.png",
        "civitai": "https://cdn-1.webcatalog.io/catalog/civitai/civitai-icon-filled-256.png?v=1676420128023",
        "replicate": "https://replicate.com/static/apple-touch-icon.1adc51db122a.png",
        "modelscope": "https://img.alicdn.com/imgextra/i4/O1CN01fvt4it25rEZU4Gjso_!!6000000007579-2-tps-128-128.png",
        "colab": "https://shinji-blog.com/wp-content/uploads/2019/02/colab_favicon_256px.png",
        "replit": "https://i.pinimg.com/736x/b8/ac/83/b8ac8361c21fd81668b5cb0bb0e77343.jpg",
        "docker": "https://cdn-icons-png.flaticon.com/512/919/919853.png",
        "github-explore": "https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png",
        "analyze": "https://cdn0.iconfinder.com/data/icons/data-charts/110/Line-512.png",
        "fork": "https://cdn.iconscout.com/icon/premium/png-256-thumb/code-fork-3660188-3053530.png",
        "release": "https://icon2.cleanpng.com/20180421/yjq/kisspng-arrow-computer-icons-circle-5adb9e2eae7ec8.9261291015243423187147.jpg",
        "ide": "https://cdn0.iconfinder.com/data/icons/social-media-logo-4/32/Social_Media_vs_code_visual_studio_code-512.png",
        "similar": "https://cdn4.iconfinder.com/data/icons/math-numbers-solid/24/approximation-solid-512.png",
        "similar2": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQn_uvKp8uCSiwV6dZDsvGP-vRmY_OD1pQzg&s",
        "chatgpt": "https://cdn-icons-png.flaticon.com/512/12222/12222588.png",
        "chat": "https://cdn-icons-png.flaticon.com/512/14/14558.png",
        "alternative": "https://icons.veryicon.com/png/o/miscellaneous/smarteditor/replace-pictures.png",
        "star": "https://cdn3.iconfinder.com/data/icons/sympletts-free-sampler/128/star-512.png",
        "combine": "https://cdn-icons-png.flaticon.com/512/3580/3580056.png",
        "talk": "https://cdn1.iconfinder.com/data/icons/lemu-broadcasting/100/talk_bold_convert-512.png",
        "extension": "https://images.icon-icons.com/1369/PNG/512/-extension_90746.png",
        "oschina": "https://boostnote.io/assets/img/oschina.png",
        "gitee": "https://plugins.jetbrains.com/files/11491/268641/icon/pluginIcon.png",
        "libhunt": "https://www.libhunt.com/assets/logo/logo-square-59c7e305a0cf44062d1ee926560b6384cfb5b175590450cf104dc46b3710ed62.png",
        "awesomeopensource": "https://awesomeopensource.com/awesome.gif",
        "sourcegraph": "https://sourcegraph.com/.assets/img/sourcegraph-mark.svg",
        "gitlab": "https://icon2.kisspng.com/20180429/sxw/kisspng-gitlab-logo-source-code-computer-software-continuo-5ae5d671998d87.677115291525012081629.jpg",
        "arxiv": "http://www.thetelegraphic.com/img/icon-arxiv.png",
        "khan": "http://academics.cehd.umn.edu/mobile/wp-content/uploads/2013/10/khan-academy-icon.png",
        "medium": "https://memoriaelectrika.files.wordpress.com/2015/10/mediumlogo002.png",
        "mit": "https://1.bp.blogspot.com/-fhwcWQmSJk4/VsMJ_NzuasI/AAAAAAAAAAo/qoBFDEJLnwI/w800-h800/images.png",
        "stanford": "https://d9tyu2epg3boq.cloudfront.net/institutions/stanford.png",
        "berkeley": "https://cdn4.iconfinder.com/data/icons/interior-and-buildings-9/68/66-512.png",
        "cmu": "http://www.wholeren.com/wp-content/uploads/2015/04/Carnegie_Mellon_University_CMU_1015361.png",
        "harvard": "http://tusm.3daystartup.org/files/2013/03/harvard.png",
        "oxford": "http://cdn.shopify.com/s/files/1/0581/9089/products/neck_label_option_1.png?v=1456393100",
        "cambridge": "http://a5.mzstatic.com/us/r30/Purple1/v4/6a/cf/d8/6acfd890-9467-f907-5092-5198e091fe04/icon256.png",
        "wikipedia": "http://vignette3.wikia.nocookie.net/everythingmarioandluigi/images/e/e8/Wikipedia_icon.png/revision/latest?cb=20130709180530",
        "stackoverflow": "http://cdn.sstatic.net/Sites/stackoverflow/company/img/logos/so/so-icon.png?v=c78bd457575a",
        "quora": "https://cdn4.iconfinder.com/data/icons/miu-flat-social/60/quora-128.png",
        "reddit": "http://icons.iconarchive.com/icons/uiconstock/socialmedia/128/Reddit-icon.png",
        "reddit-guide": "http://icons.iconarchive.com/icons/uiconstock/socialmedia/128/Reddit-icon.png",
        "lihkg": "https://upload.wikimedia.org/wikipedia/en/thumb/8/8c/LIHKG_logo.png/80px-LIHKG_logo.png",
        "zhihu": "https://www.shareicon.net/data/128x128/2015/08/24/90228_china_512x512.png",
        "z-zhihu": "https://www.shareicon.net/data/128x128/2015/08/24/90228_china_512x512.png",
        "t-zhihu": "https://www.shareicon.net/data/128x128/2015/08/24/90228_china_512x512.png",
        "c-zhihu": "https://www.shareicon.net/data/128x128/2015/08/24/90228_china_512x512.png",
        "v2ex": "https://www.v2ex.com/static/icon-192.png",
        "videolectures": "http://ftp.acc.umu.se/mirror/addons.superrepo.org/v7/addons/plugin.video.videolectures.net/icon.png",
        "weixin": "https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/371_Wechat_logo-512.png",
        "chuansong": "https://chuansongme.com/static/img/logo-blue.png",
        "weibo": "https://cdn4.iconfinder.com/data/icons/materia-flat-social-free/24/038_032_sina_weibo_social_network_android_material-512.png",
        "twitter": "https://www.iconpacks.net/icons/2/free-twitter-logo-icon-2429-thumb.png",
        "tiktok": "https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/tiktok-icon.png",
        "douyin": "https://www.eternityx.com/wp-content/uploads/2022/04/Douyin-%E6%8A%96%E9%9F%B3-Logo.png",
        "slack": "https://cdn0.iconfinder.com/data/icons/tuts/256/slack_alt.png",
        "rocket": "https://dashboard.snapcraft.io/site_media/appmedia/2018/12/icon-256_sDZsivC.png",
        "facebook": "https://cdn1.iconfinder.com/data/icons/logotypes/32/square-facebook-512.png",
        "fb-group": "https://cdn1.iconfinder.com/data/icons/logotypes/32/square-facebook-512.png",
        "g-plus": "https://www.easystorehosting.com/wp-content/uploads/2015/06/GooglePlus-Logo-Official.png",
        "instagram": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/240px-Instagram_icon.png",
        "localhost": "https://icones.pro/wp-content/uploads/2021/06/icone-fichier-document-noir.png",
        "copy": "https://cdn.icon-icons.com/icons2/1875/PNG/512/copy_120015.png",
        "crossref": "https://icones.pro/wp-content/uploads/2021/06/icone-fichier-document-noir.png",
        "command": "https://cdn0.iconfinder.com/data/icons/cosmo-multimedia/40/terminal_application-512.png",
        "iqiyi": "https://images-na.ssl-images-amazon.com/images/I/71ABWNB-YML._SL500_AA300_.png",
        "linkedin": "https://blogs.cornell.edu/info2040/files/2016/09/LinkedinII-2f706bu.png",
        "cbinsights": "https://seeklogo.com/images/C/cb-insights-logo-8B9B0CD6B5-seeklogo.com.png",
        "v.qq": "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=311155846,3382957541&fm=23&gp=0.jpg",
        "douyu": "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=791058301,37936658&fm=23&gp=0.jpg",
        "pan.baidu": "https://img.favpng.com/1/25/7/baidu-wangpan-logo-illustration-image-png-favpng-AkSbBsNBRDU6S79LYhrxgHWAL.jpg",
        "cnblog": "https://png.pngtree.com/svg/20170425/72dc1fe78b.svg",
        "youku": "http://pluspng.com/img-png/logo-youku-png-i-was-invited-by-youku-to-join-this-logo-refresh-project-drawing-this-illustration-gave-me-lots-of-fun-hope-you-guys-like-it-300.png",
        "zeef": "https://zeef.io/image/24118/300/s?1432128680548",
        "discord": "https://b.thumbs.redditmedia.com/OIDktcKCqI8n4CnTj2SNZAQtXjBWxo9Qah6ku96YsME.png",
        "twitch": "https://cdn1.iconfinder.com/data/icons/micon-social-pack/512/twitch-512.png",
        "bilibili": "https://user-images.githubusercontent.com/9050713/39107515-619773e0-46f5-11e8-9fa9-2859816f1c42.png",
        "artstation": "https://cdn4.iconfinder.com/data/icons/social-media-2210/24/Artstation-512.png",
        "slideshare": "http://icons.iconarchive.com/icons/limav/flat-gradient-social/256/Slideshare-icon.png",
        "google": "https://cdn4.iconfinder.com/data/icons/new-google-logo-2015/400/new-google-favicon-512.png",
        "flickr": "https://www.icrisat.org/wp-content/uploads/flickr-icon-300x300.png",
        "pinterest": "https://cdn0.iconfinder.com/data/icons/Pinterest/256/Pinterest_Favicon.png",
        "jianshu": "https://upload.jianshu.io/collections/images/1956/icon_jianshu.png?imageMogr2/auto-orient/strip|imageView2/1/w/240/h/240",
        "archive.org": "http://richmondsfblog.com/wp-content/uploads/2016/11/internet-archive-squarelogo.png",
        "tieba": "https://cdn4.iconfinder.com/data/icons/chinas-social-share-icons/256/cssi_tieba-512.png",
        "appveyor": "https://www.appveyor.com/assets/img/appveyor-logo-256.png",
        "baiduyun": "http://www.1mtb.com/wp-content/uploads/2014/06/How-To-Get-2-TB-Free-Cloud-Storage-Space-On-Baidu-Pan-Baidu-Cloud.png",
        "mixer": "https://mixer.com/_latest/assets/images/main/logos/merge-on-black.png",
        "douban": "https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg",
        "doulist": "https://img3.doubanio.com/pview/event_poster/raw/public/8147be751c6567f.jpg",
        "patreon": "http://www.comixlaunch.com/wp-content/uploads/2016/08/patreon-logo-05.jpg",
        "steam": "http://media.moddb.com/images/members/1/927/926352/profile/steam.png",
        "stackexchange": "https://cdn.sstatic.net/Sites/stackexchange/img/apple-touch-icon@2.png",
        "vine": "http://media.idownloadblog.com/wp-content/uploads/2014/03/Vine-1.4.8-for-iOS-app-icon-small-e1404946147708.png",
        "nico": "https://ddnavi.com/wp-content/uploads/2013/02/img_540644_19961289_0.png",
        "wikia": "https://images.wikia.com/central/images/b/bc/Wiki.png",
        "fandom": "https://images.wikia.com/central/images/b/bc/Wiki.png",
        "channel9": "https://raw.githubusercontent.com/camalot/plugin.video.microsoft.channel9/master/icon.png",
        "soundcloud": "http://icons.iconarchive.com/icons/xenatt/minimalism/256/App-SoundCloud-icon.png",
        "bitbucket": "https://cdn.iconscout.com/icon/free/png-256/bitbucket-226075.png",
        "goodreads": "https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/goodreads-512.png",
        "band": "https://upload.wikimedia.org/wikipedia/commons/3/30/2._BAND_Icon.png",
        "wordpress": "https://cdn0.iconfinder.com/data/icons/social-network-9/50/27-512.png",
        "blogspot": "https://cdn0.iconfinder.com/data/icons/social-network-9/50/27-512.png",
        "gamepedia": "https://static-cdn.jtvnw.net/jtv_user_pictures/gamepedia-profile_image-34322c6bfe2db55c-70x70.png",
        "tumblr": "https://upload.wikimedia.org/wikipedia/commons/2/2d/New_tumblr_logo.png",
        "inoreader": "https://images.sftcdn.net/images/t_app-logo-l,f_auto,dpr_auto/p/d83b2000-9b61-11e6-ad29-00163ec9f5fa/1756659416/inoreader-logo.png",
        "keybase": "https://keybase.io/images/icons/icon-keybase-logo-48.png",
        "telegram": "https://cdn2.iconfinder.com/data/icons/telegram/154/logotype-telegram-round-blue-logo-512.png",
        "shokichan": "https://app.shokichan.com/shoki.png",
        "iptv.zone": "https://iptv.zone/en/images/design/logo256x256.png",
        "pscp": "https://www.pscp.tv/v/images/largepin.svg",
        "juejin": "https://b-gold-cdn.xitu.io/v3/static/img/logo.a7995ad.svg",
        "toutiao": "https://upload.wikimedia.org/wikipedia/en/thumb/7/73/ToutiaoLogo2017.png/200px-ToutiaoLogo2017.png",
        "topbuzz": "https://3.bp.blogspot.com/-8IO2lid6VrM/WxWovZ2s87I/AAAAAAAAAB8/6dikyvOvOGIQ4OOx3pW_IDekiD77wBXjQCLcBGAs/s320/images.jpeg",
        "lizhi": "http://www.lizhi.fm/assets/images/c98fc30ffe142b8d084d2f7450a88e8f-newlogo.png",
        "skype": "https://cdn3.iconfinder.com/data/icons/flat-icons-web/40/Skype-512.png",
        "chart": "http://icons.iconarchive.com/icons/papirus-team/papirus-apps/256/lucidchart-icon.png",
        "trello": "https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/trello-512.png",
        "relationship": "https://flyclipart.com/thumb2/relationship-icon-with-png-and-vector-format-for-free-unlimited-768804.png",
        "graph": "https://cdn2.iconfinder.com/data/icons/social-media-line/50/graph-512.png",
        "category": "https://cdn2.iconfinder.com/data/icons/shopping-e-commerce-4/100/SC-14-512.png",
        "commonlounge": "https://d1qb2nb5cznatu.cloudfront.net/startups/i/2529968-d8d3cb035697ed9bf0643bfc8f7406a1-medium_jpg.jpg?buster=1504069939",
        "searchin": "https://png.pngtree.com/png-vector/20190115/ourmid/pngtree-vector-search-icon-png-image_320926.jpg",
        "meetup": "https://www.shareicon.net/data/256x256/2015/09/25/106943_media_512x512.png",
        "tagboard": "https://cdn-images-1.medium.com/max/1200/1*Dn6hWx7acm7DwYJFnMDAhg.png",
        "crunchbase": "https://global-uploads.webflow.com/5726ee0d78d342c0529ee26c/594859000194a27e3600ae53_icon-crunchbase.svg",
        "crawler": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-QziCxVl05uOtXVFKmci8tbd_76EslXVwug&s",
        "disqus": "https://i2.wp.com/www.betterhostreview.com/wp-content/uploads/disqus.jpg",
        "stardev": "https://images.seeklogo.com/logo-png/43/2/star-channel-japan-logo-png_seeklogo-435513.png",
    }
