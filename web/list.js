var args = [];
var search_box;
var global_selection = '';
var extension_count_dict = [];


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
    isTag = false;
    originText = text
    result = content2(content_id, dialog_engin_count, dialog_command_count);

    if (data.indexOf('#') > 0) {
        split_data = data.split('#');
        rid = split_data[0];
        resourceType = split_data[1];
        aid = split_data[2];
        if (split_data[3] == 'True') {
            isTag = true;
        }
        originText = split_data[4];
    }
    
    dialog_args = {type : 'dialog', rID : rid, searchText: text, originText : originText, resourceType : resourceType, fileName : fileName, library : library, aid : aid, enginArgs : engin_args, isTag : isTag};
    $.post('/queryUrl', dialog_args, function(data) {
        if (data.indexOf('#') > 0 && data.substring(0, data.indexOf('#')).indexOf('color:') < 0) {
            engin_count = parseInt(data.substring(0, data.indexOf('#')));
            data = data.substring(data.indexOf('#') + 1);
            console.log('', aid);

            $('#' + content_id).html(data);

        } else {
            $('#' + content_id).html(data);
        }
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



$(document).ready(function(){

  search_box = document.getElementById('search_txt');

  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});

  if (fileName.indexOf('exclusive') != -1) {
      $.post('/getKnowledgeGraph', {url : window.location.href, fileName : fileName}, function(data) {
           if (data != '') {
               window.location.href = data;
           }
           
      });
  }

  if (fileName.indexOf('arxiv') != -1) {

  var loading_more = false;
  var count = 0;
  count = fileName.substring(fileName.indexOf('arxiv') + 11,  fileName.indexOf('-'))
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
      count = count - 300;
      if (count < 300) {
          return;
      }
      postArgs = {'db' : 'eecs/papers/arxiv/', 'key' : 'arxiv' + count + '-arxiv' + getDateTimeStr()}
      var parent_div = document.getElementById('loadmore');
      var div = document.createElement('div');
      div.id = 'loadmore-div-' + count;
      parent_div.appendChild(div)
      
      $('#' + div.id).load('/loadmore', postArgs, function(data){
          var target=document.getElementById('total-info');
          target.style.display="none";
          loading_more = false;
          MathJax.Hub.Queue(["Typeset", MathJax.Hub, div.id]);
      });
    }
  });
  }
});

function getDateTimeStr(){
    var s="";
    var d = new Date();
    s += d.getFullYear() ;
    return s;
}

function setText(objN){
    var clicktext=document.getElementById(objN);
    if (clicktext.innerText == "..."){
        clicktext.innerText="less";
    } else {
        clicktext.innerText="...";
    }
    clicktext.style.color="#999966";
}

function updateSearchbox(text) {
    search_box.value = text.split("%20").join(' ');
    if (search_box_target != null) {
        search_box_target.innerHTML = genEnginHtml(search_box_target.id, text, '', '');
    }
}

function showdiv(targetid,objN){
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

function search(inputid,optionid){
    var input = document.getElementById(inputid);
    var select = document.getElementById(optionid);
    console.log("xx",input.value);
    console.log("",select[select.selectedIndex].text);
    //if (input.value.indexOf('http') != -1 || input.indexOf('.com') != -1) {
    //    window.open(input.value);
    //	return;
    //}
    if (select[select.selectedIndex].value.slice(0, 1) == "!"){
        url = "http://duckduckgo.com/?q=" + select[select.selectedIndex].value + " " + input.value.replace("&nbsp;", " ")
        window.open(url);
        userlog(select[select.selectedIndex].text, url, 'searchbox', fileName, '', input.value, '');
    } else if (select[select.selectedIndex].value == "current") {
        var url = "http://localhost:5000?db=" + database;
        if (key != "") {
            //url = url + "&key=" + key;
        }
        url = url + '&filter="' + input.value + '"' + '&column=1';
        window.open(url)
        userlog(select[select.selectedIndex].text, url, 'searchbox', fileName, '', input.value, '');
    } else if (select[select.selectedIndex].value == "add") {
        addRecord(fileName, input.value);
    } else if (select[select.selectedIndex].value == "exclusive") {
        exclusive('exclusive', input.value, '', true, '', fileName, '', engin_args, false);

    } else {
        url = select.value
        if (url.indexOf("%s") != -1) {
            url = url.replace("%s", input.value);
        } else {
            url = select.value + input.value;
        }
        window.open(url);
        userlog(select[select.selectedIndex].text, url, 'searchbox', fileName, '', input.value, '');
    }
}

function addRecord(fileName, data) {
    $.post('/addRecord', {fileName : fileName, data : data}, function(data) {
        window.location.href = window.location.href;   
    });
}

function exclusive(fileName, data, crossrefPath, newTab, resourceType, originFilename, rID, enginArgs, kgraph) {
    $.post('/exclusive', {fileName : fileName, data : data, enginArgs : enginArgs, crossrefPath: crossrefPath, newTab : newTab, resourceType : resourceType, originFilename : originFilename, rID : rID, kgraph : kgraph}, function(data) {
        if (data.indexOf('refresh#') != -1) {
            window.location.href = data.substring(data.indexOf('#') + 1);
        } else {
            window.open(data); 
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
    $.post('/tolist', {rID : rID, resourceType : resourceType, originFilename : originFilename}, function(data) {
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
        }
    }
    if (track_mode == false) {
        obj.style.color="#822312";
        obj.style.fontSize="12pt"; 
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

function requestExtension(postArgs, tipInfo) {
    console.log('', 'requestExtension ' + postArgs['targetDataId']);
    var target_data_id = postArgs['targetDataId'];
    var obj = document.getElementById(postArgs['objID']);
    if (tipInfo) {
        $("#" + target_data_id).html("<br>Loading ...");
        var i = 0;
        var loadAnimID = setInterval(function() {
            i = ++i % 4;
            $("#" + target_data_id).html("<br>Loading " + Array(i+1).join("."));
        }, 800);
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
            clearInterval(loadAnimID);
        }

        $.post('/extensionJobDone', postArgs, function(data) {

        });
        
        MathJax.Hub.Queue(["Typeset", MathJax.Hub, postArgs['targetid']]);
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
      if (target.style.display != 'none') {
          target.style.display="none";
          if (targetid.indexOf('search') < 0) {
            lastHidenDivID = targetid;

          }
      }
      
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
    if (array != '') {
        var enginHtml = array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo).replace(/#quote/g, "'").replace(/#rid/g, rID);
        return enginHtml
    } else {
        return '';
    }


}


function appendContent(targetid, id, topic, url, otherInfo, hidenEngin) {
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
        var enginHtml = genEnginHtml(targetid, topic, otherInfo, id)
        target.innerHTML = enginHtml + extensionHtml;
        appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin);
    } else {
        $.post('/queryStarEngin', {rID : id, rTitle : topic, targetid : targetid, url : url, otherInfo : otherInfo}, function(data) {
        if (data == '') {
            var enginHtml = genEnginHtml(targetid, topic, otherInfo, id)
            target.innerHTML = enginHtml + extensionHtml;
        } else {
            target.innerHTML = data + extensionHtml;
        }
        appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin);
    });

    }

}

function appendContentEx(targetid, id, topic, url, otherInfo, hidenEngin) {

    if (hidenEngin) {
        //target.innerHTML = enginHtml + extensionHtml;
        //console.log('', targetid + '-star-0');
        for (var i = 0; i < starDivCount; i++) {
            var obj = document.getElementById(targetid + '-star-' + i.toString());
            if (obj != null) {
                obj.style.display = "none";
            }
        } 
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

    $.post('/extensions', {name : module, rID : id, rTitle : topic, url : url, fileName : fileName, originFileName : fileName, nocache : nocache, column : column, 'check' : 'true', user_name : user_name, os : os, browser : browser}, function(data){
        if (data.trim() != '') {
            console.log("xx", data)
            var extensions = data.split(" ");
            extension_count_dict[id] = extensions.length;
            var found = false;
            for (var i = 0; i < extensions.length; i++) {
                hidenMetadata(targetid, extensions[i], "");
            }
            $.post('/queryNavTab', {name : module, rID : id, rTitle : topic, url : url, fileName : fileName, targetid : targetid, otherInfo : otherInfo, column : column}, function(data1){

                console.log("data1", data1);

                if (data1 != '' && data1.indexOf(",") >= 0) {
                    dataSplit = data1.split(',');
                    default_tab =  dataSplit[0].trim();
                    second_default_tab = dataSplit[1].trim();
                    console.log("default_tab ", default_tab);
                    console.log("second_default_tab ", second_default_tab);
                }   

                if (data.indexOf(default_tab) >= 0) {
                    for (var i = 0; i < extensions.length; i++) {
                        if (extensions[i] == default_tab){
                            navTopic(document.getElementById(targetid + "-nav-" + default_tab), targetid, targetid + "-nav-",4);
                            found = true;
                            break;
                        }
                    }
                }
                
                if (data.indexOf(second_default_tab) >= 0 && !found) {
                    for (var i = 0; i < extensions.length; i++) {
                        if (extensions[i] == second_default_tab){
                            navTopic(document.getElementById(targetid + "-nav-" + second_default_tab), targetid, targetid + "-nav-",4);
                            found = true;
                            break;
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
    var target=document.getElementById(targetid);
    var box=document.getElementById(boxid);
    search_box = box;
    search_box_target = target;
    console.log("id", targetid);
    var data = box.value;
    while(data.indexOf(' ') >= 0) {
	data = data.replace(' ', '%20');
    }
    target.innerHTML = genEnginHtml(targetid, data, '', '');
    for (var i = 0; i < extensions.length; i++) {
        hidenMetadata(targetid, extensions[i], "none")
    }
}

function hidenMoreContent(pid, start) {
    if (pid == 'searchbox_div') {
        return;
    }
    id1 = pid.split('-')[start];
    id2 = pid.split('-')[start + 1];
    
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
    $.post('/exec', {command : command, text : text, fileName : url }, function(data){});
}

function userlog(text, url, module, library, rid, searchText, resourceType) {
    var os = getOsInfo();
    var browser = getBrowserInfo();
    $.post("/userlog", {text : text , searchText : searchText, url : url, module : module, library : library, rid : rid, resourceType: resourceType, user : user_name, os : os, browser : browser, ip : '', from : '', mac : ''}, function(data){});
}

function agentRequest(agentName, rid, path) {

    $.post("/agent", {agentName : agentName, rid : rid, path : path}, function(data) {
        
    });

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