var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var theRequest = new Object();
var mo = 1;
var zan = document.getElementById('zan');
var store = document.getElementById('store');
var comment = document.getElementById('comment');
var numLike = document.getElementById('numLike');
var numStore = document.getElementById('numStore');
var numComment = document.getElementById('numComment');

if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
}

gettopics('1');
var int = self.setInterval("listen()", 10000);

$(function() {
    $(document).keydown(function(event) {
        if (event.keyCode == 13) {
            search();
        }
    });
});

function test() {
    console.log('test')
}

function choose1() {
    if (window.now === 2) {
        $("#icon").rotate({ animateTo: 0, duration: 500 });
        var obj = document.getElementsByClassName("postarea");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.setProperty('top', '90%', 'important')
        }
    }
    $("#look_chat").show(500, function() {});
    $("#search").show();
    $("#selfinfo").hide();
    $("#up").hide(500, function() {});
    $("#read").show();
    $("#chat").hide();
    mescroll.showTopBtn();
    window.now = 1;
}

function choose2() {
    $("#look_chat").hide(500, function() {});
    $("#up").show();
    $("#selfinfo").hide(500, function() {});

    $("#icon").rotate({ animateTo: 180, duration: 500 });
    window.label = '其他';
    window.now = 2;
    mescroll.hideTopBtn();
    var obj = document.getElementsByClassName("postarea");
    for (var i = 0; i < obj.length; i++) {
        obj[i].style.setProperty('top', '10%', 'important')
    }
}

function choose3() {
    if (window.now === 2) {
        $("#icon").rotate({ animateTo: 0, duration: 500 });
        var obj = document.getElementsByClassName("postarea");
        for (var i = 0; i < obj.length; i++) {
            obj[i].style.setProperty('top', '90%', 'important')
        }
    }
    mescroll.hideTopBtn();
    $("#look_chat").hide();
    $("#up").hide(500, function() {});
    $("#selfinfo").show(500, function() {});
    document.getElementById("na").innerHTML = window.name;
    window.now = 3;
}

function privatechat() {
    mo = 0;
    $("#chat").show();
    $("#mescroll").animate({ right: '1000px' }).show();
    mescroll.hideTopBtn();
    $("#search").hide();
    getchat();
    $('#ch_li').animate({ left: '0px' }).show();
    document.getElementById("chat").style.setProperty('z-index', '-99', 'important');
}

function look() {
    mo = 1;
    $("#mescroll").animate({ right: '0px' }).show();
    mescroll.hideTopBtn();
    $("#search").show();
    $('#ch_li').animate({ left: '1000px' }).show();
    setTimeout(function() {
        $("#chat").hide();
    }, 750)
}

function quit() {
    window.location.href = './index.html?';
}

function listen() {
    /*var n = window.name;
    $.ajax(url + '/askchat', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function(data) {
        if (data['have_message']) {
            console.log(data['message_count']);
        } else {
            console.log('0');
        }
    })*/
}

function gettopics(w) {
    if (w == 0) {
        var n = window.head;
    } else if (w == 2) {
        var n = window.back;
    } else {
        var n = '0';
    }
    $.ajax(url + '/gettopics', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            w,
            n,
        }),
    }).done(function(data) {
        if (data == false) {
            if (w == 0) {
                alert('没有新帖子发布');
            } else if (w == 2) {
                alert('帖子已经到底了');
            } else {
                alert('获取失败');
            }
        } else {
            var re = document.getElementById("re_li");
            if (w == 1 || w == 2) {
                for (var i = 0; i < data.length; i++) {
                    re.innerHTML = re.innerHTML + '<div class="post" id="' + data[i]['post_id'] + '" onclick="read_topic(' + data[i]['post_id'] + ')"><div class="post_title">' + data[i]['title'] + '</div>' +
                        '<div class="post_some_context">' + data[i]['content'] + '</div>' +
                        '<div class="post_info">' + 
                        '<div id="tag1" style="float: left;display: flex;">' + '<img id="tag" src="./images/tag.png" alt="" class="homeTag">' + '<div class="num">' + data[i]['board'] + '</div>' + '</div>' +
                        '<div id="thumb1" style="float: right;display: flex;">' + '<img id="zan" src="./images/b_Zan.png" alt="" class="homeLike">' + '<div class="num">' + data[i]['like_count'] + '</div>' + '</div>' +
                        '<div id="comment1" style="float: right;display: flex;">' + '<img id="store" src="./images/b_Store1.png" alt="" class="homeStore">' + '<div class="num">' + data[i]['collect_count'] + '</div>' + '</div>' +
                        '<div id="share1" style="float: right;display: flex;">' + '<img id="comment" src="./images/Comment.png" alt="" class="homeComment">' + '<div class="num">' + data[i]['comment_count'] + '</div></div></div></div>';
                }
                if (w == 1) {
                    window.head = data[0]['post_id'].toString();
                }
                window.back = data[i - 1]['post_id'].toString();
            } else if (w == 0) {
                for (var i = data.length - 1; i >= 0; i--) {
                    re.innerHTML = '<div class="post" id="' + data[i]['post_id'] + '" onclick="read_topic(' + data[i]['post_id'] + ')"><div class="post_title">' + data[i]['title'] + '</div>' +
                        '<div class="post_some_context">' + data[i]['content'] + '</div>' +
                        '<div class="post_info"><div id="thumb1" style="float: right;">' + '<img id="zan" src="./images/b_Zan.png" alt="" class="homeLike">' + data[i]['like_count'] + '</div>' +
                        '<div id="comment1" style="float: right;">' + '<img id="store" src="./images/b_Store1.png" alt="" class="homeStore">' + data[i]['collect_count'] + '</div>' +
                        '<div id="share1" style="float: right;">' + '<img id="comment" src="./images/Comment.png" alt="" class="homeComment">' + data[i]['comment_count'] + '</div></div></div>' + re.innerHTML;
                }
                window.head = data[0]['post_id'].toString();
            }
        }
    })
}

function getchat() {
    var n = window.name;
    $.ajax(url + '/getchat', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function(data) {
        var ch = document.getElementById("ch_li");
        ch.innerHTML = "";
        var temp = "";
        const day = new Date();
        for (var i = 0; i < data.length; i++) {
            temp = "";
            temp = '<div class="chatimg">' + '<img src=./images/github.png alt="头像">' + '</div>';
            temp += '<div class="chatpart1"><div class="chatname">' + '匿名用户' + '</div>' +
                '<div class="chatctt">' + data[i]['content'] + '</div></div>';
            var tday = new Date(data[i]['time']);
            if (day.getMonth() == tday.getMonth() && day.getDate() == tday.getDate()) {
                temp += '<div class="chatpart2"><div class="chattime">' + tday.getHours() + ':' + tday.getMinutes() + '</div>';
            } else {
                temp += '<div class="chatpart2"><div class="chattime">' + tday.getMonth() + '-' + tday.getDate() + '</div>';
            }
            if (data[i]['have_message']) {
                temp += '<div class="chatnum">' + data[i]['message_count'] + '</div>';
            }
            temp = '<div class="singlechat" onclick="chat(\'' + data[i]['user_name'] + '\')">' + temp + '</div></div>';
            ch.innerHTML += temp;
        }
    })
}

function uptopic() {
    var n = window.name;
    var t = $('input[id="title"]').val();
    var c = $('textarea[id="content"]').val();
    var l = window.label;
    if (t == "") {
        alert("想一个有趣的标题吧，这样子才会有更多人关注哦！");
    } else if (c == "") {
        alert("你不想说点什么吗？");
    } else {
        $.ajax(url + '/uptopic', {
            async: true,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                n,
                t,
                c,
                l,
            }),
        }).done(function(data) {
            if (data) {
                alert("发送成功");
                $('input[id="title"]').val("");
                $('textarea[id="content"]').val("");
            } else {
                alert("发送失败");
            }
        })
    }
}

function choose_label(i) {
    //document.getElementById(window.label).style.backgroundColor = '#0b9db7';
    //document.getElementById(i).style.backgroundColor = 'yellow';
    document.getElementById(window.label).setAttribute('class', 'tag-blue');
    document.getElementById(i).setAttribute('class', 'tag-green');
    window.label = i;
}

function link(p) {
    var n = window.name;
    $.ajax(url + '/link', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        //点亮点赞，数字加一
    })
}

function win_ch() {
    if (1.4 * document.body.clientWidth > document.body.clientHeight) {
        $(".navbar").hide();
    } else {
        $(".navbar").show();
    }
}