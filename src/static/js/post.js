
var u = location.search;
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    str = str.split("=").split("&");
    window.name = strs[1];
    window.number = strs[3];
    main()
}
function main() {
    var n = window.number;
    $.ajax(url + '/gettopic', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function (data) {
        var t = document.getElementById("title");
        t.innerHTML = data['title'];
        var c = document.getElementById("content");
        c.innerHTML = data['content'];
        /*document.getElementById("content3").value = data['title'] + '\n';
        document.getElementById("content3").value = document.getElementById("content3").value + data['content'] + '\n';
        document.getElementById("content3").value = document.getElementById("content3").value + data['browse_count'] + '\n';
        document.getElementById("content3").value = document.getElementById("content3").value + data['post_time'] + '\n';
        document.getElementById("content3").value = document.getElementById("content3").value + data['author_name'] + '\n';*/
        var com = document.getElementById("comment");
        for (var i = 0; i < data['comment'].length; i++) {
            document.getElementById("content3").value = document.getElementById("content3").value + data['comment'][i]['content'] + '\n';
        }
    })
}