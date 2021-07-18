var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    strs = str.split("&");
    for (var i = 0; i < strs.length; i++) {
        theRequest[strs[i].split("=")[0]] = (strs[i].split("=")[1]);
    }
    window.name = theRequest['nickname'];
    window.number = theRequest['postnumber'];
}
var comment_nub;
main();
window.onload=function() {
    console.log("running")
    mui('#picture').on('tap', 'li>a', function() {
        mui.alert("你刚点击了\"" + this.innerHTML + "\"按钮");
    //  mui("#picture").popover('toggle');//这是可以用来关闭底部弹窗的事件
    })
}

function del() {
    if (window.name != window.author) {
        alert('您不可以删除该帖哦');
    } else {
        var p = window.number;
        $.ajax(url + '/delpost', {
            async: true,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                p,
            }),
        }).done(function(data) {
            if (data) {
                alert('删除成功');
                quit();
            }
        })
    }
}

function del_comment(n, p) {
    if (window.name != n) {
        alert('您不可以删除该评论哦');
    } else {
        $.ajax(url + '/delcomment', {
            async: true,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                p,
            }),
        }).done(function(data) {
            if (data) {
                alert('删除成功');
                if (comment_nub == 1) {
                    var co = document.getElementById("com");
                    co.innerHTML = '<div class="blank"><p>快来发表你的评论吧</p><img src="./images/sofa.png"></div>';
                } else {
                    var de = document.getElementById(p);
                    de.parentNode.removeChild(de);
                }
                comment_nub -= 1;
            }
        })
    }
}

function main() {
    var na = window.name;
    var nu = window.number;
    $.ajax(url + '/gettopic', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            na,
            nu,
        }),
    }).done(function(data) {
        $("#time").html(data['post_time']);
        $("#title").html(data['title']);
        $("#content").html(data['content']);
        $("#post_img").attr("onclick", "chat('" + data['author_name'] + "')");
		$("#taginfo").html(data['board']);
        var co = document.getElementById("com");
        if (data['collect']) {
            $("#Store").removeClass("StoreF").addClass("StoreT");
        }
        if (data['like']) {
            $('#Like').removeClass("LikeF").addClass("LikeT");
        } else if (data['dislike']) {
            $('#Dislike').removeClass("DislikeF").addClass("DislikeT");
        }
        if (data['comment'].length == 0) {
            co.innerHTML = '<div class="blank"><p>快来发表你的评论吧</p><img src="./images/sofa.png"></div>';
            comment_nub = 0;
        } else {
            var l = data['comment'].length;
            comment_nub = data['comment'].length;
            for (var i = 0; i < l; i++) {
                if (data['comment'][i]['like'] == true) {
                    co.innerHTML = co.innerHTML + ' <li id="' + data['comment'][i]['comment_id'] + '"><div class="comment1"><div class="HeadBar1">' +
                        '<img src="./images/1.jpeg" alt="" onclick=chat("' + data['comment'][i]['author_name'] + '")>' +
                        '<p class="name1" >匿名用户</p>' + '<div class="more"><input type="button" class="three"><ul class="nav-box"><li><input type="button" value="删除" onclick="del_comment(\'' + data['comment'][i]['author_name'] + '\', \'' + data['comment'][i]['comment_id'] + '\')"></li>' +
                        '<li><a href="#picture" class="mui-btn mui-btn-primary">举报</a></li><li><input type="button" value="不感兴趣"></li></ul></div><p class="time1">' + data['comment'][i]['comment_time'] + '</p></div>' +
                        '<div class="BodyBar1"><p class="content1">' + data['comment'][i]['content'] + '</p>' +
                        '<div class="ZanBar"><button class="LikeT" id="Like' + data['comment'][i]['comment_id'] + '"onclick="LikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '<button class="DislikeF" id="Dislike' + data['comment'][i]['comment_id'] + '"onclick="DislikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '</div></div></div></li>';
                } else if (data['comment'][i]['dislike'] == true) {
                    co.innerHTML = co.innerHTML + ' <li id="' + data['comment'][i]['comment_id'] + '"><div class="comment1"><div class="HeadBar1">' +
                        '<img src="./images/1.jpeg" alt="" onclick=chat("' + data['comment'][i]['author_name'] + '")>' +
                        '<p class="name1" >匿名用户</p>' + '<div class="more"><input type="button" class="three"><ul class="nav-box"><li><input type="button" value="删除" onclick="del_comment(\'' + data['comment'][i]['author_name'] + '\', \'' + data['comment'][i]['comment_id'] + '\')"></li>' +
                        '<li><a href="#picture" class="mui-btn mui-btn-primary">举报</a></li><li><input type="button" value="不感兴趣"></li></ul></div><p class="time1">' + data['comment'][i]['comment_time'] + '</p></div>' +
                        '<div class="BodyBar1"><p class="content1">' + data['comment'][i]['content'] + '</p>' +
                        '<div class="ZanBar"><button class="LikeF" id="Like' + data['comment'][i]['comment_id'] + '"onclick="LikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '<button class="DislikeT" id="Dislike' + data['comment'][i]['comment_id'] + '"onclick="DislikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '</div></div></div></li>';
                } else {
                    co.innerHTML = co.innerHTML + ' <li id="' + data['comment'][i]['comment_id'] + '"><div class="comment1"><div class="HeadBar1">' +
                        '<img src="./images/1.jpeg" alt="" onclick=chat("' + data['comment'][i]['author_name'] + '")>' +
                        '<p class="name1" >匿名用户</p>' + '<div class="more"><input type="button" class="three"><ul class="nav-box"><li><input type="button" value="删除" onclick="del_comment(\'' + data['comment'][i]['author_name'] + '\', \'' + data['comment'][i]['comment_id'] + '\')"></li>' +
                        '<li><a href="#picture" class="mui-btn mui-btn-primary">举报</a></li><li><input type="button" value="不感兴趣"></li></ul></div><p class="time1">' + data['comment'][i]['comment_time'] + '</p></div>' +
                        '<div class="BodyBar1"><p class="content1">' + data['comment'][i]['content'] + '</p>' +
                        '<div class="ZanBar"><button class="LikeF" id="Like' + data['comment'][i]['comment_id'] + '" onclick="LikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '<button class="DislikeF" id="Dislike' + data['comment'][i]['comment_id'] + '"onclick="DislikeCmt(' + data['comment'][i]['comment_id'] + ')"></button>' +
                        '</div></div></div></li>';
                }
            }
        }
    })
}

function comment() {
    var c = $('textarea[id="comment1"]').val();
    if (c != '') {
        var na = window.name;
        var nb = window.number;
        $.ajax(url + '/upcomment', {
            async: true,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                c,
                na,
                nb,
            }),
        }).done(function(data) {
            if (data) {
                $('textarea[id="comment1"]').val("")
                var co = document.getElementById("com");
                if (comment_nub == 0) {
                    co.innerHTML = '';
                }
                co.innerHTML = co.innerHTML + ' <li id="' + data['comment_id'] + '"><div class="comment1"><div class="HeadBar1">' +
                    '<img src="./images/1.jpeg" alt="" onclick=chat("' + window.name + '")>' +
                    '<p class="name1">匿名用户</p>' +
                    '<div class="more">' +
                    '<input type="button" class="three">' +
                    '<ul class="nav-box">' +
                    '<li><input type="button" value="删除" onclick="del_comment(\'' + window.name + '\', \'' + data['comment_id'] + '\')"></li>' +
                    '<li><input type="button" value="举报"></li>' +
                    '<li><input type="button" value="不感兴趣"></li>' +
                    '</ul></div>' +
                    '<p class="time1">' + getNewDate() + '</p></div>' +
                    '<div class="BodyBar1"><p class="content1">' +
                    c + '</p>' +
                    '<div class="ZanBar"><button class="LikeF" id="Like' + data['comment_id'] + '" onclick="LikeCmt(' + data['comment_id'] + ')"></button>' +
                    '<button class="DislikeF" id="Dislike' + data['comment_id'] + '"onclick="DislikeCmt(' + data['comment_id'] + ')"></button>' +
                    '</div></div></div></li>';
                comment_nub += 1;
                $(".PingLun").show();
                $(".PingLun1").hide();
            }
        })
    }
}

function Sclick() {
    if ($("#Store").hasClass("StoreF")) {
        collect();
    } else {
        ucollect();
    }
}

function collect() {
    var n = window.name;
    var p = window.number;
    $.ajax(url + '/collectpost', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['collect'] == true) {
            $("#Store").removeClass("StoreF").addClass("StoreT");
        }
    })
}

function ucollect() {
    var n = window.name;
    var p = window.number;
    $.ajax(url + '/ucollectpost', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['collect'] == false) {
            $("#Store").removeClass("StoreT").addClass("StoreF");
        }
    })
}

function Like() {
    var n = window.name;
    var p = window.number;
    if ($('#Dislike').hasClass("DislikeT")) {
        Dislike();
    }
    $.ajax(url + '/starpost', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['like'] == true) {
            $('#Like').removeClass("LikeF").addClass("LikeT");
        } else if (data['like'] == false) {
            $('#Like').removeClass("LikeT").addClass("LikeF");
        }
    })
}

function Dislike() {
    var n = window.name;
    var p = window.number;
    if ($('#Like').hasClass("LikeT")) {
        Like();
    }
    $.ajax(url + '/ustarpost', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['dislike'] == true) {
            $('#Dislike').removeClass("DislikeF").addClass("DislikeT");
        } else if (data['dislike'] == false) {
            $('#Dislike').removeClass("DislikeT").addClass("DislikeF");
        }
    })
}

function LikeCmt(p) {
    var n = window.name;
    var lc = '#Like' + p;
    var dlc = '#Dislike' + p;
    if ($(dlc).hasClass("DislikeT")) {
        DislikeCmt(p);
    }
    $.ajax(url + '/starcomment', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['like'] == true) {
            $(lc).removeClass("LikeF").addClass("LikeT");
        } else if (data['like'] == false) {
            $(lc).removeClass("LikeT").addClass("LikeF");
        }
    })
}

function DislikeCmt(p) {
    var n = window.name;
    var lc = '#Like' + p;
    var dlc = '#Dislike' + p;
    if ($(lc).hasClass("LikeT")) {
        LikeCmt(p);
    }
    $.ajax(url + '/ustarcomment', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            p,
        }),
    }).done(function(data) {
        if (data['dislike'] == true) {
            $(dlc).removeClass("DislikeF").addClass("DislikeT");
        } else if (data['dislike'] == false) {
            $(dlc).removeClass("DislikeT").addClass("DislikeF");
        }
    })
}

function getNewDate() {
    var date = new Date();
    var transverse = "-";
    var Verticalpoint = ":";
    var month = date.getMonth() + 1; //获取月份
    var strDate = date.getDate(); //获取具体的日期           
    var strHour = date.getHours(); //获取...钟点
    var strMinute = date.getMinutes(); //获取分钟数
    var strSeconde = date.getSeconds(); //获取秒钟数
    //判断获取月份 、 具体的日期 、...钟点、分钟数、秒钟数 是否在1~9
    //如果是则在前面加“0”
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 1 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    if (strHour >= 1 && strHour <= 9) {
        strHour = "0" + strHour
    }
    if (strMinute >= 1 && strMinute <= 9) {
        strMinute = "0" + strMinute;
    }

    if (strSeconde >= 1 && strSeconde <= 9) {
        strSeconde = "0" + strSeconde;
    }
    //时间日期字符串拼接
    var NewDate = date.getFullYear() + transverse + month + transverse + strDate + " " +
        strHour + Verticalpoint + strMinute + Verticalpoint + strSeconde;
    //返回拼接字符串
    return NewDate;
}

function createEvent(type) {
    var event;

    try {
        event = new Event(type);
    } catch (e) {
        event = doc.createEvent("Events");
        event.initEvent(type, true, true);
    }

    return event;
}
function comment_win() {
    $(".PingLun").hide();
    $(".PingLun1").show();
}