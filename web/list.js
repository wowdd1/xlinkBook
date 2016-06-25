var args = [];

$(document).ready(function(){
	
  //urlq = QueryString.q;
  
  //if(msg !== '') { d3.select("#rtable").append('div').classed('msg', true).html(msg); }
 
  //addPapers(20, false);
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
    if(scrollPercentage > 0.8 && !loading_more) {
      console.log('scrollPercentage:%f', scrollPercentage);
      //addPapers(5, true);
      //alert('xx');
      loading_more = true;
      count = count - 300;
      if (count < 300) {
          return;
      }
      postArgs = {'db' : 'eecs/papers/arxiv/', 'key' : 'arxiv' + count + '-arxiv2016'}
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
MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});

function setText(objN){
    var clicktext=document.getElementById(objN);
    if (clicktext.innerText == "..."){
        clicktext.innerText="less";
    } else {
        clicktext.innerText="...";
    }
    clicktext.style.color="#999966";
}
function showdiv(targetid,objN){
      var target=document.getElementById(targetid);
      if (target == null) {
          console.log("error", targetid);
          return
      }
      var clicktext=document.getElementById(objN);
            if (clicktext.innerText=="less"){
                target.style.display="";
                $('#' + targetid).attr("alt", 'showing')
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
    if (select[select.selectedIndex].value.slice(0, 1) == "!"){
        window.open("http://duckduckgo.com/?q=" + select[select.selectedIndex].value + " " + input.value.replace("&nbsp;", " "));
    } else if (select[select.selectedIndex].value == "current") {
        var url = "http://localhost:5000?db=" + database;
        if (key != "") {
            //url = url + "&key=" + key;
        }
        url = url + '&filter="' + input.value + '"' + '&column=1';
        window.open(url)
    } else {
        window.open(select.value + input.value);
    }
}
function trimStr(str){return str.replace(/(^s*)|(s*$)/g,"");}
function searchTopic(obj, topic, otherInfo){
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
            if (options[i].value.indexOf("$") != -1) {
                window.open(options[i].value.replace("$", topic.replace("&nbsp;", " ")) + otherInfo);
            } else {
                console.log("xx", obj.text.slice(0, 1));
                if (options[i].value.slice(0, 1) == "!"){
                    console.log("xx", options[i].value + topic.replace("&nbsp;", " "));
                    window.open("http://duckduckgo.com/?q=" + options[i].value + " " + topic.replace("&nbsp;", " ") + otherInfo);
                } else {
                    window.open(options[i].value + topic.replace("&nbsp;", " ") + otherInfo);
                }
            }
        }
    }
}

function navTopic(obj, divID, parentDivID, countIndex){
    var targetid = divID + "-" + obj.text;
    var target=document.getElementById(targetid);
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
    obj.style.color="#822312";
    obj.style.fontSize="12pt";
    if (target.style.display == ""){
        target.style.display="none";
    } else {
        target.style.display="";
    }

    var postArgs;
    if (args[divID] != null){
        postArgs = {name : obj.text, rID : args[divID][0], rTitle : args[divID][1], url : args[divID][2], fileName : fileName, 'check' : 'false', column, column};
    } else {
        postArgs = {name : obj.text, rID : 'search', rTitle : search_box.value.replace('', '%20'), url : '', fileName : fileName, 'check' : 'false', column, column};
    }
    postArgs["divID"] = divID + "-" + obj.text;
    postArgs["defaultLinks"] = 2;
    var extension = false;
    for (var i = 0; i < extensions.length; i++) {
        console.log('zzz', extensions[i]);
        if (extensions[i] == obj.text) { 
            extension = true;
            $("#" + targetid).html("Loading ...");
            var loadAnimID = setInterval(function() {
                i = ++i % 4;
                $("#" + targetid).html("Loading " + Array(i+1).join("."));
            }, 800);
            $('#' + targetid).load('/extensions', postArgs, function(data){
                 console.log('return', data);
                 if (data == "" || (obj.text == "save" && data.indexOf("sucess") != -1)) {
                     obj.style.display="none";
                 } else if (data.indexOf("http") == 0){
                     //window.location.href = data;
                     window.open(data);
                 }
                 clearInterval(loadAnimID);
                 MathJax.Hub.Queue(["Typeset", MathJax.Hub, targetid]);
             });
        }
    }
    if (!extension && postArgs['rID'] != '') {
        console.log('datatarget', targetid + '-data');
        data_target = $('#' + targetid + '-data');
        if (data_target != null) {
            data_target.show();
            postArgs["navigate"] = 'true';
            data_target.load('/navigate', postArgs, function(data){
            });
        }
    }
}
function showdiv_2(targetid){
      var target=document.getElementById(targetid);
            if (target.style.display=="none"){
                target.style.display="";
            } else {
                target.style.display="none";
            }
}
function hidendiv_2(targetid){
      var target=document.getElementById(targetid);
      target.style.display="none";
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

function appendContent(targetid, id, topic, url, otherInfo){
    var target=document.getElementById(targetid);
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
    target.innerHTML = array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo);
    console.log("xx", reference[id]);

    for (var i = 0; i < extensions.length; i++) {
        hidenMetadata(targetid, extensions[i], "none");
    }
    if (id == "") {
        return;
    }
    var module = "*";
    var nocache = 'false'
    if (targetid.indexOf("-content-") > 0) {
        module = "content"
    }
    if (fileName.indexOf("library") > 0){
        nocache = "true";
    }
    $.post('/extensions', {name : module, rID : id, url : url, fileName : fileName, nocache : nocache, 'check' : 'true'}, function(data){
        if (data.trim() != '') {
            console.log("xx", data)
            var extensions = data.split(" ");
            for (var i = 0; i < extensions.length; i++) {
                hidenMetadata(targetid, extensions[i], "");
                if (extensions[i] == default_tab){
                    navTopic(document.getElementById(targetid + "-nav-" + default_tab), targetid, targetid + "-nav-",4);
                }
            }
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
var search_box;
function appendContentBox(targetid, boxid){
    var target=document.getElementById(targetid);
    var box=document.getElementById(boxid);
    search_box = box;
    console.log("id", targetid);
    target.innerHTML = array.join("").replace(/#div/g, targetid).replace(/#topic/g, box.value.replace('', '%20')).replace(/#otherInfo/g, "");
    for (var i = 0; i < extensions.length; i++) {
        hidenMetadata(targetid, extensions[i], "none")
    }
}
