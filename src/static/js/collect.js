var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
}
get_collect();

function modify() {
    console.log("modifying")

    var obj = document.getElementsByClassName("post_some_context");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.display = "none";
    }

    var obj = document.getElementsByClassName("post");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('width', '85%', 'important');
    }

    setTimeout(function() {
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
            obj[i].style.setProperty('display', '', 'important');
        }
    }, 750);


    var obj = document.getElementsByClassName("post");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('width', '95%', 'important');
        // obj[i].style.setProperty('height', '95%', 'important');
    }
    var obj = document.getElementsByClassName("delete");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.display = "none";
    }
    setTimeout(function() {
        var obj = document.getElementsByClassName("cancel");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.setProperty('background-color', 'white', 'important')
        }
    }, 750);
}

function del(p) {
    var n = window.name;
    $.ajax(url + '/ucollectpost', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
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
    var n = window.name;
    $.ajax(url + '/getusecollect', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function(data) {
        if (data == false) {
            var l = document.getElementById("mycollect_li");
            l.innerHTML = '<div class="empty">这里什么都没有找到T^T</div>';
        } else {
            var l = document.getElementById("mycollect_li");
            l.innerHTML = "";
            for (var i = 0; i < data.length; i++) {
                l.innerHTML = l.innerHTML + '<div class="post" id="' + data[i]['post_id'] + '" onclick="read_topic(' + data[i]['post_id'] + ')"><div class="post_title">' +
                    data[i]['title'] + '</div><div class="post_some_context">' +
                    data[i]['content'] + '</div>' +
                    '<div class="post_info"><div id="thumb1" style="float: right;display: flex;">' + '<img id="zan" src="./images/b_Zan.png" alt="" class="homeLike">' + '<div class="num">' + data[i]['like_count'] + '</div>' + '</div>' +
                    '<div id="comment1" style="float: right;display: flex;">' + '<img id="store" src="./images/b_Store1.png" alt="" class="homeStore">' + '<div class="num">' + data[i]['collect_count'] + '</div>' + '</div>' +
                    '<div id="share1" style="float: right;display: flex;">' + '<img id="comment" src="./images/Comment.png" alt="" class="homeComment">' + '<div class="num">' + data[i]['comment_count'] + '</div></div></div></div>' +
                    '<div class="cancel" id="' + data[i]['post_id'] + '"><div id="' + data[i]['post_id'] + '" class="delete" onclick="del(' + data[i]['post_id'] + ')">删除</div></div>'
            }
        }
    })
}