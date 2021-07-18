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
    window.who = theRequest['who'];
}
get_chat(1);
var int = self.setInterval("listen()", 10000);

function listen() {
    var n = window.name;
    $.ajax(url + '/askchat', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function (data) {
        if (data['have_message']) {
            get_chat(2);
        }
    })
}

function get_chat(wa)
{
    var n=window.name;
    var w=window.who;
    if (wa == 0) {
        c = window.num;
    } else {
        c = '0';
    }
    $.ajax(url + '/lookchat',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        w,
        wa,
        c,
        }),
    }).done(function(data){
        if (data == false) {
            if (wa == 1) {
                var ma = document.getElementById("mescroll");
                ma.innerHTML = '<div class="msgem"><p>还没跟对方发过消息呐，快来聊一聊吧</p><img src="./images/chat.png"></div>' + ma.innerHTML;
            }
            else if (wa == 0) {
                alert('没有更多消息了');
            } else {
                alert('获取失败');
            }
        } else {
            var ma = document.getElementById("msglist");
            if (wa == 1 || wa == 2) {
                for (var i = data.length-1; i >= 0; i--) {
                    if (data[i]['sender']) {
                        ma.innerHTML = ma.innerHTML + '<li class="rightmsg"><div class="rightwithtime"><div class="rightmsgtime">'
                        + data[i]['time'] + '</div><div class="chat_right">'
                        + data[i]['content'] + '</div></div><img src="./images/user.png" alt="用户头像" class="rightimg"></li><li><br><br></li>';
                    } else {
                        ma.innerHTML = ma.innerHTML + '<li class="leftmsg"><img src="./images/momo.png" alt="对方头像" class="leftimg"><div class="leftwithtime"><div class="leftmsgtime">'
                        + data[i]['time'] + '</div><div class="chat_left">'
                        + data[i]['content'] + '</div></div></li><li><br><br></li>';
                    }
                }
                window.num = data[data.length-1]['message_id'].toString();
            }
            else if (wa == 0) {
                for (var i = 0; i <data.length; i++) {
                    if (data[i]['sender']) {
                        ma.innerHTML = '<li class="rightmsg"><div class="rightwithtime"><div class="rightmsgtime">'
                        + data[i]['time'] + '</div><div class="chat_right">'
                        + data[i]['content'] + '</div></div><img src="./images/user.png" alt="用户头像" class="rightimg"></li><li><br><br></li>'
                        + ma.innerHTML;
                    } else {
                        ma.innerHTML = '<li class="leftmsg"><img src="./images/momo.png" alt="对方头像" class="leftimg"><div class="leftwithtime"><div class="leftmsgtime">'
                        + data[i]['time'] + '</div><div class="chat_left">'
                        + data[i]['content'] + '</div></div></li><li><br><br></li>'
                        + ma.innerHTML;
                    }
                }
                window.num = data[data.length-1]['message_id'].toString();
            }
        }
    })
}

function getNewDate() {
    var date = new Date();
    var transverse = "-";
    var Verticalpoint = ":";
    var month = date.getMonth() + 1;//获取月份
    var strDate = date.getDate();//获取具体的日期           
    var strHour = date.getHours();//获取...钟点
    var strMinute = date.getMinutes();//获取分钟数
    var strSeconde = date.getSeconds();//获取秒钟数
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

function send_chat()
{
    var n=window.name;
    var w=window.who;
    var c=$('textarea[id="message"]').val();
    if (c == "")
    {
        alert("消息不可为空");
    } else {
        $.ajax(url + '/chat',{
            async:true,
            type:"POST",
            contentType:"application/json",
            data:JSON.stringify({
            n,
            w,
            c,
            }),
        }).done(function(data){
            if (data) {
                var ma = document.getElementById("msglist");
                ma.innerHTML = ma.innerHTML + '<li class="rightmsg"><div class="rightwithtime"><div class="rightmsgtime">'
                + getNewDate() + '</div><div class="chat_right">'
                + c + '</div></div><img src="./images/user.png" alt="用户头像" class="rightimg"></li><li><br><br></li>';
                $('textarea[id="message"]').val("")
            } else {
                alert('发送失败！');
            }
        })
    }
}
