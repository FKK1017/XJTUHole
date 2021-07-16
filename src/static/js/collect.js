var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
}
get_collect();

function quit() {
    window.history.go(-1);
}

function modify() {
    console.log("modifying")

    var obj = document.getElementsByClassName("post_some_context");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.display="none";
    }

    var obj = document.getElementsByClassName("post");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('width', '85%', 'important');
    }

    setTimeout(function () {
        var obj = document.getElementsByClassName("delete");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.display = "flex";
        }
    }, 250);

    var obj = document.getElementsByClassName("cancel");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('background-color', 'red', 'important')
    }
    document.getElementById("modify").style.display = "none"
    document.getElementById("save").style.display = ""
}

function save() {
    document.getElementById("modify").style.display = ""
    document.getElementById("save").style.display = "none"

    setTimeout(function() {
        var obj = document.getElementsByClassName("post_some_context");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.setProperty('display','','important');
        }
    },750);

    
    var obj = document.getElementsByClassName("post");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('width', '95%', 'important');
        // obj[i].style.setProperty('height', '95%', 'important');
    }
    var obj = document.getElementsByClassName("delete");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.display = "none";
    }
    setTimeout(function () {
        var obj = document.getElementsByClassName("cancel");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.setProperty('background-color', 'white', 'important')
        }
    }, 750);
}

function del(p) {
    var n=window.name;
    $.ajax(url + '/ucollectpost',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        p,
        }),
    }).done(function(data){
        if (data) {
            //删除
            var de = document.getElementById(p);
            de.parentNode.removeChild(de);
            var de = document.getElementById(p);
            de.parentNode.removeChild(de);
        }
    })
}

function get_collect() {
    var n=window.name;
    $.ajax(url + '/getusecollect',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        }),
    }).done(function(data){
        if (data == false) {
            var l = document.getElementById("mycollect_li");
            l.innerHTML = '<div class="empty">这里什么都没有找到T^T</div>';
        } else {
            var l = document.getElementById("mycollect_li");
            l.innerHTML = "";
            for (var i = 0; i < data.length; i++) {
                l.innerHTML = '<div class="post" id="' + data[i]['post_id'] + '" onclick="read_topic(' + data[i]['post_id'] + ')"><div class="post_title">'
                + data[i]['title'] + '</div><div class="post_some_context">'
                + data[i]['content'] + '</div><div class="post_info"><div id="thumb1" style="float: right;">点赞 200</div><div id="comment1" style="float: right;">评论 100</div><div id="share1" style="float: right;">转发 100</div></div></div><div class="cancel" id="' + data[i]['post_id'] + '"><div id="' + data[i]['post_id'] + '" class="delete" onclick="del(' + data[i]['post_id'] + ')">删除</div></div>'
                + l.innerHTML;
            }
        }
    })
}

function read_topic(n) {
    window.location.href = './post.html?nickname=' + window.name + '&postnumber=' + n;
}