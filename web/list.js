var args = []

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
      var clicktext=document.getElementById(objN);
            if (clicktext.innerText=="less"){
                target.style.display="";
            } else {
                target.style.display="none";
            }
}
function search(inputid,optionid){
    var input = document.getElementById(inputid);
    var select = document.getElementById(optionid);
    console.log("xx",input.value);
    console.log("",select[select.selectedIndex].text);
    if (select[select.selectedIndex].value.slice(0, 1) == "!"){
        window.open("http://duckduckgo.com/?q=" + select[select.selectedIndex].value + " " + input.value.replace("&nbsp;", " "));
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
    for (var i = 0; i < extensions.length; i++) {
        console.log('zzz', extensions[i]);
        for (var j = 0; j < args[divID].length; j++) {
            console.log('args', args[divID][j])
        }
        if (extensions[i] == obj.text) { 
            var postArgs = {name : obj.text, rID : args[divID][0], rTitle : args[divID][1], fileName : fileName, 'check' : 'false', column, column}
            postArgs["divID"] = divID + "-" + obj.text
            postArgs["defaultLinks"] = 2
            $("#" + targetid).html("Loading ...");
            var loadAnimID = setInterval(function() {
                i = ++i % 4;
                $("#" + targetid).html("Loading " + Array(i+1).join("."));
            }, 800);
            $('#' + targetid).load('/extensions', postArgs, function(data){
                 console.log('return', data);
                 if (data == "") {
                     obj.style.display="none"
                 } else {
                      //console.log('zzz', "MathJax.Hub.Queue " + targetid)
                      //MathJax.Hub.Queue(["Typeset", MathJax.Hub, targetid]);
                 }
                 clearInterval(loadAnimID)
                 //target.innerHTML = "";
                 //target.innerHTML = data;
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
}
function appendContent(targetid, id, topic, otherInfo){
    args[targetid] = [id, topic];
    var target=document.getElementById(targetid);
    target.innerHTML = array.join("").replace(/#div/g, targetid).replace(/#topic/g, topic).replace(/#otherInfo/g, otherInfo);
    console.log("xx", reference[id]);

    hidenMetadata(targetid, "reference", "none");
    hidenMetadata(targetid, "content", "none");
    hidenMetadata(targetid, "similar", "none");
    $.post('/extensions', {name : '*', rID : id, fileName : fileName, 'check' : 'true'}, function(data){
        if (data != '') {
            console.log("xx", data)
            var extensions = data.split(" ");
            for (var i = 0; i < extensions.length; i++) {
                hidenMetadata(targetid, extensions[i], "");
            }
        }
    });
   /*
    if (typeof(reference[id]) != "undefined"){
        var referenceDiv = document.getElementById(targetid + "-reference");
        referenceDiv.innerHTML =reference[id];
    } else{
        hidenMetadata(targetid, "reference", "none");
        $('#' + targetid + "-reference").load('/extensions', {name : 'reference', rID : id, fileName : fileName, 'check' : 'true'}, function(data){
           if (data == "true") {
               hidenMetadata(targetid, "reference", "");
           }
        });
        //hidenMetadata(targetid, "reference");
    }
    if (typeof(content[id]) != "undefined"){
        var contentDiv = document.getElementById(targetid + "-content");
        contentDiv.innerHTML = content[id];
    } else{
        hidenMetadata(targetid, "content", "none");
        $('#' + targetid + "-content").load('/extensions', {name : 'content', rID : id, fileName : fileName, 'check' : 'true'}, function(data){
           if (data == "true") {
               hidenMetadata(targetid, "content", "");
           } 
        });
        //hidenMetadata(targetid, "content");
    }*/
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
function appendContentBox(targetid, boxid){
    var target=document.getElementById(targetid);
    var box=document.getElementById(boxid);
    console.log("xx", target);
    target.innerHTML = array.join("").replace(/#div/g, targetid).replace(/#topic/g, box.value.replace(" ", "&nbsp;")).replace(/#otherInfo/g, "");
    hidenMetadata(targetid, "content");
    hidenMetadata(targetid, "reference");
}
