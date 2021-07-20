var url = 'http://111.229.120.197:8080';
var rw;
var rrid;
var rnu;
window.onload = function() {
    console.log("running")
    mui('#picture').on('tap', 'li>a', function() {
        //mui.alert("你刚点击了\"" + this.innerHTML + "\"按钮");
        let r;
        if (this.innerHTML == '删除') {
            r = 0;
        } else if (this.innerHTML != '取消') {
            r = 1;
        }
        handle(r);
        mui("#picture").popover('toggle'); //这是可以用来关闭底部弹窗的事件
    })
}

function main() {
    let n = window.name;
    $.ajax(url + '/getreports', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function(data) {
        let temp = document.getElementById("tohandle");
        temp.innerHTML = '';
        let t = '';
        for (let i = 0; i < data.length; i++) {
            if (data[i]['type'] == 'post') {
                t = '<div class="to_admin">' +
                    '<div class="tag">举报类型:贴子</div>' +
                    '<div class="post">' +
                    '<div class="post_title">' + data[i]['title'] + '</div>' +
                    '<div class="post_some_context">' + data[i]['content'] + '</div>' +
                    '</div>' +
                    '<div class="info">' +
                    '<div class="uper" id="pst' + data[i]['post_id'] + '-rid" name="' + data[i]['reporter_id'] + '">举报人:' + data[i]['reporter_name'] + '</div>' +
                    '<div class="reason">举报原因:' + data[i]['report_reason'] + '</div>' +
                    '</div>' +
                    '<div class="opt" id="pst' + data[i]['post_id'] + '">' +
                    '<a href="#picture" class="mui-btn mui-btn-primary " style="' +
                    'font-size: 3em;' +
                    'background-color: transparent;' +
                    'border: none;' +
                    'color: red;">处理</a>' +
                    '</div>' +
                    '</div>'
            } else {
                t = '<div class="to_admin">' +
                    '<div class="tag">举报类型:评论</div>' +
                    '<div class="post">' +
                    '<div class="HeadBar">' +
                    '<p class="name">匿名用户</p>' +
                    '<p class="time">' + data[i]['comment_time'] + '</p>' +
                    '</div>' +
                    '<div class="BodyBar">' +
                    '<p class="content">' + data[i]['content'] + '</p>' +
                    '</div>' +
                    '</div>' +
                    '<div class="info">' +
                    '<div class="uper" id="cmt' + data[i]['comment_id'] + '-rid" name="' + data[i]['reporter_id'] + '">举报人:' + data[i]['reporter_name'] + '</div>' +
                    '<div class="reason">举报原因:' + data[i]['report_reason'] + '</div>' +
                    '</div>' +
                    '<div class="opt" id="cmt' + data[i]['comment_id'] + '">' +
                    '<a href="#picture" class="mui-btn mui-btn-primary " style="' +
                    'font-size: 3em;' +
                    'background-color: transparent;' +
                    'border: none;' +
                    'color: red;">处理</a>' +
                    '</div>' +
                    '</div>'
            }
            temp.innerHTML += t;
        }
        bind();
    })
}

function bind() {
    mui('.opt').off('tap', 'a', bbind);
    mui('.opt').on('tap', 'a', bbind);
}

function bbind() {
    let t = this.parentNode.id
    console.log($('#' + t + '-rid').attr('name'));
    if (t.startsWith('pst')) {
        rw = 'post';
    } else {
        rw = 'comment';
    }
    rnu = t.split('t')[1];
    rrid = $('#' + t + '-rid').attr('name');
}

function handle(r) {
    let n = window.name;
    let w = rw;
    let r_id = rrid;
    let nu = rnu;
    $.ajax(url + '/handlereport', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            w,
            nu,
            r,
            r_id
        }),
    }).done(function(data) {
        alert(data);
        main();
    })
}

main();