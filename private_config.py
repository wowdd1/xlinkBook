#!/usr/bin/env python
# -*- coding: utf-8-*- 

from config import Config
class PrivateConfig():


    processSourceDict = {':gamedev' : '>>unreal + >>gamework + >>gdc + >>xbox + >FromScratch + :graphics',\
                        ':gamedev2' : '>cry * unreal * unity * gamew + >>gdc + >graphics api + :dcc + >Cloud Game',\
                        ':gamedev3' : '>engine + >>sony + >forza + >studio',\
                        ':gamedev4' : '>engine + >GameWork + >Graphics api',\
                        ':weekly' : '>state of ai + >State of Graphics + >Shader',\
                        ':ai' : ':ml + :sdc + :robot + :nlp + :vision',\
                        ':data science' : ':ai + >>data science',\
                        ':ai people' : '=>MIT people + =>Stanford people + =>Berkeley people + =>CMU people',\
                        ':ai research' : '>NVIDIA Research + >Microsoft Research + >Facebook AI + =>Google Research + >MIT CSAIL + >Stanford AI + >Berkeley AI + >CMU AI',\
                        ':vision' : '=>cnn + =>vision + >vision',\
                        ':nlp' : '=>nlp + >nature language',\
                        ':robot' : '=>robot + =>slam + :sdc',\
                        ':sdc' : '>>carnd + ?alias:State of SDC + >Autonomous Vehicles + =>SDC',\
                        ':ml' : '>machine learning + =>machine learning + =>deep learning',\
                        ':graphics' : '>>siggraph + >>realtime rendering + =>image + :rendering-team + :rtx + >Johan Andersson + >Natalya Tatarchuk + >Yuriy O Donnell + >GameWork + >gpuopen + >intel graphics',\
                        ':rendering' : ':graphics',\
                        ':rtx' : '>>realtime ray tracing + >unity engine + >unreal engine + >cry engine + >frostbite engine',\
                        ':rendering-team' : '>ray tracing gems * Frostbite Rendering',\
                        ':tech' : ':os + :hardware + :chip + :gametech + >San Francisco + :weekly + :internet + :ai + :network',\
                        ':school' : '>MIT + >Stanford + >Berkeley + >CMU + >Harford + >College + >School + >University',\
                        ':degree' : '#AI degree + #game degree + #business degree + #NeuroScience Degree',\
                        ':game' : '>>gamer + =>game publisher',\
                        ':gametech' : '>>gamer + =>game publisher + :gamedev2 + :gameconf',\
                        ':internet' : '>google + >youtube + >facebook + >baidu + >Tencent + >Taobao + >twitter + >twitch + >reddit + >github + >Amazon + >Netflix + >Booking + :cloud',\
                        ':cloud' : '>>Cloud Native Computing Foundation',\
                        ':google' : '>google + =>Google Product + =>Google Company',\
                        ':microsoft' : '>microsoft + =>microsoft Product + =>Microsoft Company',\
                        ':network' : '=>5g + >Cisco',\
                        ':db' : '>Oracle + >Mysql + >DB',\
                        ':software' : '>microsoft + >IBM + >Android OS',\
                        ':os' : '=>Operating system',\
                        ':hardware' : '>apple + >hardware Review + >IBM + >Dell + >HP',\
                        ':chip' : '>nvidia + >intel + >amd + >ARM + >Qualcomm',\
                        ':dcc' : '>>maya',\
                        ':platform' : '>apollo * android i * game engine a',\
                        ':conf' : ':aiconf + :engconf + :gameconf + :brainconf',\
                        ':aiconf' : '=>ai conference',\
                        ':engconf' : '=>engineering conference',\
                        ':gameconf' : '=>gametech conference + =>game expo',\
                        ':brainconf' : '=>brain conference',\
                        ':vs' : '>>vs + ?Award',\
                        ':cool tech' : '=>Cool Tech'}

    
    processSearchCommandDict = {':social' : 'twitter: + facebook: + linkedin: + reddit: + zhihu: + z-zhihu: + weibo: + slack: + discord:',\
                                ':video' : 'youtube + youtube: + y-playlist: + y-channel: + y-video: + videolectures: + twitch: + mixer: + bilibili:',\
                                ':talk' : ':video + :ppt',\
                                ':project' : 'github: + github + sourcegraph: + bitbucket: + code + source + crx:',\
                                ':code' : ':project',\
                                ':news' : 'news + :blog + weekly  + 2019 + weixin + chuansong:',\
                                ':blog' : 'blogspot: + blog + zhihu: + z-zhihu: + medium: + medium',\
                                ':paper' : 'paper + gems + publication + reading + ppt: + goodread: + :year + :blog + refs',\
                                ':ppt' : 'ppt + presentation + links + slideshare: + slide + talk',\
                                ':reading' : ':blog + :paper + :ppt + book',\
                                ':company' : 'leadership + linkedin: + history + acquisition + merger + :product + job + report',\
                                ':product' : 'product + hardware + software + GPU + CPU + Chip + Service + Operating system',\
                                ':year' : '2019 + 2018 + 2017',\
                                ':now' : ':news + :social',\
                                ':nav' : 'searchin: + command: + alias: + keyword:',\
                                ':learn' : ':paper + :breakdown + :links + :blog + :video + Roadmap + learn + note',\
                                ':research' : ':learn',\
                                ':rtx' : 'rtx + dxr + tracing + ray',
                                ':intro' : 'introduction + tutorial + intro + sample + example + play with + Guide',\
                                ':links' : 'links + resource + awesome + guide + list',\
                                ':bigpic' : 'report + ecosystem + roadmap + trending',\
                                ':breakdown' : ':intro + :project + frame + architecture + 架构 + directory structure + data structure + algorithm + math model + process model + thread model + memery model + loop + pipeline + graph + flow + boot sequence + performance + optimization + spec'}
    

    processPostCommandDict = {':merger' : '',\
                              ':contentsearch' : '',\
                              ':innersearch' : '',\
                              ':append' : '',\
                              ':and' : '',\
                              ':andm' : '',\
                              ':engine' : '',\
                              ':preview' : '',\
                              ':deeper' : ''}
    # url keyword + args
    # resource type + args

    convert_command_dict = {':rtx' : 'rtx #or tracing #or trace #or dxr #or light #or ray #or optix #or denoise #or noise',\
                            ':graphics' : 'render #or graphics #or shade #or shading #or direct #or dx12 #or vulkan #or opengl',\
                            ':xr' : 'xr + vr + ar + Virtual Reality + Augmented Reality',\
                            ':ai' : 'deep learning #or machine learning #or learning #or AI #or artificial intelligence #or image + robot + vision + nature language',\
                            ':cloudgame' : 'cloud #or #or Streaming #or Stadia #or google #or xcloud #or SpatialOS #or 5g #or Virtualization',\
                            ':theory' : 'algorithm #or math #or theory + probability + statistics',\
                            ':conf' : 'gdc #or siggraph #or gtc #or CONFERENCE'}

    convert_source2engine_dict = {'-berkeley' : 'yt-berkeley',\
                                '-mit' : 'yt-ocw edx',\
                                '-stanford' : 'yt-stanfordeng yt-stanfordonline coursera',\
                                '-cmu' : 'yt-cmurobotics yt-cmucs',\
                                'cvpr' : 'yt-vision',\
                                'iccv' : 'yt-vision',\
                                'gdcvault' : 'gdcvault youtube yt-gdc'}

    convert_dict = {'example.com' : {'url_args' : '', 'page_step' : Config.convert_page_step, 'page_start' : Config.convert_page_start,\
                                 'page_max' : Config.convert_page_max, 'page_to_end' : Config.convert_page_to_end, 'tag' : 'a#title',\
                                 'min_num' : Config.convert_min_num, 'max_num' : Config.convert_max_num, 'filter' : Config.convert_filter,\
                                 'contain' : Config.convert_contain, 'start' : Config.convert_start, 'split_column_number' : Config.convert_split_column_number,\
                                 'output_data_to_new_tab' : Config.convert_output_data_to_new_tab, 'output_data_format' : Config.convert_output_data_format},\
                    'reddit' : {'tag' : 'a#title', 'next_page' : 'span#next-button'},
                    'quora' : {'script' : 'convert_quora.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'linkedin' : {'script' : 'convert_linkedin.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'zhuanlan' : {'script' : 'convert_zhihu.py', 'script_custom_ui' : False, 'split_column_number' : 50},
                    'www.zhihu' : {'script' : 'convert_zhihu.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    #'youtube' : {'script' : 'convert_youtube.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'youtube' : {'tag' : 'h3', 'lazyload' : 5},\
                    'medium' : {'script' : 'convert_medium.py', 'script_custom_ui' : False, 'split_column_number' : 12},
                    'thecvf' : {'tag' : 'dt#ptitle', 'split_column_number' : 40, 'cut_max_len' : 90},\
                    'syllabus' : {'tag' : 'a', 'contain' : '.pdf'},\
                    'research.fb' : {'url_args' : 'page/', 'url_args_2' : '', 'tag' : 'h3', 'page_max' : 10, 'split_column_number' : 55},\
                    'deepmind.com/research' : {'url_args' : '?page=', 'tag' : 'h1#h6', 'page_max' : 20, 'split_column_number' : 30, 'div_width_ratio' : 0, 'div_height_ratio' : 0},\
                    'deepmind.com/blog' : {'url_args' : '?page=', 'tag' : 'a#faux-link-block--link', 'page_start' : 1, 'page_step' : 1, 'page_max' : 10, 'min_num' : 4},\
                    'ai.google' : {'script' : 'convert_google_brain.py'},\
                    '/io20' : {'tag' : 'h4'},\
                    'googleblog' : {'next_page' : 'a#blog-pager-older-link', 'tag' : 'h2#title', 'contain' : 'googleblog'},\
                    'openai' : {'tag' : 'article#Research-Papers-paper', 'remove' : ['Blog', 'Code']},\
                    'microsoft' : {'url_args' : '&pg=', 'tag' : 'h3#card__heading', 'page_max' : 3, 'cut_max_len' : 80, 'split_column_number' : 50},\
                    'blogs.msdn' : {'url_args' : 'page/', 'tag' : 'h2#entry-title'},\
                    'devblogs.microsoft' : {'url_args' : '/page/', 'tag' : 'h5#entry-title'},\
                    'mlr.press' : {'script' : 'convert_mlr.py', 'script_custom_ui' : False, 'cut_max_len' : 90, 'split_column_number' : 105},\
                    'channel9' : {'next_page' : 'li#next', 'tag' : 'h3', 'url_is_base' : True},\
                    'wwdc' : {'tag' : 'a', 'contain' : '/wwdc20'},\
                    'andrewng' : {'tag' : 'h4#fig-title', 'cut_max_len' : 100, 'split_column_number' : 80},\
                    '~ang' : {'tag' : 'b', 'replace' : {'<br>': ''}, 'cut_max_len' : 110, 'split_column_number' : 78, 'filter' : 'Best paper'},\
                    'self-driving-car' : {'tag' : 'a#dhtgD', 'start' : 2, 'filter' : 'Slack Transcript'},\
                    'cvlibs' : {'tag' : 'div#paperdesc', 'url_is_base' : True, 'split_column_number' : 50, 'cut_max_len' : 95, 'cut_end' : '['},\
                    'aiweekly' : {'url_args' : '?page=', 'tag' : 'li#item', 'pass2' : True, 'tag_pass2' : 'h3', 'split_column_number' : 7, 'cut_max_len' : 300,  'page_start' : 1, 'page_step' : 1, 'page_max' : 1, 'replace' : {'Issue' : '', ',' : '<br>&nbsp;&nbsp;&nbsp;&nbsp;'}},\
                    'wildml' : {'tag' : 'h1', 'cut_end' : 'If you', 'remove' : ['The Wild Week in AI', '-', '–'], 'replace' : {';' :'<br>'}, 'start' : 3},\
                    'aidl' : {'url_args' : '?page=', 'tag' : 'li#item', 'page_max' : 7, 'split_column_number' : 20},\
                    'deeplearningweekly' : {'tag' : 'a', 'pass2' : True, 'tag_pass2' : 'span#item-link-title', 'cotain' : 'Weekly', 'cut_start' : '#', 'replace' : {',' : '<br>'}, 'split_column_number' : 40},\
                    'paperreading' : {'next_page' : 'a#next', 'url_is_base' : True, 'tag' : 'a#post-link', 'page_max' : 6},\
                    'syncedreview' : {'next_page' : 'a#next', 'tag' : 'h2#entry-title', 'page_max' : 3, 'split_column_number' : 80, 'cut_max_len' : 90},\
                    'pixar' : {'tag' : 'b', 'url_is_base' : True},\
                    'disneyanimation' : {'tag' : 'h3'},\
                    'disneyresearch' : {'url_args' : 'page/', 'tag' : 'h2#post-title', 'page_start' : 1, 'page_step' : 1, 'page_max' : 20, 'split_column_number' : 40, 'cut_max_len' : 60},\
                    'graphics.stanford' : {'tag' : 'dt', 'split_column_number' : 165, 'cut_max_len' : 90},\
                    Config.ip_adress :  {'script_custom_ui' : False, 'split_column_number' : 40, 'cut_max_len' : 60, 'div_width_ratio' : 7.6, 'div_height_ratio' : 33.8, 'show_url_icon' : False},\
                    'realtimerendering' : {'script' : 'convert_realtimerendering.py', 'output_data_to_temp' : True, 'script_custom_ui' : False, 'split_column_number' : 40, 'cut_max_len' : 60, 'div_width_ratio' : 7.6, 'div_height_ratio' : 30.5, 'show_url_icon' : False, 'stat_field' : ['url']},\
                    'jendrikillner' : {'url_args' : 'page/', 'tag' : 'h2', 'tag_pass2' : 'h2', 'pass2' : True, 'page_start' : 1, 'page_step' : 1, 'page_max' : 1, 'no_url_args_4_1st_page' : True},\
                    'blogspot' : {'tag' : 'h3#post-title', 'next_page' : 'a#blog-pager-older-link', 'page_max' : 10, 'split_column_number' : 30, 'cut_max_len' : 80},\
                    'research.nvidia' : {'tag' : 'span#field-content', 'split_column_number' : 110, 'cut_max_len' : 100, 'div_width_ratio' : 7.6, 'div_height_ratio' : 33},\
                    'nvidianews' : {'url_args' : '&page=', 'tag' : 'h3', 'page_max' : 10, 'cut_max_len' : 95, 'split_column_number' : 50},\
                    'devblogs.nvidia' : {'url_args' : 'page/', 'tag' : 'div#home-posts-title', 'page_max' : 3},\
                    'news.developer.nvidia' : {'url_args' : '/page/', 'tag' : 'h1#entry-title', 'replace' : {'Permalink to' : ''}},\
                    'matt/' : {'tag' : 'a#post-link'},\
                    'ingowald' : {'url_args' : 'page/', 'tag' : 'h1#entry-title'},\
                    '~wald' : {'tag' : 'a', 'contain' : 'pdf'},\
                    'realitylab' : {'tag' : 'strong'},\
                    'chillee' : {'tag' : 'td#title'},\
                    'unrealengine' : {'tag' : 'h3#title', 'split_column_number' : 50, },\
                    'seed' : {'script' : 'convert_seed.py'},\
                    'frostbite/news' : {'tag' : 'h3', 'split_column_number' : 20, 'remove' : ['- Frostbite', '- Frostbit…']},\
                    'cryengine' : {'next_page' : 'li#pager-next', 'tag' : 'h2', 'url_is_base' : True, 'split_column_number' : 30, 'min_num' : 3, 'page_max' : 8},\
                    'colinbarrebrisebois' : {'url_args' : '/page/', 'tag' : 'h1#entry-title'},\
                    'guerrilla-games' : {'tag' : 'h3#box-simple__title', 'split_column_number' : 20, 'smart_engine' : 'google*pdf'},\
                    'gameenginebook' : {'tag' : 'a', 'split_column_number' : 40, 'domain_stat_field' : ['url']},\
                    'valvesoftware' : {'tag' : 'li', 'contain' : '"', 'cut_start' : '"', 'cut_end' : '."', 'split_column_number' : 21},\
                    'gpuopen' : {'tag' : 'h6#post-title', 'smart_engine' : 'gpuopen', 'split_column_number' : 55, 'cut_max_len' : 90},\
                    'gamasutra' : {'url_args' : '?page=', 'tag' : 'span#story_title', 'page_max' : 10},\
                    '.bib' : {'script' : 'convert_bibliographies.py', 'script_custom_ui' : False, 'split_column_number' : 100, 'cut_max_len' : 65, 'smart_engine' : 'scholar'},\
                    'wordpress' : {'url_args' : '/page/', 'tag' : 'h2', 'page_max' : 21, 'min_num' : 3, 'remove' : ['Permanent Link to '], 'split_column_number' : 20},\
                    'umbra3d' : {'url_args' : '/page/', 'tag' : 'h2', 'page_max' : 4},\
                    'eurogamer' : {'url_args' : '/?start=', 'tag' : 'p#title', 'page_start' : 0, 'page_step' : 30, 'page_max' : 30, 'replace' : {'Digital Foundry' : '', ': Hands' : 'Hands'}, 'split_column_number' : 60},\
                    'gameanim' : {'script' : 'convert_gameanim.py', 'script_custom_ui' : False, 'split_column_number' : 40, 'cut_max_len' : 60},
                    'oculus' : {'url_args' : '?page=', 'tag' : 'div#_1f17'},\
                    'slideshare' : {'url_args' : '/', 'tag' : 'strong', 'split_column_number' : 20, 'cut_max_len' : 60, 'min_num' : 2, 'filter' : 'course'},\
                    'collection' : {'url_args' : '?page=', 'tag' : 'h2#zm-item-title', 'page_start' : 1, 'page_step' : 1, 'page_max' : 21},\
                    'csdn' : {'url_args' : '/article/list/', 'filter' : '帝都的凛冬', 'contain' : 'article', 'tag' : 'h4', 'page_max' : 11, 'remove' : ['原 ']},\
                    #media  s: ppt a: audio v: video
                    #'cut_end' : ' by ',
                    'fuchsia-china' : {'url_args' : '/page/', 'tag' : 'h2#post-title'},\
                    'gdcvault' : {'url_args_2' : '&media=vs', 'smart_engine' : 'gdcvault', 'tag' : 'a#session_item', 'cut_start' : '20', 'cut_start_offset' : 2, 'cut_to_desc' : ' by ', 'remove' : ['(Presented', '(Prese', '"', "'"] , 'split_column_number' : 40, 'cut_max_len' : 1000},\
                    'nips' : {'tag' : 'li', 'min_num' : 15, 'split_column_number' : 100, 'cut_end' : ',', 'cut_max_len' : 80},\
                    'twitter' : {'script' : 'convert_twitter.py', 'script_custom_ui' : False, 'split_column_number' : 12},\
                    'employbl' : {'script' : 'convert_employbl.py', 'script_custom_ui' : False, 'split_column_number' : 71},\
                    'igdb' : {'script' : 'convert_igdb.py', 'script_custom_ui' : True, 'split_column_number' : 12},\
                    'gamefromscratch' : {'url_args' : '?page=', 'tag' : 'a#posttitlelink', 'page_start' : 1, 'page_step' : 1, 'page_max' : 10},\
                    'uwa4d' : {'url_args' : 'page/', 'tag' : 'h2#post-title', 'page_start' : 1, 'page_step' : 1, 'page_max' : 30, 'page_to_end' : True, 'contain' : '虚幻', 'split_column_number' : 40 },\
                    'feed' : {'script' : 'convert_rss.py', 'script_custom_ui' : False},\
                    'douban' : {'url_args' : '?start=', 'tag' : 'div#title', 'page_start' : 0, 'page_step' : 25, 'page_max' : 50},\
                    'ccf' : {'tag' : "li"},\
                    'dlab' : {'tag' : 'strong'},\
                    'zlab' : {'tag' : 'a', 'min_num' : 3},\
                    'wharton' : {'tag' : 'h4'},\
                    'similarsites' : {'script' : 'convert_similarsites.py'},\
                    'selfshadow' : {'tag' : 'div#entry-content->a', 'split_column_number' : 30, 'domain_stat_field' : ['url']},\
                    'gfx-hub' : {'url_args' : '/page/', 'tag' : 'h2', 'page_start' : 1, 'page_step' : 1, 'page_max' : 13},\
                    'weixin' : {'script' : 'convert_weixin.py', 'split_column_number' : 40, 'confirm_argv' : True, 'page_max' : 4},\
                    'chuansong' : {'script' : 'convert_chuansong.py', 'split_column_number' : 40},\
                    'china-pub' : {'url_args' : '&page=', 'tag' : 'li#result_name', 'page_max' : 10, 'split_column_number' : 40},\
                    '%5BPDF%5D' : {'url_args' : '&start=', 'tag' : 'h3#r', 'page_start' : 0, 'page_step' : 10, 'page_max' : 50, 'contain' : '.pdf'},\
                    'gputechconf' : {'script' : 'convert_gtc.py', 'split_column_number' : 40, 'smart_engine' : 'gtc', 'cut_max_len' : 73},\
                    'oschina' : {'url_args' : '&type=ajax&p=', 'tag' : 'h3#header', 'page_to_end' : False, 'page_max' : 10},\
                    'github.com' : {'script' : 'convert_github.py', 'script_custom_ui' : False, 'split_column_number' : 12, 'cut_max_len' : 85}}


    innerSearchDict = {'y-channel:' : 'https://www.youtube.com/channel/%s/search?query=%w',\
                       'youtube:' : 'https://www.youtube.com/%s/search?query=%w',\
                       'github:' : 'https://github.com/%s/search?q=%w',\
                       ':blog' : 'blog + news'}