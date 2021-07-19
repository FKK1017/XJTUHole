window.onload = function() {
    console.log("running")
    mui('#picture').on('tap', 'li>a', function() {
        mui.alert("你刚点击了\"" + this.innerHTML + "\"按钮");
        //  mui("#picture").popover('toggle');//这是可以用来关闭底部弹窗的事件
    })

    mui('.opt').on('tap', 'a', function() {
        console.log(this.parentNode.parentNode);
    })
}