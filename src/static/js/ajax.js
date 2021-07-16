function 帖子点赞() {
    var n=window.name;
    var p=window.number;
    $.ajax(url + '/starpost',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        p,
        }),
    }).done(function(data){
        //成功data=True，否则为False
    })
}
function 帖子点踩() {
    var n=window.name;
    var p=window.number;
    $.ajax(url + '/ustarpost',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        p,
        }),
    }).done(function(data){
        if (!data) {
            //成功data=True，否则为False
        }
    })
}
function 评论点赞(p) { //p为评论序号
    var n=window.name;
    $.ajax(url + '/starcomment',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        p,
        }),
    }).done(function(data){
        //成功data=True，否则为False
    })
}
function 评论点踩(p) { //p为评论序号
    var n=window.name;
    var p=window.number;
    $.ajax(url + '/ustarcomment',{
        async:true,
        type:"POST",
        contentType:"application/json",
        data:JSON.stringify({
        n,
        p,
        }),
    }).done(function(data){
        if (!data) {
            //成功data=True，否则为False
        }
    })
}