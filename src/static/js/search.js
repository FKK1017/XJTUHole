var labels = ['hot', '学习', '情感', '游戏', '运动', '吐槽', '求助', '整活', '其他'];
var url = 'http://111.229.120.197:8080';
window.label = labels[0];
window.lastindex = [0, 0, 0, 0, 0, 0, 0, 0, 0];
window.onload = function() {
    var w = $("#header").width();
    var tabsSwiper = new Swiper('#tabs-container', {
        on: {
            slideChangeTransitionStart: function() {
                var i = this.activeIndex;
                //console.log(w * 0.07 * i);
                $('#header').animate({ scrollLeft: w * 0.08 * i }, 500);
                //console.log(i);
                $('.item-active').removeClass('item-active')
                $('#item' + i).addClass('item-active');
                window.label = labels[i];
                gettopics(1, i);
            }
        }
    });

    $(".list li").on('click', function(e) {
        e.preventDefault();
        tabsSwiper.slideTo(Number(this.id[4]));
    })

}

$(function() {
    $(document).keydown(function(event) {
        if (event.keyCode == 13) {
            search();
        }
    });
});

gettopics(1, 0);

function quit() {
    window.history.go(-1);
}

function search() {
    window.location.href = './search_result.html?nickname=' + window.name + '&key_word=' + $("#search").val();
}

function read_topic(n) {
    window.location.href = './post.html?nickname=' + window.name + '&postnumber=' + n;
}

function gettopics(w, p) {
    if (w == 1) {
        window.lastindex[p] = '0';
    }
    var n = window.lastindex[p];
    var l = window.label;
    $.ajax(url + '/hottopic', {
        async: true,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            w,
            n,
            l
        }),
    }).done(function(data) {
        if (data == false) {
            if (w == 2) {
                alert('帖子已经到底了');
            } else {
                alert('获取失败');
            }
        } else {
            let temp = document.getElementById(l);
            if (w === 1) {
                temp.innerHTML = '';
            }
            if (l === 'hot') {
                var thtml = '';
                for (var i = 0; i < data['ret'].length; i++) {
                    thtml = '<div class="hot" id="' + data['ret'][i]['post_id'] + '" onclick="read_topic(' + data['ret'][i]['post_id'] + ')">' +
                        '<div id="hot_num">' + (i + Number(window.lastindex[p]) + 1) + '</div>' +
                        '<div class="hot_title">' + data['ret'][i]['title'] + '</div>' +
                        '<img id="fire" src="./images/hot.png">' +
                        '<p id="hot_degree">' + data['ret'][i]['browse_count'] + '万热度</p>' +
                        '</div>';
                    temp.innerHTML += thtml;
                }
                window.lastindex[p] = data['next_post_index'];
            } else {
                for (var i = 0; i < data.length; i++) {
                    temp.innerHTML = temp.innerHTML + '<div class="post" id="' + data[i]['post_id'] + '" onclick="read_topic(' + data[i]['post_id'] + ')"><div class="post_title">' + data[i]['title'] + '</div>' +
                        '<div class="post_some_context">' + data[i]['content'] + '</div>' +
                        '<div class="post_info"><div id="thumb1" style="float: right;display: flex;">' + '<img id="zan" src="./images/b_Zan.png" alt="" class="homeLike">' + '<div class="num">' + data[i]['like_count'] + '</div>' + '</div>' +
                        '<div id="comment1" style="float: right;display: flex;">' + '<img id="store" src="./images/b_Store1.png" alt="" class="homeStore">' + '<div class="num">' + data[i]['collect_count'] + '</div>' + '</div>' +
                        '<div id="share1" style="float: right;display: flex;">' + '<img id="comment" src="./images/Comment.png" alt="" class="homeComment">' + '<div class="num">' + data[i]['comment_count'] + '</div></div></div></div>';
                }
                window.lastindex[p] = data[i - 1]['post_id'].toString();
            }
        }
    })
}