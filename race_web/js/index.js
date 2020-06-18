
// 显示隐藏比赛
$(".race-title .layui-icon").on("click", function () {
    if( $(this).hasClass("layui-icon-down") ){ // 显示状态
        $(this).removeClass("layui-icon-down").addClass("layui-icon-up");
    }else{
        $(this).removeClass("layui-icon-up").addClass("layui-icon-down");
    }
    $(this).parent().nextAll().slideToggle();
});

// 点击选择比分
$("td").not(".more, .layui-bg").on("click", function () {
    $(this).toggleClass("layui-bg-red");
});

// 显示筛选
$(".choose-race .layui-header-filter").on("click", function () {
    $(".filter-race").removeClass("layui-hide");
    $(".grey-bg").removeClass("layui-hide");
});

// 点击筛选赛事 / 选关
$(".filter .match div, .choose-guan .guan div").on("click", function () {
    $(this).toggleClass("layui-bg-red");
});

// 全选
$(".check-all").on("click", function () {
    $(".match-title").addClass("layui-bg-red");
});

// 反选
$(".check-fan").on("click", function () {
    $(".match-title").toggleClass("layui-bg-red");
});

// 确定
$(".filter .confirm .submit").on("click", function () {
    $(".filter").addClass("layui-hide");
    $(".grey-bg").addClass("layui-hide");
    layer.open({
        content: '确定筛选'
        ,skin: 'msg'
        ,time: 2
    });
});

// 取消
$(".confirm .cancel").on("click", function () {
    $(".fixed").addClass("layui-hide");
    $(".grey-bg").addClass("layui-hide");
});


// 更多选项
$(".more").on("click", function () {
    $(".more-check").removeClass("layui-hide");
    $(".grey-bg").removeClass("layui-hide");
})
// 确定
$(".more-check .confirm .submit").on("click", function () {
    $(".more-check").addClass("layui-hide");
    $(".grey-bg").addClass("layui-hide");
    layer.open({
        content: '确定选择'
        ,skin: 'msg'
        ,time: 2
    });
});

// 取消
$(".more-check .confirm .cancel").on("click", function () {
    $(".more-check").addClass("layui-hide");
    $(".grey-bg").addClass("layui-hide");
});


// 投注
$(".touzhu").on("click", function () {
    $(".choose-race").addClass("layui-hide");
    $(".choose-result").removeClass("layui-hide");
})

// 投注列表返回 / 添加赛事
$(".choose-result .layui-header-back, .choose-result .oprate .layui-btn-normal").on("click", function () {
    $(".choose-race").removeClass("layui-hide");
    $(".choose-result").addClass("layui-hide");
})

// 清空重选
$(".choose-result .oprate .layui-btn-warm").on("click", function () {
    layer.open({
        content: '确认清空全部赛事重新选择？'
        ,btn: ['确认', '取消']
        ,yes: function () {

            layer.open({
                content: '确定选择'
                ,skin: 'msg'
                ,time: 2
            });
        }
    });
})


// 选择过关
$(".guanbei .guan").on("click", function () {
    $(".choose-guan").removeClass("layui-hide");
    $(".grey-bg").removeClass("layui-hide");
});

// 确定
$(".choose-guan .confirm .submit").on("click", function () {
    $(".fixed").addClass("layui-hide");
    $(".grey-bg").addClass("layui-hide");
    layer.open({
        content: '确定选择'
        ,skin: 'msg'
        ,time: 2
    });
});


// 倍数选择
// 减
$(".bei-oprate .jian").on("click", function () {
    var bei = $(".bei").text();
    bei--;
    bei > 0 && $(".bei").text( bei );
});

// 加
$(".bei-oprate .jia").on("click", function () {
    var bei = $(".bei").text();
    bei++;
    bei < 1000 && $(".bei").text( bei );
});

$(".bei").on("click", function () {
    $(".number").removeClass("layui-hide");
    $(".grey-bg").removeClass("layui-hide");
});

// 倍数选择
$(".number-list div").not(".clear-number, .backspace-number").on("click", function () {
    let number = $(".number-result").text();
    let result = number + $(this).text();
    $(".number-result").text( result );
})
// 倍数选择退格
$(".number-list .backspace-number").on("click", function () {
    let number = $(".number-result").text();
    let result = number.substr(0, number.length - 1);
    $(".number-result").text( result );
})
// 倍数选择清空
$(".number-list .clear-number").on("click", function () {
    $(".number-result").text( '' );
})
// 倍数选择确定
$(".number .submit").on("click", function () {
    let number = parseInt($(".number-result").text());
    if( isNaN(number) ){
        layer.open({
            content: '请选择倍数'
            ,skin: 'msg'
            ,time: 2
        });
    }else if( number == 0 ){
        layer.open({
            content: '倍数最少1倍'
            ,skin: 'msg'
            ,time: 2
        });
    }else if( number > 999 ){
        layer.open({
            content: '倍数最多999倍'
            ,skin: 'msg'
            ,time: 2
        });
    }else{
        $(".bei").text( number );
        $(".fixed").addClass("layui-hide");
        $(".grey-bg").addClass("layui-hide");
    }
})