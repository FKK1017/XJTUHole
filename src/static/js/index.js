url = 'http://111.229.120.197:8080';
function register_login() {
    $('input[id="username"]').val("");
    $('input[id="password"]').val("");
    $('input[id="re_password"]').val("");
    $('input[id="nickname"]').val("");
    $('tr[id="re"]').addClass("hidden");
    $("#reg").hide();
    $("#log").show();
}
function login_register() {
    $('input[id="username"]').val("");
    $('input[id="password"]').val("");
    $('tr[id="re"]').removeClass("hidden");
    $("#reg").show();
    $("#log").hide();
}
function login() {
    var u = $('input[id="username"]').val();
    var p = $('input[id="password"]').val();
    if (u == "") {
        alert("用户名不能为空");
    }
    else if (p == "") {
        alert("密码不能为空");
    }
    else {
        $.ajax(url + '/login?user=' + u + '&passwd=' + p, {
            async: true,
            type: "GET",
            contentType: "application/json",
        }).done(function (data) {
            if (data['status']) {
                alert("登陆成功!欢迎你，" + data['name']);
                window.location.href = './home.html?nickname=' + data['name'];
            }
            else {
                alert("用户名或密码错误");
            }
        })
    }
}
function register() {
    var u = $('input[id="username"]').val();
    var p = $('input[id="password"]').val();
    var rp = $('input[id="re_password"]').val();
    var n = $('input[id="nickname"]').val();
    if (u == "") {
        alert("用户名不能为空");
    }
    else if (p == "") {
        alert("密码不能为空");
    }
    else if (rp == "") {
        alert("确认密码不能为空");
    }
    else if (n == "") {
        alert("昵称不能为空");
    }
    else if (p != rp) {
        alert("密码与确认密码不同");
    }
    else {
        $.ajax(url + '/register?user=' + u + '&passwd=' + p + '&name=' + n, {
            async: true,
            type: "GET",
            contentType: "application/json",
        }).done(function (data) {
            alert("注册成功，请继续登陆!")
            register_login();
        })
    }
}