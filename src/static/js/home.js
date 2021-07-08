var url = 'http://111.229.120.197:8080';
var u = location.search;
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
    //gettopics('1', '0');
    var int = self.setInterval("listen()", 10000);
}

function choose1() {
    $("#look_chat").show();
    $("#selfinfo").hide();
    $("#up").hide();
    $("#read").show();
    $("#chat").hide();
}

function choose2() {
    $("#look_chat").hide();
    $("#up").show();
    $("#selfinfo").hide();
}

function choose3() {
    $("#look_chat").hide();
    $("#up").hide();
    $("#selfinfo").show();
}

function privatechat() {
    $("#read").hide();
    $("#chat").show();
    //getchat();
}

function look() {
    $("#read").show();
    $("#chat").hide();
}

function quit() {
    window.history.go(-1);
}

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
            console.log(data['message_count']);
        } else {
            console.log('0');
        }
    })
}

function gettopics(w, n) {
    $.ajax(url + '/gettopics', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            w,
            n,
        }),
    }).done(function (data) {
        if (data == false) {
            alert('获取失败');
        } else {
            if (w == '1') {
                var re = document.getElementById("re_li");
                for (var i = 0; i < data.length; i++) {
                    re.innerHTML = re.innerHTML + '<li class="topic">' + data[i]['title'] + '</li>';
                    re.innerHTML = re.innerHTML + '<li class="content">' + data[i]['content'] + '</li>';
                }
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
    }).done(function (data) {
        var ch = document.getElementById("ch_li");
        ch.innerHTML = "";
        for (var i = 0; i < data.length; i++) {
            alert(data[i]['user_name']);
            ch.innerHTML = ch.innerHTML + '<li>' + data[i]['user_name'] + '</li>';
            ch.innerHTML = ch.innerHTML + '<li>' + data[i]['time'] + '</li>';
            ch.innerHTML = ch.innerHTML + '<li>' + data[i]['content'] + '</li>';
            if (data[i]['have_message']) {
                ch.innerHTML = ch.innerHTML + '<li>' + '您有' + data[i]['message_count'] + '条新消息！' + '</li>';
            }
        }
    })
}

function uptopic() {
    var n = window.name;
    var t = $('input[id="title"]').val();
    var c = $('textarea[id="content"]').val();
    $.ajax(url + '/uptopic', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            t,
            c,
        }),
    }).done(function (data) {
        if (data) {
            alert("发送成功");
        }
    })
}

function read_topic(n) {
    window.location.href = './post.html?nickname=' + window.name + '&postnumber=' + n;
}

function chat() {
    window.location.href = './chatveiw.html?nickname=' + window.name;
}