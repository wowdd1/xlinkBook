var args = [];
var search_box;
var global_selection = '';
var extension_count_dict = [];
var pop_width = 1444;
var pop_height = 900;


$(function() {  
    
    $("[data-toggle='popover']").popover({  
        html : true,    
        title: title(), 
        container: 'body',
        delay:{show:500, hide:1000},  
        content: function() {  
          return content(this.textContent, $(this).data('popover-content'));    
        }   
    });  
}); 

window.document.onkeydown = onkeydown;
window.document.onkeyup = onkeyup;

var KEY_C_DOWN = false;
var KEY_X_DOWN = false;
var KEY_E_DOWN = false;
var KEY_Q_DOWN = false;
var KEY_G_DOWN = false;
var KEY_S_DOWN = false;
var KEY_D_DOWN = false;
var KEY_V_DOWN = false;
var KEY_P_DOWN = false;

var KEY_SHIFT_DOWN = false;
var KEY_ESC_DOWN = false;
var KEY_TAB_DOWN = false;


var hover_mode = true;

var lastClick = null;
var clickArray = new Array();
var KEY_L_ALT = 18;
var KEY_L_CTRL = 17;
var KEY_V_CODE = 86;
var KEY_P_CODE = 80;
var KEY_C_CODE = 67;
var KEY_D_CODE = 68;
var KEY_X_CODE = 88;
var KEY_ESC_CODE = 27;
var KEY_E_CODE = 69;
var KEY_Q_CODE = 81;
var KEY_G_CODE = 71;
var KEY_H_CODE = 72;
var KEY_S_CODE = 83;
var KEY_ENTER_CODE = 13;
var KEY_SHIFT_CODE = 16;
var KEY_COMMAND_CODE = 91;




var KEY_TAB_CODE = 9;

var KEY_192_CODE = 192;
var KEY_187_CODE = 187;
var KEY_189_CODE = 189;
var KEY_0_CODE = 48;
var KEY_1_CODE = 49;
var KEY_2_CODE = 50;
var KEY_3_CODE = 51;
var KEY_4_CODE = 52;
var KEY_5_CODE = 53;
var KEY_6_CODE = 54;
var KEY_7_CODE = 55;
var KEY_8_CODE = 56;
var KEY_9_CODE = 57;



function searchTextChanage() {
    search_box = document.getElementById('search_txt');
    console.log('searchTextChanage', search_box.value);

    search_box_text_div = document.getElementById('searchBoxTextDiv')

    //search_box_text_div.innerHTML = search_box.value;
}

function doPreview(baseUrl, searchText, popup) {
    var url = '';
    if (searchText.indexOf('*') != -1) {
        url = baseUrl.replace('%s', '[' + searchText + ']');
    } else {
        //url = baseUrl.replace('%s', searchText);
        url = baseUrl.split('%s').join(searchText);
    }
    
    if (textArray.length > 0) {
        urlArray = new Array();
        for (var i = 0; i < textArray.length; i++) {
            if (textArray[i].indexOf(' - ') > 0) {
                textArray[i] = textArray[i].substring(textArray[i].indexOf(' - ') + 3);
            }
            if (textArray[i].indexOf('(') > 0) {
                textArray[i] = textArray[i].substring(0, textArray[i].indexOf('(')).replace('-', ' ').replace('  ', ' ');
            }
            if (textArray[i].indexOf('>') >= 0) {
                textArray[i] = textArray[i].substring(textArray[i].indexOf('>') + 1);
            }
            if (textArray[i].indexOf('!') > 0) {
                textArray[i] = textArray[i].substring(textArray[i].indexOf('!') + 1);
            }
            urlArray.push(baseUrl.replace('%s', textArray[i]));
           
        }
    }
    if (popup == true) {
        window.scroll(0, 20);
        onHoverPreview('', searchText, url, 'searchbox', true);    
    } else {
        urlArray.push(url);
        for (var i = 0; i < urlArray.length; i++) {
           window.open(urlArray[i]); 
        }
        textArray = new Array();
        urlArray = new Array();
        
    }
}

var tab_down_count = 0;
function onkeydown(evt){
    console.log('ss', "onkeydown " + evt.keyCode.toString());

    evt = (evt) ? evt : window.event
    if (evt.keyCode) {
       if (evt.keyCode == KEY_X_CODE){
            KEY_X_DOWN = true;

            hiddenPopup();

       } else if (evt.keyCode == KEY_C_CODE) {
            KEY_C_DOWN = true;
       } else if (evt.keyCode == KEY_E_CODE) {
           KEY_E_DOWN = true;

       } else if (evt.keyCode == KEY_Q_CODE) {
           KEY_Q_DOWN = true;
       } else if (evt.keyCode == KEY_G_CODE) {
           KEY_G_DOWN = true;
       } else if (evt.keyCode == KEY_D_CODE) {
           KEY_D_DOWN = true;
           /*
           if (startPointX != 0) {
              endPointX = pageX;
              endPointY = pageY;    
              drawLine(startPointX, startPointY, endPointX, endPointY);
              endPointX = 0;
              endPointY = 0;
              startPointX = 0;
              startPointY = 0;
           } else {
              startPointX = pageX;
              startPointY = pageY;
           }*/

       } else if (evt.keyCode == KEY_S_CODE) {
           KEY_S_DOWN = true;    
       } else if (evt.keyCode == KEY_P_CODE) {
           KEY_P_DOWN = true;
       } else if (evt.keyCode == KEY_V_CODE) {
           if (isEditing == false) {
               KEY_V_DOWN = true;
               hover_mode = true;
               if (lastHoveredUrl != '') {
                   if (lastHoveredUrl.substring(0, 4) != 'http') {
                      window.scroll(0, 20);
                      showPopupContent(0, 20, pop_width, pop_height, lastHoveredUrl); 
                   } else {
                      window.scroll(0, 20);
                      onHoverPreview(lastHoveredID, lastHoveredText, lastHoveredUrl, 'searchbox', KEY_V_DOWN);
                   }
               }            
           } else {
               console.log('isEditing');
           }
       } else if ((evt.keyCode > 47 && evt.keyCode < 58) || evt.keyCode == KEY_192_CODE || evt.keyCode == KEY_187_CODE || evt.keyCode == KEY_189_CODE && lastHoveredText != '') {
           if (isEditing == false && lastHoveredText != '') {
               var searchText = lastHoveredText;
               var popup = true;
               var baseUrl = '';
               if (searchText.indexOf(' - ') > 0) {
                   searchText = searchText.substring(searchText.indexOf(' - ') + 3);
               }
               if (searchText.indexOf('(') > 0) {
                   searchText = searchText.substring(0, searchText.indexOf('(')).replace('-', ' ').replace('  ', ' ');
               }

               if (searchText.indexOf('>') >= 0) {
                   searchText = searchText.substring(searchText.indexOf('>') + 1);
               }
               if (searchText.indexOf('!') > 0) {
                   searchText = searchText.substring(searchText.indexOf('!') + 1);
               }
               if (evt.keyCode == KEY_0_CODE || evt.keyCode == KEY_192_CODE) {
                   //baseUrl = 'https://wikipedia.org/wiki/%s';
                   var name = '';
                   if (evt.keyCode == KEY_0_CODE) {
                       name = prompt("please input the search engine", lastHoveredCMD);
                   } else {
                       name = 'd:star';
                       if (isPopupShowing()){
                           hiddenPopup();
                           return;
                       }
                   }

                   if (name == 'all') {
                       baseUrl = 'https://www.google.com/search?q=%s*http://www.baidu.com/s?word=%s*https://www.youtube.com/results?search_query=%s*http://s.weibo.com/weibo/%s*https://www.toutiao.com/search/?keyword=%s*https://www.zhihu.com/search?type=question&q=%s*https://www.google.com/search?q=%s*https://www.google.com/search?q=%s*http://gen.lib.rus.ec/search.php?phrase=1&view=simple&column=def&sort=year&sortmode=DESC&req=%s';
                       doPreview(baseUrl, searchText, true);                     
                       return;
                   }


                   if (name.indexOf('%') != -1) {
                       //typeKeyword(name.replace('%', searchText.split('*').join(' + >')));
                       showPopupContent(0, 20, pop_width, pop_height, name.replace('%', searchText.split('*').join(' + >')));
                       window.scroll(0, 20);
                       return;
                   } else if (name.indexOf('>') != -1) {
                       //typeKeyword(name);
                       showPopupContent(0, 20, pop_width, pop_height, name);
                       window.scroll(0, 20);                      
                       return;
                   } else if (name.indexOf('/') != -1) {
                       //typeKeyword('>' + searchText.split('*').join(' + >') + name);
                       showPopupContent(0, 20, pop_width, pop_height, '>' + searchText.split('*').join(' + >') + name);
                       window.scroll(0, 20);                       
                       return;
                   }
                   
                   $.post('/getEngineUrl', {'engineName' : name, 'searchText' : searchText}, function(result) {
                       if (result != '') {
                           
                           if (result.indexOf('</a>') > 0) {
                               baseText = result;
                               showPopup(pageX, pageY, 340, 100);
                           } else if (result.indexOf('*') > 0) {
                               urls = result.split('*');
                               for (var i = 0; i < urls.length; i++) {
                                   doPreview(urls[i], searchText, false);
                               }
                           } else {
                               baseUrl = result;
                               doPreview(baseUrl, searchText, popup);
                           }
                           
                           
                           return;
                       } 
                   }); 

               } else if (evt.keyCode == KEY_1_CODE) {
                   baseUrl = 'https://www.google.com/search?q=%s';
               } else if (evt.keyCode == KEY_2_CODE) {
                   baseUrl = 'http://www.baidu.com/s?word=%s';
               } else if (evt.keyCode == KEY_3_CODE) {
                   popup = false;
                   baseUrl = 'https://twitter.com/search?src=typd&q=%s';
               } else if (evt.keyCode == KEY_4_CODE) {
                   baseUrl = 'https://www.youtube.com/results?search_query=%s';
               } else if (evt.keyCode == KEY_5_CODE) {
                   baseUrl = 'http://s.weibo.com/weibo/%s';
               } else if (evt.keyCode == KEY_6_CODE) {
                   popup = false;
                   baseUrl = 'https://github.com/search?q=%s';
               } else if (evt.keyCode == KEY_7_CODE) {
                   baseUrl = 'https://www.zhihu.com/search?type=question&q=%s';
               } else if (evt.keyCode == KEY_8_CODE) {
                   baseUrl = 'http://gen.lib.rus.ec/search.php?phrase=1&view=simple&column=def&sort=year&sortmode=DESC&req=%s';
               } else if (evt.keyCode == KEY_9_CODE) {
                   baseUrl = 'https://www.google.com/search?newwindow=1&source=hp&q=%s&btnI=I';
                   //baseUrl = 'http://www.similarsites.com/site/%s';
               } else if (evt.keyCode == KEY_187_CODE) {
                   typeKeyword('??' + searchText);
                   return;
               } else if (evt.keyCode == KEY_189_CODE) {
                   typeKeyword('?=>' + searchText + '/:/:group-short ' + searchText);
                   return;
               }

               if (baseUrl != '') {
                   if (searchText.indexOf('*') != -1) {
                        baseUrl = baseUrl.replace('%s', '[' + searchText + ']');
                   }
                   console.log('baseUrl', baseUrl);
                   doPreview(baseUrl, searchText, popup);
               }
               
           }
       } else if(evt.keyCode == KEY_L_ALT){
            console.log('ss', "onkeydown 18");

            if (clickArray.length > 0) {
                var obj = clickArray[clickArray.length - 1]
                clickArray.splice(clickArray.length - 1, 1);

                if (obj.text == 'less') {
                    obj.click();
                } else {
                    for (var i = clickArray.length - 1; i <= 0; i--) {
                        var obj = clickArray[i];
                        clickArray.splice(i, 1);

                        if (obj.text == 'less') {
                            obj.click();
                            break;
                        }

                    }

                }

            }
       } else if (evt.keyCode == KEY_L_CTRL) {
            if (lastClick != null) {
                lastClick.click();
            }
       } else if (evt.keyCode == KEY_ESC_CODE) {
            KEY_ESC_DOWN = true;
            resetState();
            hiddenPopup();
       } else if (evt.keyCode == KEY_TAB_CODE) {
            KEY_TAB_DOWN = true;
            tab_down_count++;
            startTyping();           
       } else if (evt.keyCode == KEY_H_CODE) {
            hover_mode  = !hover_mode;

            console.log('hover_mode ' + hover_mode);
       } else if (evt.keyCode == KEY_ENTER_CODE) {
            var a = document.getElementById('searchbox-a');
            var textbox = document.getElementById('search_txt');
            if (a.text == '...' && textbox.value != '') {
                a.onclick();
            }
       } else if (evt.keyCode == KEY_SHIFT_CODE) {
            KEY_SHIFT_DOWN = true;

       }


       if (KEY_TAB_DOWN && evt.keyCode >= 49 && evt.keyCode <= 60) {
           typePattern(evt.keyCode);
       } 
    }
}

function normalColor(obj, color) {
    obj.style.background = color; 
}

function hoverColor(obj, color) {
    obj.style.background = color; 

}

function normal(obj) {
    obj.style.background = 'white'; 
}

function hover(obj) {
    obj.style.background = '#F8F8FF'; 

}

function resetState() {
    console.log('resetState()');
    hover_mode = true;
    KEY_Q_DOWN = false;
    KEY_E_DOWN = false;
    KEY_P_DOWN = false;
    KEY_SHIFT_DOWN = false;
    KEY_TAB_DOWN = false;
    popupMode = false;
    urlArray = new Array(); 
    textArray = new Array();

    resetHoverState();
}

function setCaretPosition(ctrl, pos) {
  // Modern browsers
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    ctrl.setSelectionRange(pos, pos);
  
  // IE8 and below
  } else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveEnd('character', pos);
    range.moveStart('character', pos);
    range.select();
  }
}

function startTyping() {

    lastHoveredUrl = '';
    lastHoveredText = '';
  
    search_a = document.getElementById('searchbox-a');
    search_box = document.getElementById('search_txt');
    search_btn = document.getElementById('search_btn');


    if (search_a.text == 'less') {
        search_a.click();
    }


    if (tab_down_count > 1) {
        if (tab_down_count == 5) {
           search_box.value = '->';
        } else if (tab_down_count == 2) {
           search_box.value = '>:';
        }  else {
            tab_str = '';
            for (var i = 0; i < tab_down_count - 1; i++) {
                tab_str = '>' + tab_str;
            }
            search_box.value = tab_str;         
        }

    } else {
        search_box.value = '>';
    }
    
    search_btn.focus();
    //search_a.focus();
    lastHoveredUrl = '';

    setTimeout(function () {
        search_box.focus();
    }, 50); 
}

var parentCmdOfTypeKeyword = ''


function typeKeywordEx(keyword, parentCmd, refresh, parentDivID) {

    if (keyword.indexOf('^') != -1) {
        keyword = keyword.split('^').join('"');
    }
    
    if (refresh) {
        typeKeyword(keyword, parentCmd);
    } else {
        var paddingLeft = 20;

        $.post('getPluginInfo', {'title' : keyword, 'url' : '', style : 'padding-left:' + paddingLeft + 'px; padding-top: 10px;', 'parentCmd' : parentCmd, parentDivID : parentDivID}, function(result){
    
            if (result != '') {
                //console.log(parentDivID);
                //$('#' + parentDivID).append('xxxx');
                $('#' + parentDivID).append(result);
            } 
        });       
    
    }
}

function typeKeyword(keyword, parentCmd) {
    if (keyword.indexOf('^') != -1) {
        keyword = keyword.split('^').join('"');
    }
    console.log('ss', "typeKeyword");
    resetHoverState();
    if (parentCmd == '') {
        search_box = document.getElementById('search_txt');
        txt = search_box.value;
        if (txt != '' && txt != keyword) {
            parentCmd = txt;
        }
    }

    if (KEY_SHIFT_DOWN) {
        textArray.push(keyword);
        return;
    }

    if (KEY_E_DOWN) {
        KEY_E_DOWN = false;
        window.open('http://localhost:5000/library?search_keyword=' + keyword);

        return;
    }

    if (KEY_P_DOWN || popupMode) {
        KEY_P_DOWN = false;
        showPopupContent(0, 20, pop_width, pop_height, keyword);
        window.scroll(0, 20);
        return;
    }

    if (KEY_S_DOWN) {
        keyword = keyword.substring(keyword.indexOf('>') + 1)
        if (keyword.indexOf('group-short') > 0) {
            keyword = keyword.substring(keyword.indexOf('group-short') + 12)
        }
        baseText = genEnginHtml('', keyword, '', '');
        showPopup(pageX, pageY, 340, 100);
        popupMode = false;
        return;
    }
    //startTyping();
    parentCmdOfTypeKeyword = parentCmd;
    search_a = document.getElementById('searchbox-a');
    search_box = document.getElementById('search_txt');

    if (search_a.text == 'less') {
        search_a.click();
    }

    setTimeout(function () {
        if (search_a.text == '...') {
            search_box.value = keyword;
            search_a.click();
        }
    }, 500); 
    
}


function typePattern(keycode) {
    search_box = document.getElementById('search_txt');  
    search_btn = document.getElementById('search_btn');
    if (keycode == KEY_1_CODE) {
        search_box.value = '?';
    } else if (keycode == KEY_2_CODE) {
        search_box.value = '!';
    } else if (keycode == KEY_3_CODE) { 
        search_box.value = '>^*/>/>';
    } else if (keycode == KEY_4_CODE) { 
        search_box.value = '>^+/>/>';
    } else if (keycode == KEY_5_CODE) {
        search_box.value = '?$+/>/>';
    } else if (keycode == KEY_6_CODE) {
        search_box.value = ':# of # from # and #';
    }


    search_btn.focus();

    setTimeout(function () {
        search_box.focus();
    }, 50); 
}

function editSearchinField(rID, rTitle, url, title, searchinFieldTitle, resourceType, library, searchinFieldText) {
    resetState();
    js = ''
    js += "var text = $('#custom-plugin-" + rID + "-textarea');"
    js += "var postArgs = {'rID' : '" + rID + "', 'rTitle' : '" + rTitle + "', 'url' : '" + url + "', 'title' : '" + title + "', 'searchinFieldTitle' : '" + searchinFieldTitle + "', 'resourceType' : '" + resourceType + "', 'library' : '" + library + "', 'editText' : text[0].value};"
    js += "var searchinFieldText = '" + searchinFieldTitle + "' + '()';\
      if (text[0].value == searchinFieldText){\
          console.log('searchinFieldText no chanaged');\
          hiddenPopup();\
          return;\
      }"    
    js += "$.post('/editSearchinField', postArgs, function(data) { \
      console.log(data);\
      var postArgs = {name : 'edit', rID : '" + rID + "', rTitle : '" + rTitle + "',  check : 'false', fileName : '" + 'db/library/' + library+ "', divID : 'div-plugin-android-os-1-1-edit', originFileName : '" + 'db/library/' + library+ "', textContent : data};\
      console.log(postArgs);\
      $.post('/extensions', postArgs, function(data) { hiddenPopup(); });\
    })"
      //$.post('/extensions', postArgs, function(data) { hiddenPopup(); });\
  
    if (searchinFieldText == '') {
      searchinFieldText = searchinFieldTitle + '()';
    }
    baseText = "Edit Searchin Field:<br><textarea rows='15' cols='40' id='custom-plugin-" + rID + "-textarea' style='font-size: 13px; border-radius: 5px; font-family: &quot;San Francisco&quot;; color: rgb(0, 51, 153); white-space: pre-wrap; background: white;'>" + searchinFieldText + "</textarea>";
    baseText += '<br>'
    if (searchinFieldText.indexOf('please edit') == -1) {
        baseText += '<button type="submit" id="edit_btn" hidefocus="true" onclick="' + js + '">submit</button>'
    } else {
        typejs = "showPopupContent(0, 20, pop_width, pop_height, '>" + searchinFieldTitle + "');"
        baseText += '<a href="javascript:void(0);" onclick="' + typejs + '">Click and Edit "' + searchinFieldTitle + '" Here!!!</a>'
    }
    showPopup(pageX, pageY, 340, 300);  
}

function editSearchinLink(rID, title, searchinFieldTitle, searchinPart1, searchinPart2, searchinPart3, descPart, library) {
    console.log('searchinPart1', searchinPart1);
    console.log('searchinPart2', searchinPart2);
    console.log('searchinPart3', searchinPart3);

    resetState();
    js = "var searchinPart1='" + searchinPart1 + "';"
    js += "var text = $('#custom-plugin-" + rID + "-textarea');"
    js += "var searchinPart2 = text[0].value;"
    js += " if (searchinPart2 == '') { searchinPart2 = '" + searchinFieldTitle + "';}"
    js += "var searchinFieldTitle = '" + searchinFieldTitle + "' + '<>';"
    js += " if (searchinPart2 == searchinFieldTitle) { console.log('searchinlink no chanaged');hiddenPopup(); return;}"
    js += "var searchinPart3='" + searchinPart3 + "';"
    js += 'var searchin = searchinPart1 + searchinPart2 + searchinPart3;'
    js += "searchin = searchin.split(', ').join('*');"
    js += "var desc = '" + descPart + ",\\nsearchin(' + searchin + ')';"
    js += "desc = desc.split('newline').join('\\n');"
    js += 'console.log(desc);'
    pluginID = 'custom-plugin-' + rID
    js += "var postArgs = {name : 'edit', rID : '" + pluginID + "', rTitle : '" + title + "', check: 'false', fileName : 'db/library/" + library + "', divID : 'div-plugin-android-os-1-1-edit', originFileName : 'db/library/" + library + "', textContent: desc};"
    js += "$.post('/extensions', postArgs, function(data) {   a = document.getElementById('searchbox-a');   if (a.text == 'less'){ a.onclick(); a.onclick(); }  });"
                        

    baseText = "Edit Searchin Link:<br><textarea rows='15' cols='40' id='custom-plugin-" + rID + "-textarea' style='font-size: 13px; border-radius: 5px; font-family: &quot;San Francisco&quot;; color: rgb(0, 51, 153); white-space: pre-wrap; background: white;'>" + searchinPart2 + "</textarea>";
    baseText += '<br>'
    baseText += '<button type="submit" id="edit_btn" hidefocus="true" onclick="' + js + '">submit</button>'
    showPopup(pageX, pageY, 340, 300);  
}

function onkeyup(evt){
    evt = (evt) ? evt : window.event
    if (evt.keyCode) {
       if(evt.keyCode == KEY_X_CODE){
            console.log('ss', "onkeyup 88");
            KEY_X_DOWN = false;
       } else if (evt.keyCode == KEY_C_DOWN) {
            //KEY_C_DOWN = false;
       } else if (evt.keyCode == KEY_E_CODE) {
            console.log('ss', "onkeyup 69");
            KEY_E_DOWN = false;

       } else if (evt.keyCode == KEY_Q_CODE) {
            KEY_Q_DOWN = false;
       } else if (evt.keyCode == KEY_G_CODE) {
            KEY_G_DOWN = false;
       } else if (evt.keyCode == KEY_S_CODE) {
            KEY_S_DOWN = false;
       } else if (evt.keyCode == KEY_D_CODE) {
            KEY_D_DOWN = false;
       } else if (evt.keyCode == KEY_P_CODE) {
            KEY_P_DOWN = false;
       } else if (evt.keyCode == KEY_V_CODE) {
            KEY_V_DOWN = false;
       } else if (evt.keyCode == KEY_SHIFT_CODE) {
            KEY_SHIFT_DOWN = false;

       } else if (evt.keyCode == KEY_ESC_CODE) {
            KEY_ESC_DOWN = false;
       } else if (evt.keyCode == KEY_TAB_CODE) {
            KEY_TAB_DOWN = false;
            if (tab_down_count > 0) {
                setTimeout(function () {
                    tab_down_count = 0;
                }, 700);              
            }

       }
    }
}


 
function title() {
    return $("[data-toggle='popover']").text;  

}  

 
function content(text, data) {  
    console.log('', data);
    var content_id = "content-id-" + $.now();
    split_data = null;
    rid = '';
    resourceType = '';
    aid = '';
    refreshID = ''
    isTag = false;
    originText = text
    result = content2(content_id, dialog_engin_count, dialog_command_count);

    if (data.indexOf('#') > 0) {
        split_data = data.split('#');
        rid = split_data[0];
        resourceType = split_data[1];
        refreshID = split_data[2];
        aid = refreshID.replace('td-', 'a-')
        if (split_data[3] == 'True') {
            isTag = true;
        }
        originText = split_data[4];
    }
    
    dialog_args = {type : 'dialog', rID : rid, searchText: text, originText : originText, resourceType : resourceType, fileName : fileName, library : library, aid : aid, refreshID : refreshID, enginArgs : engin_args, isTag : isTag, windowHref : window.location.href};
    $.post('/queryUrl', dialog_args, function(data) {
        if (data.indexOf('#') > 0 && data.substring(0, data.indexOf('#')).indexOf('color:') < 0) {
            engin_count = parseInt(data.substring(0, data.indexOf('#')));
            data = data.substring(data.indexOf('#') + 1);
            console.log('', aid);
        }
        $('#' + content_id).html(data);
    });

    return result;
}  

function content2(content_id, dialog_engin_count, dialog_command_count) {
    result = '<div id="' + content_id + '">'
    /*
    for (var i = 0; i < dialog_engin_count - 1; i++) {
        result += 'nbsp;';
        if (i % 5 == 0 && i > 0) {
           result += 'nbsp;<br>' ;
        }
    }
    if (dialog_engin_count > 5) {
        //result +='<br>';
    }
        for (var i = 0; i < dialog_command_count; i++) {
        result += '<br>' ;
    }
    
    result += 'Loading...</div>';
    console.log('',result);
    */
    result += 'nbsp;nbsp;nbsp;nbsp;nbsp;nbsp;nbsp;';
    return result;
}


var pageX = 0;
var pageY = 0;
function mousemoveHandler(e) {
    e = e || window.event;

    pageX = e.pageX;
    pageY = e.pageY;

    // IE 8
    if (pageX === undefined) {
        pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }


    //console.log(pageX, pageY);
}

$(document).ready(function(){

  document.addEventListener('mousemove', mousemoveHandler);

  search_box = document.getElementById('search_txt');

  url = window.location.href;

  if (url.indexOf('/search?q=') != -1) {
      query = url.substring(url.indexOf('?q=') + 3);
      search_box.value = query.replace('%20', ' ');  

      a = document.getElementById('searchbox-a');
      a.click();
  }

  if (url.indexOf('search_keyword=') != -1) {
      keyword = url.substring(url.indexOf('keyword=') + 8);
      keyword = keyword.replace('%3E', '>');
      keyword = keyword.replace('%20', ' ');
      typeKeyword(keyword);
  }



  //MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});

  if (fileName.indexOf('exclusive') != -1) {
      $.post('/getKnowledgeGraph', {url : window.location.href, fileName : fileName}, function(data) {
           if (data != '') {
               window.location.href = data;
           }
           
      });
  }

  
  var loading_more = false;
  var count = 0;
  if (fileName.indexOf('arxiv') != -1) {

    count = fileName.substring(fileName.indexOf('arxiv') + 11,  fileName.indexOf('-'));
  }
  $(window).on('scroll', function(){
    var scrollTop = $(document).scrollTop();
    var windowHeight = $(window).height();
    //var bodyHeight = $(document).height() - windowHeight;
    var bodyHeight = $(document).height();
    var scrollPercentage = (scrollTop / bodyHeight);
    var percentage = 0.8;
    if (column == '1') {
        percentage = 0.8;
    } else if (column == '2') {
        percentage = 0.7;
    } else if (column == '3') {
        percentage = 0.6;
    }
    if(scrollPercentage > percentage && !loading_more) {
      console.log('scrollPercentage:%f', scrollPercentage);
      loading_more = true;

      postArgs = {}
      if (fileName.indexOf('arxiv') != -1) {
          count = count - 300;
          if (count < 300) {
              return;
          }
          postArgs = {'db' : 'eecs/papers/arxiv/', 'key' : 'arxiv' + count + '-arxiv' + getDateTimeStr()}
      } else {
          count = count + 1;
      }
      var parent_div = document.getElementById('loadmore');
      var div = document.createElement('div');
      div.id = 'loadmore-div-' + count;
      if (parent_div == null) {
          parent_div = document.getElementById('searchbox_div');
          //div.setAttribute("align", "left");
          //div.setAttribute("onmouseout", "normal(this);");
          //div.setAttribute("onmouseover", "hover(this);");
          //div.style = 'border-radius: 15px; padding-left: 0px; padding-top: 2px; width: 446px; height: 165px; float: left; background: white;';
      }
      if (parent_div != null) {
          $.post('/loadmore', postArgs, function(data){
              if (data != '') {
                  parent_div.appendChild(div);
                  $('#' + div.id).html(data);
              }
              if (fileName.indexOf('arxiv') != -1) {
                  var target=document.getElementById('total-info');
                  target.style.display="none";
              
                  //MathJax.Hub.Queue(["Typeset", MathJax.Hub, div.id]);
              }
    
              loading_more = false;
          });   
      }
    }
  });
  
});

function refreshTab2(divID, objID, tab) {
    obj = document.getElementById(objID);

    if (obj != null && obj.style.color == 'rgb(130, 35, 18)'){
        var obj = document.getElementById(objID);
        hidendiv_2(divID);
        navTopic(obj, divID.replace('-' + tab, ''), objID.replace('-' + tab, ''), 10);
    }   
}

function refreshTab(aid, tab){
    console.log('aid', aid);
    console.log('tab', tab);

    divID = '';
    objID = aid.replace('td-', '');
    if (objID.indexOf('-a-') != -1) {
        objID = aid.replace('td-', '');
        objID = objID.substring(0, objID.indexOf('-a-'));
        objIDs = objID.split('-');
        //tab = 'history'
        divID = objIDs[0] + '-' + objIDs[1] + '-' + objIDs[2] + '-0-' + tab;
        objID = objIDs[0] + '-' + objIDs[1] + '-' + objIDs[2] + '-0-nav-' + tab;
    
    } else if (aid.indexOf('a-') != -1) {
        divID = aid.replace('a-', 'div-')
        divID = divID.substring(0, divID.indexOf(tab) + tab.length);
        objID = divID.replace(tab, 'nav-' + tab);
    }

    obj = document.getElementById(objID);
    console.log('divID', divID);
    console.log('objID', objID);  
    if (obj != null && obj.style != null && obj.style.color == 'rgb(130, 35, 18)'){
        console.log('style', obj.style.color); 

        var obj = document.getElementById(objID);
        hidendiv_2(divID);
        navTopic(obj, divID.replace('-' + tab, ''), objID.replace('-' + tab, ''), 10);
    }
}

function getDateTimeStr(){
    var s="";
    var d = new Date();
    s += d.getFullYear() ;
    return s;
}

function setText(objN){
    if (isEditing) {
        return;
    }
    var clicktext=document.getElementById(objN);
    console.log('setText', objN);
    console.log('setText', clicktext);
    lastClick = clicktext;
    if (clicktext != null) {
        if (clicktext.text == '...' && clicktext != clickArray[clickArray.length - 1]) {
            clickArray.push(clicktext);
        }

        if (clicktext.innerText == "..."){
            clicktext.innerText="less";
        } else {
            clicktext.innerText="...";
        }
        clicktext.style.color="#999966";  
    }
}

function updateSearchEngine(engin, rID, rTitle, fileName, divID) {
    $.post('/updateSearchEngine', {engin : engin, rID : rID, rTitle : rTitle, fileName : fileName, divID : divID}, function(data) {

        if (data != '') {
            for (var i = 0; i < 10; i++) {
                var div = document.getElementById(divID + '-' + i);
                if (div != null) {
                    div.innerHTML = '';
                } else {
                    break;
                }
            }
            var div = document.getElementById(divID + '-0');
            div.innerHTML = data;           
        }

    });
}

function updateSearchbox(text, moduleStr) {

    if (moduleStr == 'searchbox') {
        return
    }

    a = document.getElementById('searchbox-a');

    if (a.text != 'less') {
        search_box.value = text.split("%20").join(' ');

        if (search_box_target != null) {
            search_box_target.innerHTML = genEnginHtml(search_box_target.id, text, '', '');
        }
    }

}


function appendSearchbox(text) {

    a = document.getElementById('searchbox-a');
    search_box.value = search_box.value + text;

}

function showdiv(targetid,objN){
    if (isEditing) {
        return;
    }
      var target=document.getElementById(targetid);
      if (target == null) {
          console.log("error", targetid);
          return
      }
      /*=
      if (trimStr(target.innerHTML) == '') {
          target.style.display="none";
          return;
      }
      if (targetid.indexOf('tr-') >= 0) {
          if (target.innerHTML.indexOf('showing') < 0) {
            target.style.display="none";
            return;
          }
      }*/
      var clicktext=document.getElementById(objN);
      if (clicktext != null) {
            if (clicktext.innerText=="less"){
                target.style.display="";

                $('#' + targetid).attr("alt", 'showing')
                //console.log("showing" , targetid);
            } else {
                if (targetid.indexOf('tr-') >= 0) {
                    if (target.innerHTML.indexOf('showing') > 0) {
                    } else {
                        target.style.display="none";
                        $('#' + targetid).attr("alt", '')
                    } 
                } else {
                    target.style.display="none";
                    $('#' + targetid).attr("alt", '')
                }
            }       
      }

}

var startPointX = 0;
var startPointY = 0;
var endPointX = 0;
var endPointY = 0;


function drawLine(x1, y1, x2, y2) {
    console.log('drawLine', 'x1:' + x1 + ' y1:' + y1 + ' x2:' + x2 + ' y2:' + y2);
    var line = $('#line');

    line.attr('x1',x1).attr('y1',y1).attr('x2',x2).attr('y2',y2);
}


function tabsPreview(link, titles, urls, highLightText) {
    baseText = '<div align="left">';

    titleList = titles.split('*')
    urlList = urls.split('*');
    openAllJS = "";
    linksHtml = "";
    for (var i = 0; i < urlList.length; i++) {
	if(urlList[i] == '') {
            continue;
	}
        openAllJS += "window.open('" + urlList[i] + "');"
        js = "window.open('" + urlList[i] + "'); hiddenPopup();"
        title = urlList[i];
        if (titleList.length == urlList.length) {
            title = titleList[i];
        }

	if (highLightText != '' && title.toLowerCase().indexOf(highLightText.toLowerCase()) != -1) {
	    title = title.toLowerCase().replace(highLightText.toLowerCase(), '<i><strong>' + highLightText + '</strong></i>');
	}
        linksHtml += '<a href="javascript:void(0);" onclick="' + js + '">' + title + '</a>';
	url = urlList[i].replace("https://", "").replace("http://", "");
	if (url.indexOf("/") > 0) {
            url = url.substring(0, url.indexOf("/"));
        }
	url = "https://www.similarweb.com/zh/website/" + url + "/#competitors"
	linksHtml += ' <a target="_blank" href="' + url + '"><img src="https://img.apkgit.com/f7/com.coffye.pqzsfe/1/icon.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> '
	linksHtml += ' <a target="_blank" href="' + urlList[i] + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a><br>'
    }
    baseText += linksHtml;

    openAllJS += "hiddenPopup();";
    baseText += '<div align="right" style="margin-top: 5px; margin-bottom: 5px; margin-right: 10px;"><a href="javascript:void(0);" onclick="' + openAllJS + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a><a>  </a></div>'
    baseText += '</div>'
    if (urlList.length > 10) {
        showPopup(pageX, pageY, 550, 480);
    } else {
        showPopup(pageX, pageY, 550, 220);
    }

}

var baseText = null;
var popupMode = false;
var popupCMD = ''

function showPopupContent(x, y, w, h, cmd) {
    var paddingLeft = search_box.offsetLeft - 8;
    if (cmd.indexOf('/') != -1) {
        paddingLeft = 10;
    }

    if (x + w > window.innerWidth) {
        x = x - w;
    }

    if (y + h > window.innerHeight) {
	y = y - window.innerHeight / 2;
    }


    $.post('getPluginInfo', {'title' : cmd, 'url' : '', style : 'padding-left:' + paddingLeft + 'px; padding-top: 10px;', 'parentCmd' : '', parentDivID : '', 'popup' : true}, function(result){

        if (result != '') {
            //console.log(parentDivID);
            //$('#' + parentDivID).append('xxxx');
            baseText = result;
            if (popupCMD == '') {
                popupCMD = cmd;
            }
            
            showPopup(x, y, w, h);
            if (x == 0) {
              window.scroll(0, y);
            }
            
        } 
    }); 
    
}

function isPopupShowing() {

    var popUp = document.getElementById("popupcontent");

    if (popUp.style.visibility == 'visible') {
        return true;
    } else {
        return false;
    }

}

function showPopup(x, y, w,h){ 
    var popUp = document.getElementById("popupcontent"); 
    popUp.style.top = y + "px"; 
    popUp.style.left = x + "px"; 
    popUp.style.width = w + "px"; 
    popUp.style.height = h + "px"; 
    if (baseText == null) baseText = popUp.innerHTML; 
    html = '<div id=\"statusbar\" align="right">'
    if (popupCMD != '') {
        //html += '<a href="javascript:void(0);"  onclick=\"showPopupContent(0, 20, 1444, 900, ' + "'" + popupCMD + "'" + ');\"><img src="http://grupojvr.com.mx/web/wp-content/uploads/2014/08/Direcci%C3%B3n-azul.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"><a>'
    }
    html += '<a href="javascript:void(0);"  onclick=\"hiddenPopup();\"><img src="https://cdn2.iconfinder.com/data/icons/duo-toolbar-signs/512/erase-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"><a>  </div>' + baseText; 
    
    popUp.innerHTML = html;
    var sbar = document.getElementById("statusbar"); 
    sbar.style.marginTop = "5px"; 
    sbar.style.marginBottom = "5px"; 
    sbar.style.marginRight = "10px"; 
    popUp.style.visibility = "visible"; 
    popupMode = true;
}

function hiddenPopup(){ 
  var popUp = document.getElementById("popupcontent"); 
  if (popUp != null) {
      popUp.style.visibility = "hidden"; 
      popupMode = false;
      popupLastCMD = '';    
  }

}

function hiddenOrShowLayer(layerID){ 
  var layer = document.getElementById(layerID); 
  if (layer != null) {
      if (layer.style.display == "" || layer.style.display == "block") {
          layer.style.display = "none"; 
      } else {
          layer.style.display = "block"; 
      }
      
  }
}

function search(inputid,optionid){
    var input = document.getElementById(inputid);
    var select = document.getElementById(optionid);
    console.log("xx",input.value);
    //console.log("",select[select.selectedIndex].text);
    //if (input.value.indexOf('http') != -1 || input.indexOf('.com') != -1) {
    //    window.open(input.value);
    //	return;
    //}
    var optionValue = '';
    if (select == null) {
      optionValue = "exclusive";
    } else {
      optionValue = select[select.selectedIndex].value;
    }
    
    if (optionValue.slice(0, 1) == "!"){
        url = "http://duckduckgo.com/?q=" + select[select.selectedIndex].value + " " + input.value.replace("&nbsp;", " ")
        window.open(url);
        userlog(select[select.selectedIndex].text, url, 'searchbox', fileName, '', input.value, '');
    } else if (optionValue == "current") {
        var url = "http://localhost:5000?db=" + database;
        if (key != "") {
            //url = url + "&key=" + key;
        }
        url = url + '&filter="' + input.value + '"' + '&column=1';
        window.open(url)
        userlog(select[select.selectedIndex].text, url, 'searchbox', fileName, '', input.value, '');
    } else if (optionValue == "add") {
        addRecord(fileName, input.value);
    } else if (optionValue == "exclusive") {
        exclusive('exclusive', input.value, '', true, '', fileName, '', engin_args, false);

    } else {
        url = select.value
        text = input.value
        if (text.indexOf(',') != -1) {
            data = text.split(',');
            for (var i = 0; i < data.length; i++) {
                if (data[i] != '') {
                    doSearch(url, trimStr(data[i]));
                }
            }
        } else {
            doSearch(url, text);

        }
        userlog(text, url, 'searchbox', fileName, '', input.value, '');
    }
}

function doSearch(url, text) {
    if (url.indexOf("%s") != -1) {
        url = url.replace("%s", text);
    } else {
        url = url + text;
    }
    window.open(url);
}

function addRecord(fileName, data) {
    $.post('/addRecord', {fileName : fileName, data : data}, function(data) {
        window.location.href = window.location.href;   
    });
}

function add2Library(rid, aid, text, resourceType, library) {

    $.post('/add2Library', {rid : rid, text : text, resourceType : resourceType, library : library}, function(data) {
        window.location.href = window.location.href; 
    });   
}

function exclusiveEx(fileName, data, crossrefPath, newTab, resourceType, originFilename, rID, enginArgs, kgraph, extension) {
    data2 = ''
    if (urlArray.length > 0) {
        data2 = urlArray.join(", ");
    }

    $.post('/exclusive', {fileName : fileName, data : data, data2 : data2, enginArgs : enginArgs, crossrefPath: crossrefPath, crossrefQuery : crossrefQuery, newTab : newTab, resourceType : resourceType, originFilename : originFilename, rID : rID, kgraph : kgraph, extension : extension}, function(data) {
        urlArray = new Array();
        if (data.indexOf('refresh#') != -1) {
            window.location.href = data.substring(data.indexOf('#') + 1);
        } else {
            window.open(data); 
        }
          
    });
}

function exclusive(fileName, data, crossrefPath, newTab, resourceType, originFilename, rID, enginArgs, kgraph) {
    exclusiveEx(fileName, data, crossrefPath, newTab, resourceType, originFilename, rID, enginArgs, kgraph, '')
}

function exclusiveCrossref(rID, rTitle, url, crossref) {
    $.post('/exclusiveCrossref', {rID : rID, rTitle : rTitle, url : url, crossref : crossref}, function(data) {
        if (data.indexOf('refresh#') != -1) {
            window.location.href = data.substring(data.indexOf('#') + 1);
        } else {
            window.open(data); 
        }
          
    });
}

function add2QuickAccess(rid, aid, text, value, resourceType, library) {

    $.post('/add2QuickAccess', {rid : rid, text : text, value : value, resourceType : resourceType, library : library}, function(data) {

        if (data == 'ok') {
            refreshTab(aid, 'history');
        }
    });

}


function batchOpen(data, resourceType) {

    $.post('/batchOpen', {data : data, resourceType : resourceType}, function(data) {
        if (data != '') {
            urls = data.split(' ');
            for (var i = 0; i < urls.length; i++) {
                if (urls[i] != '') {
                    window.open(urls[i]);
                }
            }
        }
    });
}

var lastHovered = '';


var lastHoveredID = '';
var lastHoveredUrl = '';
var lastHoveredText = '';

var lastHoveredCMD = '';


function delteOnHoverUrl(text, moduleStr) {
  $.post('/delteOnHoverUrl', { title : text, module : moduleStr}, function(data) {
      typeKeyword('>:cmd', '');
  });
}

function resetHoverState() {
    KEY_V_DOWN = false;
    KEY_C_DOWN = false;
    lastHoveredID = '';
    lastHoveredUrl = ''; 
    lastHoveredText = '';  
    crossrefQuery = '';
    doConvert = false;
    convertPreview = false;
}

var doConvert = false;
var convertPreview = false;
var convertArgv = '';

function onHoverPreview(aid, text, url, moduleStr, preview) {
    lastHoveredID = aid;
    lastHoveredUrl = url;
    lastHoveredText = text;
    if (moduleStr == 'searchbox' || moduleStr == 'history' || moduleStr == 'convert' || moduleStr == 'filefinder' || moduleStr == 'main') {
        /*if (KEY_SHIFT_DOWN) {
           urls = url.split(',');
           for (var i = 0; i<urls.length; i++) {
               urlArray.push(urls[i]);
           }
           return;
        }*/

        if (preview) {

            //var animID = showLoading('search_preview');
            var top = 0;

            a = document.getElementById(aid);
            if (a != null) {
                var aRect = a.getBoundingClientRect();
                top = aRect.top - 20;
            }
            console.log(urlArray);
            if (url.indexOf('*') != -1 && url.indexOf('[') == -1) {
                //url = url.replace('*', ',');
                url = url.split('*').join(',');
            }
            if (urlArray.length > 0) {
                url = url + ', ' + urlArray.join(", ");
            }
            urlArray = new Array();
            textArray = new Array();
            KEY_V_DOWN = false;
            doConvert = false;
            if (KEY_C_DOWN) {
                doConvert = true;
                KEY_C_DOWN = false;
            }
            var newTab = true;
            var search_preview_div = document.getElementById('search_preview');
            if (search_preview_div != null) {
                newTab = false;
            }
            $.post('/onHover', {text : text, url : url, module : moduleStr, lastTop : top, command : search_box.value, doConvert : doConvert, convertPreview : convertPreview, convertArgv : convertArgv, crossrefQuery : crossrefQuery, newTab : newTab}, function(data) {
                if (data != '') {
                    //console.log(data);
                    //stopLoading(animID);
                    var search_preview = document.getElementById('search_preview');
                    var popUp = document.getElementById("popupcontent"); 
                    
                    if (popUp != null && doConvert == false) {
                        resetHoverState();
                        baseText = data;
                        showPopup(0, 20, 1444, 900);
                        baseText = '';
                    } else if (search_preview != null) {
                        search_preview.innerHTML = '';
                        search_preview.innerHTML = data;
                        resetHoverState();
                        if (search_preview != null) {
                            var rect = null;
                            var preview_link = document.getElementById('search_preview_frame');
                            if (preview_link != null) {
                                rect = preview_link.getBoundingClientRect();
                            } else {
                                rect = search_preview.getBoundingClientRect();
                            }
                            
                            window.scrollTo(0, rect.top);       
                        }         
                    }

                }
            });              
        }
    }
}

function onHover(aid, text, url, rid, moduleStr, fileName, haveDesc) {

    lastHoveredText = text;
    lastHoveredUrl = url;

    var newAid = '';
    var newText = text;


    var aidArray = [];
    var newTextArray = [];
    if (newText.indexOf('(') != -1) {
        newText = newText.substring(0, newText.indexOf('('));
    } 
    aidArray = aid.split('-');

    if (newText.indexOf('/') != -1) {
        newText = newText.substring(newText.indexOf('/') + 1);
    }

    if (newText.indexOf(' - ') != -1) {
        newTextArray = newText.replace(' - ', '-').split('-');
    } else {
        newTextArray = [newText, undefined];
    }


    for (var i = 0; i < aidArray.length; i++) {
        if (i != 0 && i != aidArray.length -1) {
            newAid += aidArray[i];
        } 

        if (i != 0 && i != aidArray.length - 2 && i != aidArray.length - 1) {
            newAid += '-';
        }
    }

    if (newTextArray[1] == undefined) {
        var input = document.getElementById('search_txt');
        var value = input.value;
        if (value.indexOf('/') != -1) {
            value = value.substring(0, value.indexOf('/'));
        }
        lastHoveredCMD = value + '/' + newAid + ':' + newTextArray[0] + '/';
    } else {
        lastHoveredCMD = '>' + newTextArray[0]
            + '/' + newAid + ':' + newTextArray[1] + '/';
    }

    if (hover_mode) {
        console.log(aid + ' onHover ' + 'url:' + url + ' text:' + text + ' rid:' + rid + ' haveDesc:' + haveDesc);
        if (KEY_E_DOWN == false && rid != '') {
            updateSearchbox(text);
        }

        onHoverPreview(aid, text, url, moduleStr, KEY_V_DOWN);

        
        if (moduleStr == 'history' && haveDesc == 'true') {
            more = document.getElementById(aid + '-more');
            if (lastHovered != '' && more != null) {
                lastMore = document.getElementById(lastHovered + '-more');
                if (lastMore != null && lastMore.text == 'less') {
                    lastMore.click();
                }
            }
            if (more != null) {
                more.click();

                lastHovered = aid;
                $('#' + aid).focus();
            }
        }

    }

    

}

var urlArray = new Array();
var textArray = new Array();

function onOpenUrlClicked() {
    //hiddenPopup();
}

function openUrl(url, searchText, newTab, excl, rid, resourceType, aid, moduleStr, fileName) {
    onOpenUrlClicked();

    if (KEY_V_DOWN) {
        return; 
    }

    if (url.indexOf('*') != -1 && url.indexOf('[') == -1) {
        //url = url.replace('*', ',');
        url = url.split('*').join(',');

    }

    //if (KEY_P_DOWN || popupMode) {
    if (KEY_P_DOWN || (popupMode && newTab == false)) {

        KEY_P_DOWN = false;
        urlList = url.split(',');
        for (var i = 0; i < urlList.length; i++) {
          baseText += '<iframe  id="iFrameLink" width="100%" height="700" frameborder="0"  src="' + urlList[i] + '"></iframe><br>'
        }
        
        showPopup(0, 20, 1444, 900);
        window.scroll(0, 20);
        baseText = '';
        return;
    }

    if (KEY_Q_DOWN) {

        add2QuickAccess(rid, aid, searchText, url, resourceType, '');

        KEY_Q_DOWN = false;

        KEY_X_DOWN = true;


        return false;
    } else if (KEY_SHIFT_DOWN) {
        urlArray.push(url);
        textArray.push(searchText);

        console.log(urlArray);
        return false;
    } else if (KEY_E_DOWN) {
        extension = '';
        if (urlArray.length > 0) {
            urlArray.unshift(url);
            console.log(urlArray);
            url = urlArray.join(", ");
            urlArray = new Array();
            textArray = new Array();
            if (searchText.indexOf('(') > 0) {
                searchText = searchText.substring(0, searchText.indexOf('(')) + '(' + url + ')';
            }
        }
        if (excl) {
            updateSearchbox(searchText, moduleStr);
            if (url != '' && searchText.indexOf('(') < 0) {
                searchText = searchText + '(' + url + ')'
            }
            exclusiveEx(fileName, searchText, '', true, resourceType, fileName, rid, '', false, extension);
        } else {
            console.log(search_box.value);
            if(search_box.value != '') {
                updateSearchbox(search_box.value + ', ' + searchText, moduleStr);

            } else {
                updateSearchbox(searchText, moduleStr);
            }  
        }

        KEY_E_DOWN = false;

    } else if (KEY_G_DOWN && resourceType == 'crossref') {
        console.log(url);
        urlPart = url.split('&');
        db = ''
        key = ''
        url = ''
        for (var i = 0; i < urlPart.length; i++) {
            console.log(urlPart[i]);
            if (urlPart[i].indexOf('db=') != -1) {
                db = urlPart[i].substring(urlPart[i].indexOf('db=') + 3);
            }

            if (urlPart[i].indexOf('key=') != -1) {
                key = urlPart[i].substring(urlPart[i].indexOf('key=') + 4);
            }

        }
        console.log(db + key);

        console.log(window.location.href);
        hrefPart = window.location.href.split('&');
        for (var i = 0; i < hrefPart.length; i++) {
            console.log(hrefPart[i]);
            if (hrefPart[i].indexOf('crossrefQuery=') != -1) {
                url += 'crossrefQuery="' + db + key + '"';
            } else {
                url += hrefPart[i];
            }

            if(i != hrefPart.length - 1) {
                url += '&';
            }
        }

        console.log(url);
        window.location.href = url;
        KEY_G_DOWN = false;

    } else if (KEY_S_DOWN || KEY_G_DOWN) {
        //$.post('/toSlack', {title : searchText, url : url, module : moduleStr}, function(data) {

        //});
        if (searchText.indexOf(' - ') > 0) {
            searchText = searchText.substring(searchText.indexOf(' - ') + 3);
        }
        if (searchText.indexOf('(') > 0) {
            searchText = searchText.substring(0, searchText.indexOf('(')).replace('-', ' ').replace('  ', ' ');
        }

        if (KEY_S_DOWN) {
            baseText = genEnginHtml('', searchText, '', '');
            showPopup(pageX, pageY, 340, 100);
            popupMode = false;

            KEY_S_DOWN = false;
        } else if (KEY_G_DOWN) {
            url = 'https://www.google.com/search?newwindow=1&source=hp&q=%s&btnI=I'.replace('%s', searchText);
            window.scroll(0, 20);
            onHoverPreview('', searchText, url, 'searchbox', true);
  
        }

    } else if (newTab) {
        if (url.indexOf(',') != -1) {
            batchOpenUrls(url);
        } else {
            window.open(url);
        }
        
        updateSearchbox(searchText, moduleStr);
    } else {
        window.location.href = url;
    }


    return true;

}

function openAll(text, urls) {
    if (KEY_X_DOWN) {
        var input = document.getElementById('search_txt');
        input.value = text;

    } else {
        batchOpenUrls(urls);

    }
}

function openAllOnePage(text, urls, module) {
    $.post('/allInOnePage', {text : text, urls : urls, module : module}, function(data) {
        if (data != '') {
            window.open(data);
        }
    });
}

function batchOpenUrls(data) {
    if (data == "") {
        return;
    }

    if (data.indexOf(",") != -1) {
        urls = data.split(",");
        for (var i = 0; i < urls.length; i++) {
            if (urls[i] != '') {
                window.open(urls[i]);
            }
        }
    } else {
        window.open(data);
    }
}

function tolist(rID, resourceType, originFilename) {
    if (KEY_X_DOWN) {
        $.post('/tolist', {rID : rID, resourceType : resourceType, originFilename : originFilename, 'returnText': 'true'}, function(data) {
            if (data != '') {
                var input = document.getElementById('search_txt');
                input.value = data;               
            }
        });
    } else {
        $.post('/tolist', {rID : rID, resourceType : resourceType, originFilename : originFilename}, function(data) {
            if (data != '') {
                window.open(data);
            }
        });
    }

}

function createlist(rID, resourceType, originFilename) {
    $.post('/createlist', {rID : rID, resourceType : resourceType, originFilename : originFilename}, function(data) {
        if (data != '') {
            window.open(data);               
        }
    });
}

function merger(rID, resourceType, originFilename) {
    $.post('/merger', {rID : rID, resourceType : resourceType, originFilename : originFilename}, function(data) {
        if (data != '') {
            window.open(data);
        }
    });
}

function trimStr(str){return str.replace(/(^s*)|(s*$)/g,"");}

function searchTopic(obj, rid, topic, otherInfo){
    console.log("xx",obj.text);
    console.log("xx",topic);
    var options = document.getElementsByTagName("option");
    if (otherInfo.indexOf("&user") != -1 && obj.text == "artzub"){
    } else{
         otherInfo = "";
    }
    if (topic == "") {
        var box=document.getElementById("search_txt");
        value = box.value.replace(" ", "&nbsp;");
        if (value != "") {
            topic = value;
            console.log("xx" , "box value " + value);
        }
        
    }
    for(var i=0;i<options.length;i++){
        if (trimStr(options[i].text) == trimStr(obj.text)) {
            console.log("xx", options[i].value);
            if (options[i].value.indexOf("%s") != -1) {
                url = options[i].value.replace("%s", topic.replace("&nbsp;", " ")) + otherInfo
                window.open(url);
                userlog(obj.text, url, 'moreEngin', fileName, rid, topic, '');
            } else {
                console.log("xx", obj.text.slice(0, 1));
                if (options[i].value.slice(0, 1) == "!"){
                    console.log("xx", options[i].value + topic.replace("&nbsp;", " "));
                    url = "http://duckduckgo.com/?q=" + options[i].value + " " + topic.replace("&nbsp;", " ") + otherInfo
                    window.open(url);
                    userlog(obj.text, url, 'moreEngin', fileName, rid, topic, '');
                } else {
                    url = options[i].value + topic.replace("&nbsp;", " ") + otherInfo
                    window.open(url);
                    userlog(obj.text, url, 'moreEngin', fileName, rid, topic, '');
                }
            }
        }
    }
}


var isEditing = false;

function navTopic(obj, divID, parentDivID, countIndex){


    var targetid = divID + "-" + obj.text;
    var target_data_id = divID + "-" + obj.text + '-data';
    var target=document.getElementById(targetid);
    var target_data = document.getElementById(target_data_id);
    for (var i = 0; i < countIndex + 1; i++) {
        console.log("xx",parentDivID + i.toString());
        var parentDiv = document.getElementById(parentDivID + i.toString());
        if (parentDiv == null) {
            continue;
        }
        var children = parentDiv.children;
        for (var j = 0, len = children.length; j < len; j++) {
            children[j].style.color="#888888";
            children[j].style.fontSize="9pt";
            children[j].style.fontStyle="";
        }
    }
    if (track_mode == false) {
        obj.style.color="#822312";
        obj.style.fontSize="13pt"; 
        obj.style.fontStyle="italic";
    }

    if (target.style.display == ""){
        target.style.display="none";
        target_data.style.display="none";
    } else {
        target.style.display="";
        target_data.style.display="";
    }

    var postArgs;

    if (args[divID] != null){
        postArgs = {name : obj.text, rID : args[divID][0], rTitle : args[divID][1], url : args[divID][2], fileName : fileName, 'check' : 'false', column : column};
    } else {
        postArgs = {name : obj.text, rID : 'search', rTitle : search_box.value.replace('', '%20'), url : '', fileName : fileName, 'check' : 'false', column : column};
    }


    if (obj.text == 'edit') {
        isEditing = true;
    } else {
        isEditing = false;
    }


    postArgs["objID"] = obj.id;
    postArgs["divID"] = divID + "-" + obj.text;
    postArgs["defaultLinks"] = 2;
    postArgs['user_name'] = user_name;
    postArgs['targetid'] = targetid;
    postArgs['targetDataId'] = target_data_id;
    postArgs['originFileName'] = fileName;
    postArgs['screenWidth'] = screen.width;
    postArgs['screenHeight'] = screen.height;
    postArgs['page'] = 1;
    postArgs['os'] = getOsInfo();
    postArgs['browser'] = getBrowserInfo();
    postArgs['extension_count'] = extension_count_dict[args[divID][0]];
    postArgs['crossrefQuery'] = crossrefQuery;
    postArgs['windowHref'] = window.location.href

    if (obj.text == 'bookmark' || obj.text == 'filefinder') {
        postArgs['nocache'] = true;
    } else {
        postArgs['nocache'] = false;
    }

    if (track_mode && postArgs['rID'] != '') {
        console.log('datatarget', targetid + '-data');
        data_target = $('#' + targetid + '-data');
        if (data_target != null) {
            data_target.show();
            postArgs["navigate"] = trackmode_engin_type;
            data_target.load('/navigate', postArgs, function(data){
            });
            return;
        }
    }

    postArgs['selection'] = window.getSelection().toString();
    if (obj.text == "search" || obj.text == "keyword") {
        if (obj.text == 'search') {
            postArgs['display'] = '';
        }

        var selection = window.getSelection().toString();
        if (selection != '') {
            postArgs['selection'] = selection;
        } else if (global_selection != '') {
            postArgs['selection'] = global_selection;
            global_selection = '';

        } else {
            if (obj.text == 'search') {
                for (var i = 0; i < starDivCount; i++) {
                    starDivObj = document.getElementById(divID + '-star-' + i.toString())
                    if (starDivObj.style.display == 'none') {
                        starDivObj.style.display = '';

                    } else {
                        starDivObj.style.display = 'none';

                        if (lastHidenDivID != '') {
                            console.log('', lastHidenDivID);
                           document.getElementById(lastHidenDivID).style.display = '';
                           document.getElementById(lastHidenDivID + '-data').style.display = '';
                        }
                        obj.style.color="#888888";
                        obj.style.fontSize="9pt";
                        postArgs['display'] = 'none';
                        //return;
                    }
                    
                }

                //return
            }
            postArgs['selection'] = args[divID][1];
        /*
        if (obj.text == "keyword") {
            postArgs['selection'] = args[divID][1];
        } else {
                $("#" + targetid).html("please select some text for search");
                return
        }*/
        }
        $("#" + targetid).html('');
    }

    for (var i = 0; i < extensions.length; i++) {
        console.log('zzz', extensions[i]);
        if (extensions[i] == obj.text) { 
            requestExtension(postArgs, true);
        }
    }
 
}

function showLoading(targetid) {
    $("#" + targetid).html("<br>Loading ...");
    var i = 0;
    var loadAnimID = setInterval(function() {
        i = ++i % 4;
        $("#" + targetid).html("<br>Loading " + Array(i+1).join("."));
    }, 800);

    return loadAnimID;
}

function stopLoading(loadAnimID) {
    clearInterval(loadAnimID);
}

function requestExtension(postArgs, tipInfo) {
    console.log('', 'requestExtension ' + postArgs['targetDataId']);
    var target_data_id = postArgs['targetDataId'];
    var obj = document.getElementById(postArgs['objID']);
    loadAnimID = '';
    if (tipInfo) {
        loadAnimID = showLoading(target_data_id);
    }


    $('#' + target_data_id).load('/extensions', postArgs, function(data) {
        console.log('return', data);
        if (data == "" || (obj.text == "save" && data.indexOf("sucess") != -1)) {
            obj.style.display="none";
        } else if (data == "refresh"){

            window.location.href = window.location.href;
        } else if (data.indexOf("http") == 0){
           //window.location.href = data;
            window.open(data);
            userlog(postArgs['rTitle'], data, postArgs['name'], postArgs['fileName'], postArgs['rID'], postArgs['rTitle'], '');
            //$("#" + target_data_id).html('<br>&nbsp;&nbsp;<a target="_blank" href="' + data + '">target link</a><br>');
            $("#" + target_data_id).html('');
        } else if (data.substring(0, data.indexOf(' ')) == 'edit') {
           
            url = data.substring(data.indexOf(' ') + 1)
            console.log('execCommand', url);
            $.post('/exec', {command : 'edit', text : url, fileName :  url }, function(data){});
        }
        if (tipInfo) {
            stopLoading(loadAnimID);
        }

        $.post('/extensionJobDone', postArgs, function(data) {

        });
        
        //MathJax.Hub.Queue(["Typeset", MathJax.Hub, postArgs['targetid']]);
    });
}

function showdiv_2(targetid){
      var target=document.getElementById(targetid);
            if (target.style.display=="none"){
                target.style.display="";
            } else {
                target.style.display="none";
            }
}
var lastHidenDivID = ''
function hidendiv_2(targetid){
      
      var selection = window.getSelection().toString();
      if (selection != '') {
          global_selection = selection;
      }
      var target=document.getElementById(targetid);
      //console.log('hidendiv_2 ' + targetid + ' ' + target.style.display);
      if (target.style.display != 'none') {
          target.style.display="none";
          if (targetid.indexOf('search') < 0) {
            lastHidenDivID = targetid;

          }
      }
      //console.log('hidendiv_2 ' + targetid + ' ' + target.style.display);
      
      var target=document.getElementById(targetid + "-data");
      target.style.display="none";
}

function hidendiv_3(targetid){
      var target=document.getElementById(targetid);
      if (target.style.display == 'none') {
          target.style.display="";
      } else {
          target.style.display="none";
      }
}

function share(website, url, title) {
   if (website == "facebook")  {
       window.open('http://www.facebook.com/sharer/sharer.php?u=' + url);
   } else if (website == 'twitter') {
       window.open("https://twitter.com/intent/tweet?text=" + title + ' (' + url + ')');
   } else if (website == 'google+'){
       window.open('https://plus.google.com/share?url=' + url);
   } else if (website == 'linkedin'){
       window.open("http://www.linkedin.com/shareArticle?mini=true&amp;url=" + url + '&amp;title=' + title + ' (' + url + ')&amp;source=xlinkbook');
   } else if (website == 'weibo') {
       window.open('http://service.weibo.com/share/share.php?url=' + url + '&appkey=&title=' + title + '&pic=&ralateUid=&language=zh_cn');
   }
}

function genExtensionHtml(targetid, topic, otherInfo, rID) {
    var extensionHtml= extension_array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo).replace(/#quote/g, "'").replace(/#rid/g, id);
    return extensionHtml

}

function genEnginHtml(targetid, topic, otherInfo, rID) {
    var enginHtml = '';
    if (array != '') {
        enginHtml = array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo).replace(/#quote/g, "'").replace(/#rid/g, rID);
    }
    return enginHtml;
}


function appendEnginExtensionHtml(targetid, topic, otherInfo, rID, extensionHtml) {
    var enginHtml = genEnginHtml(targetid, topic, otherInfo, rID);
    var target=document.getElementById(targetid);
    //query server for engin html updateSearchEngine()
    target.innerHTML = enginHtml + extensionHtml;
}


function appendContent(targetid, id, topic, url, otherInfo, hidenEngin) {
    console.log('appendContent',targetid);
    var target=document.getElementById(targetid);
    url = url.replace(' ', '%20');
    if (target.innerHTML.indexOf(topic) > 0) {
        if (!disable_thumb) {
            if ($('#div-thumb-' + id.toLowerCase()).is(':visible')) {
                $('#div-thumb-' + id.toLowerCase()).hide();
            } else {
                var url = $('#div-thumb-' + id.toLowerCase()).children('img').attr('src');
                $('#div-thumb-' + id.toLowerCase()).children('img').attr('src', "");
                $('#div-thumb-' + id.toLowerCase()).children('img').attr('src', url);
                $('#div-thumb-' + id.toLowerCase()).show();
            }
        }
        return;
    }

    args[targetid] = [id, topic, url];

    var extensionHtml= extension_array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo).replace(/#quote/g, "'").replace(/#rid/g, id);
    console.log('engin_args', engin_args);
    if (engin_args != '') {
        appendEnginExtensionHtml(targetid, topic, otherInfo, id, extensionHtml);
        appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin);
    } else {
        $.post('/queryStarEngin', {rID : id, rTitle : topic, targetid : targetid, url : url, otherInfo : otherInfo}, function(data) {
        if (data == '') {
            appendEnginExtensionHtml(targetid, topic, otherInfo, id, extensionHtml);
        } else {
            target.innerHTML = data + extensionHtml;
        }
        appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin);
    });

    }

}

function hidenEnginSection(targetid) {
    for (var i = 0; i < starDivCount; i++) {
        var obj = document.getElementById(targetid + '-star-' + i.toString());
        if (obj != null) {
            obj.style.display = "none";
        }
    }    
}

function appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin) {

    if (hidenEngin) {
        //target.innerHTML = enginHtml + extensionHtml;
        //console.log('', targetid + '-star-0');
        hidenEnginSection(targetid);
    }
    
    console.log("xx", reference[id]);

    for (var i = 0; i < extensions.length; i++) {
        hidenMetadata(targetid, extensions[i], "none");
    }
    if (id == "") {
        console.log("xx", 'id is empty');
        return;
    }
    var module = "*";
    var nocache = 'false'
    //if (targetid.indexOf("-content-") > 0) {
    //    module = "content"
    //}
    if (fileName.indexOf("library") > 0){
        nocache = "true";
    }
    var os = getOsInfo();
    var browser = getBrowserInfo();

    if (crossrefQuery != '') {
        nocache = 'true';
    }

    $.post('/extensions', {name : module, rID : id, rTitle : topic, url : url, fileName : fileName, originFileName : fileName, nocache : nocache, column : column, 'check' : 'true', user_name : user_name, os : os, browser : browser, crossrefQuery : crossrefQuery, windowHref : window.location.href}, function(data){
        if (data.trim() != '') {
            console.log("xx", data)
            var extensions = data.split(" ");
            extension_count_dict[id] = extensions.length;
            for (var i = 0; i < extensions.length; i++) {
                hidenMetadata(targetid, extensions[i], "");
            }
            $.post('/queryNavTab', {name : module, rID : id, rTitle : topic, url : url, fileName : fileName, targetid : targetid, otherInfo : otherInfo, column : column, crossrefQuery : crossrefQuery}, function(data1){

                console.log("data1", data1);

                if (data1 != '' && data1.indexOf(",") >= 0) {
                    dataSplit = data1.split(',');
                    default_tab =  dataSplit[0].trim();
                    second_default_tab = dataSplit[1].trim();
                    console.log("default_tab ", default_tab);
                    console.log("second_default_tab ", second_default_tab);
                }

                if (extension != '' && data.indexOf(extension) >= 0) {
                    navTopic(document.getElementById(targetid + "-nav-" + extension), targetid, targetid + "-nav-",4);
                    extension = '';
                    return;

                }

                if (data.indexOf(default_tab) >= 0) {
                    for (var i = 0; i < extensions.length; i++) {
                        if (extensions[i] == default_tab){
                            navTopic(document.getElementById(targetid + "-nav-" + default_tab), targetid, targetid + "-nav-",4);
                            return;
                        }
                    }
                }
                
                if (data.indexOf(second_default_tab) >= 0) {
                    for (var i = 0; i < extensions.length; i++) {
                        if (extensions[i] == second_default_tab){
                            navTopic(document.getElementById(targetid + "-nav-" + second_default_tab), targetid, targetid + "-nav-",4);
                            return;
                        }
                    }
                }

            });
        }
    });

    if (!disable_thumb && id.indexOf('loop') < 0) {
        $.post('/thumb', {name : module, rID : id, url : url, fileName : fileName, nocache : nocache, 'check' : 'false'}, function(data){
            if (data != '') {

                $('#div-thumb-' + id.toLowerCase()).html('<a target="_blank" href="' + data+ '"><image width="78px" height="70px" src="https://api.thumbalizr.com/?url=' + data + '&width=1280&quality=100"/></a>');
            }
        });
    }
}

function hidenMetadata(targetid, datatype, value){
    var target=document.getElementById(targetid);
    var children = target.children;
    for (var j = 0, len = children.length; j < len; j++) {
        if (children[j].id.indexOf(targetid + "-nav") != -1){
            var children2 = children[j].children;
            for (var i = 0, len2 = children2.length; i < len2; i++) {
                if (children2[i].text == datatype){
                    children2[i].style.display = value;
                }
            }
        }
    }
}

var search_box_target;
function appendContentBox(targetid, boxid){

    if (isEditing) {
        return;
    }
    var target=document.getElementById(targetid);
    var box=document.getElementById(boxid);

    console.log('', target.style.display);
    if (target.style.display.trim() == 'none') {
        console.log("appendContentBox", "return");
        target.innerHTML = '';
        return;
    }
    searchbox_a = document.getElementById('searchbox-a');
    searchbox_a.focus();
    search_box = box;
    search_box_target = target;
    console.log("id", targetid);
    var data = box.value;
    while(data.indexOf(' ') >= 0) {
	   data = data.replace(' ', '%20');
    }

    keyword = data
    if (keyword.indexOf('(') != -1) {
        keyword = keyword.substring(0, keyword.indexOf('('))
    }
    searchHTML = genEnginHtml(targetid, keyword, '', '');
    loadAnimID = showLoading(targetid);

    if (data.indexOf('>') != -1 || data.indexOf('?') != -1 || data.indexOf(':') != -1) {
        searchHTML = '<br><br>';
    } 

    paddingLeft = search_box.offsetLeft - 8;

    if (data.indexOf('./') == -1) {
        data = data.split('.').join('/'); 
    }
    
    if (data.indexOf('/') != -1) {
        paddingLeft = 20;
    }

    if (data.indexOf('>:cmd') != -1) {
        paddingLeft = search_box.offsetLeft - 8;
    }
    resetHoverState();
    //$.post('getPluginInfo', {'title' : data, 'url' : '', style : 'padding-left: ' + (search_box.offsetLeft - 8) + '; padding-top: 10px;', 'parentCmd' : parentCmdOfTypeKeyword}, function(result){
    $.post('getPluginInfo', {'title' : data, 'url' : '', style : 'padding-left:' + paddingLeft + 'px; padding-top: 10px;', 'parentCmd' : parentCmdOfTypeKeyword}, function(result){

        stopLoading(loadAnimID);
        if (result != '') {
            target.innerHTML = searchHTML + result;

            $.post('getUnfoldCmd', {'title' : data}, function(result){
                if (result != '') {
                    //search_box.value = result;
                }
            });
        } else {
            target.innerHTML = searchHTML;
            
        }
    });
    /*
    for (var i = 0; i < extensions.length; i++) {
        hidenMetadata(targetid, extensions[i], "none")
    }*/
}

function hidenMoreContent(pid, start) {
    if (pid == 'searchbox_div') {
        return;
    }
    id1 = pid.split('-')[start];
    id2 = pid.split('-')[start + 1];

    if (id2 == null || id1 == null) {
        return
    }
    
    setText('a-' + id1.toString() + '-' + id2.toString() + '-0');
    showdiv('div-' + id1.toString() + '-' + id2.toString() + '-0','a-' + id1.toString() + '-' + id2.toString() + '-0');
    var count = hidenMoreCount;
    var index = 0;
    for (var i = 0; i < count; i++) {
        id = id1.toString() + '-' + id2.toString() + '-' + i.toString()
        trid = id2 + '-' + i.toString()
        console.log(id);
        console.log(trid);

        if (document.getElementById('td-div-' + id) != null) {
            showdiv('td-div-' + id, 'a-' + id1.toString() + '-' + id2.toString() + '-0' );
            showdiv('tr-' + trid, 'a-' + id1.toString() + '-' + id2.toString() + '-0' );
            index = 0;
        } else {
            if (index > 1223) {
                break;
            }
            index = index + 1;
            continue;
        }
    }
}

function toPage(page, url) {
    console.log('url', url);
    href = window.location.href;
    if (href.indexOf('/library') > 0) {
        href = url;
    }
    console.log('ss', href);
    href = replaceArg(href, 'page', page);
    
    console.log('href', href);
    window.location.href = href;
    //alter(href);
}

function replaceArg(url, arg, value) {
    href = url;
    if (href.indexOf(arg + '=') > 0) {
        split_data = href.split(arg + '=')
        part = "";
        if (split_data[1].indexOf('&') > 0) {
            part = split_data[1].substring(split_data[1].indexOf('&') + 1);
        }
        href = split_data[0] + part
        //href = href.substring(0, href.indexOf('&page='))
    }
    if (href.substring(href.length - 1) == '&') {
        href = href + arg + '=' + value;
    } else {
        href = href + '&' + arg + '=' + value;
    }
    return href;
}

function exec(command, text, url) {
    console.log('execCommand', url);
    updateSearchbox(text);

    if (KEY_SHIFT_DOWN) {
        urlArray.push(url);
        textArray.push(text);

        console.log(urlArray);
        return false;
    }
    $.post('/exec', {command : command, text : text, fileName : url }, function(data) {
        if (data != '') {
            $('#search_preview').html(data);
        }

    });
}

function userlog(text, url, module, library, rid, searchText, resourceType) {
    if (KEY_X_DOWN) {
        KEY_X_DOWN = false;
        return;
    }
    var os = getOsInfo();
    var browser = getBrowserInfo();
    $.post("/userlog", {text : text , searchText : searchText, url : url, module : module, library : library, rid : rid, resourceType: resourceType, user : user_name, os : os, browser : browser, ip : '', from : '', mac : ''}, function(data){});
}

function userlogEx(aid, refreshID, text, url, module, library, rid, searchText, resourceType) {
    if (KEY_X_DOWN) {
        KEY_X_DOWN = false;
        return;
    }
    var os = getOsInfo();
    var browser = getBrowserInfo();
    $.post("/userlog", {aid : aid, refreshID : refreshID, text : text , searchText : searchText, url : url, module : module, library : library, rid : rid, resourceType: resourceType, user : user_name, os : os, browser : browser, ip : '', from : '', mac : ''}, function(data){
        
        if (refreshID != '') {
            console.log('refreshID:' + refreshID);
            refreshTab(refreshID, 'history');
        }

    });
}

function agentRequest(agentName, rid, path) {

    $.post("/agent", {agentName : agentName, rid : rid, path : path}, function(data) {
        
    });

}

lastSwitchLinkBGColorObj = null;

function switchLinkBGColor(id, color1, color2) {
    var obj = document.getElementById(id);
    if (obj != null) {
        console.log(obj.style.background);
        if (obj.style.background == color2 || obj.style.background=='') {
            obj.style.background = color1;
            
            if (lastSwitchLinkBGColorObj != null) {
                lastSwitchLinkBGColorObj.style.background = color2;
            }
        } else {
            obj.style.background = color2;
        }

        lastSwitchLinkBGColorObj = obj;
    }
}

function chanageLinkColorByID(id, color, fontSize) {
    console.log('chanageLinkColorByID', id);
    var obj = $(id);
    chanageLinkColor(obj, color, fontSize);
}

function chanageLinkColor(obj, color, fontSize) {
    console.log('chanageLinkColor', obj);
    console.log('chanageLinkColor', color);
    if (fontSize != '') {
        obj.innerHTML = '<font color="' + color + '" size="' + fontSize + '">' + obj.text + '</font>'
    } else {
        if (color != '') {
            //obj.style.background = color;//'#CCEEFF'
            if (obj.style != null) {
                obj.style.color = color;
            }
            
        }
    }

    obj.innerHTML = '<s>' + obj.innerHTML + '</s>';
}

function queryUrlFromServer(text, url, module, library, rid, searchText, resourceType, newTab, isTag, fileName, log) {
    //console.log('queryUrlFromServer--->', searchText);

    $.post("/queryUrl", {text : text , searchText : searchText, url : url, module : module, library : library, rID : rid, resourceType: resourceType, user : user_name, isTag : isTag, fileName : fileName, enginArgs : engin_args}, function(data){
        console.log('queryUrlFromServer--->', data);
        var urls = null;
        if (data.indexOf(' ') > 0) {
            urls = data.split(' ');
        } else {
            urls = [data];
        }

        for (var i = 0; i < urls.length; i++) {
            if (urls[i] != '') {
                window.open(urls[i]);
                if (log) {
                    userlog(text, urls[i], module, library, rid, searchText, resourceType); 
                }
            }
        }
    });
}

function getBrowserInfo() {
    var ua = navigator.userAgent.toLowerCase(); 
    var isStrict = document.compatMode == "CSS1Compat"  
    isOpera = ua.indexOf("opera") > -1  
    isChrome = ua.indexOf("chrome") > -1  
    isSafari = !isChrome && (/webkit|khtml/).test(ua)  
    isSafari3 = isSafari && ua.indexOf('webkit/5') != -1  
    isIE = !isOpera && ua.indexOf("msie") > -1  
    isIE7 = !isOpera && ua.indexOf("msie 7") > -1  
    isIE8 = !isOpera && ua.indexOf("msie 8") > -1  
    isGecko = !isSafari && !isChrome && ua.indexOf("gecko") > -1  
    isGecko3 = isGecko && ua.indexOf("rv:1.9") > -1  
    isBorderBox = isIE && !isStrict  
    var broser = ""; 

    if(isIE){  
        broser = "IE 6";  
    }else if(isIE7){  
        broser = "IE 7";  
    }else if(isIE8){  
        broser = "IE 8";  
    }else if(isOpera){  
        broser = "Opera";  
    }else if(isChrome){  
        broser = "Chrome";  
    }else if(isSafari){  
        broser = "Safari";  
    }else if(isSafari3){  
        broser = "Safari3";  
    }else{  
        broser = "Unknow";  
    }     
    return broser;
}

function getOsInfo() {
    var ua = navigator.userAgent.toLowerCase();  
                
    isWin7 = ua.indexOf("nt 6.1") > -1  
    isVista = ua.indexOf("nt 6.0") > -1  
    isWin2003 = ua.indexOf("nt 5.2") > -1  
    isWinXp = ua.indexOf("nt 5.1") > -1  
    isWin2000 = ua.indexOf("nt 5.0") > -1  
    isWindows = (ua.indexOf("windows") != -1 || ua.indexOf("win32") != -1)  
    isMac = (ua.indexOf("macintosh") != -1 || ua.indexOf("mac os x") != -1)  
    isAir = (ua.indexOf("adobeair") != -1)  
    isLinux = (ua.indexOf("linux") != -1)  
      
    var sys = "";  
     
    if(isWin7){  
        sys = "Windows 7";  
    }else if(isVista){  
        sys = "Vista";  
    }else if(isWinXp){  
        sys = "Windows xp";  
    }else if(isWin2003){  
        sys = "Windows 2003";  
    }else if(isWin2000){  
        sys = "Windows 2000";  
    }else if(isWindows){  
        sys = "Windows";  
    }else if(isMac){  
        sys = "Macintosh";  
    }else if(isAir){  
        sys = "Adobeair";  
    }else if(isLinux){  
        sys = "Linux";  
    }else{  
        sys = "Unknow";  
    }  
    return sys;
}

function setbg(id, color) {
    document.getElementById(id).style.background=color
}
