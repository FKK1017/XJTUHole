var url = 'http://111.229.120.197:8080';
var u = decodeURI(location.search);
var theRequest = new Object();
if (u.indexOf("?") != -1) {
    var str = u.substr(1);
    var strs = str.split("=");
    window.name = strs[1];
}
get_info();

function update() {
    document.getElementById("sex_choose").disabled = "";
    document.getElementById("briefintro").disabled = "";
    //document.getElementById("mypwd").disabled = "";
    document.getElementById("save").style.display = "";
    document.getElementById("update").style.display = "none";

    //修改密码部分
    //document.getElementById("oldpwd").innerHTML = "原密码";
    //document.getElementById("mypwd").value = "";

    //document.getElementById("newpwd").style.display = "";
    //document.getElementById("newpwd_input").style.display = "";

    //document.getElementById("renewpwd").style.display = "";
    //document.getElementById("renewpwd_input").style.display = "";

    document.getElementById("nochange").style.display = "none";

    document.getElementById("username").disabled = "";

    document.getElementById("cancel").style.display = "";

}

function save() {
    alter_info();
    //document.getElementById("mypwd").disabled = "disabled";
    document.getElementById("sex_choose").disabled = "disabled";
    document.getElementById("briefintro").disabled = "disabled";
    document.getElementById("save").style.display = "none";
    document.getElementById("update").style.display = "";

    //修改密码部分

    //document.getElementById("input2").value = "";
    //document.getElementById("input3").value = "";

    //document.getElementById("oldpwd").innerHTML = "用户密码";
    //document.getElementById("mypwd").value = "******";

    //document.getElementById("newpwd").style.display = "none";
    //document.getElementById("newpwd_input").style.display = "none";

    //document.getElementById("renewpwd").style.display = "none";
    //document.getElementById("renewpwd_input").style.display = "none";

    document.getElementById("nochange").style.display = "";
    
    document.getElementById("username").disabled = "disabled";
    document.getElementById("cancel").style.display = "none";
}

function cancel() {
    //按下取消放弃所有更改，并退出编辑模式
    //原来的所有参数应该在页面参数中保存着，所以直接用参数赋值即可

    //目前这里只实现了退出编辑模式，放弃更改后面再改
    //document.getElementById("mypwd").disabled = "disabled";
    document.getElementById("sex_choose").disabled = "disabled";
    document.getElementById("briefintro").disabled = "disabled";
    document.getElementById("save").style.display = "none";
    document.getElementById("update").style.display = "";

    //修改密码部分

    //document.getElementById("input2").value = "";
    //document.getElementById("input3").value = "";

    //document.getElementById("oldpwd").innerHTML = "用户密码";
    //document.getElementById("mypwd").value = "******";

    //document.getElementById("newpwd").style.display = "none";
    //document.getElementById("newpwd_input").style.display = "none";

    //document.getElementById("renewpwd").style.display = "none";
    //document.getElementById("renewpwd_input").style.display = "none";

    document.getElementById("nochange").style.display = "";

    document.getElementById("username").disabled = "disabled";
    document.getElementById("cancel").style.display = "none";
}

function get_info() {
    var n = window.name;
    $.ajax(url + '/getinfo', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
        }),
    }).done(function (data) {
        $('input[id="username"]').val(n)
        var k = document.getElementById("num_of_post");
        k.innerHTML = data['post_count'];
        var v = document.getElementById("reg_time");
        v.innerHTML = data['register_date'];
        var l = document.getElementById("briefintro");
        l.innerHTML = data['introduction'];
        var se = document.getElementById("sex_choose");
        se.innerHTML = '<option value="保密">保密</option><option value="女">女</option><option value="男">男</option>';
        var s = $("#sex_choose option");
        for (i = s.length - 1; i >= 0; i--) {
            if (data['sex'] == s[i].value) {
                s[i].selected = true;
            }
        }
    })
}

function alter_info() {
    var n = window.name;
    var nn = $('input[id="username"]').val();
    var s = $("#sex_choose option:selected").val();
    var i = $('textarea[id="briefintro"]').val();
    $.ajax(url + '/reinfo', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            n,
            nn,
            s,
            i,
        }),
    }).done(function (data) {
        window.name = nn;
        alert("修改成功");
    })
}