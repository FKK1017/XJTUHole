document.addEventListener("plusready", function() {
    // 注册返回按键事件
    plus.key.addEventListener('backbutton', function() {
        window.history.go(-1);
    }, false);
});
var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var key_word;
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
    key_word = strs[2];
}

$.ajax(url + '/search', {
    async: true,
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
        key_word
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

function read_topic(n) {
    window.location.href = './post.html?nickname=' + window.name + '&postnumber=' + n;
}