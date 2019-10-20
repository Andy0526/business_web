/**
 * Created by Administrator on 2016/4/20.
 */
// 数据缓存
var data_info;
// 替换字符串
function replace_data_info() {
    for (var i = 0; i < data_info.length; ++i) { // 逐个替换
        var info = data_info[i];
        if (info.rank == 0) {
            info.rank = "";
        }
    }

    // 去除无用数据
    data_info.sort(
        function (d1, d2) {
            if (d1.rank.length == 0)
                return 1;
            if (d2.rank.length == 0)
                return -1;
            return (d1.rank - d2.rank) * 1;
        }
    );
    var show_num = 100;
    t_data_info = []
    for (var i = 0; i < show_num; ++i) {
        t_data_info.push(data_info[i]);
    }
    data_info = t_data_info;
}
// 显示信息
function show_info() {
    var rank_num = 5;
    platform_sort('' +
        '', '1');
    for (var i = 0; i < rank_num; ++i) { // 逐个渲染
        var info = data_info[i];
        $("#rank_platform_index").append(
            "<a href= '/detail/platform/" + info.platform_name + "' target='_blank' class='list-group-item'>" + info.platform_name + "(" + info.rank + ")" + "</a>"
        );
    }

    platform_sort('平均收益', '-1');
    for (var i = 0; i < rank_num; ++i) { // 逐个渲染
        var info = data_info[i];
        $("#rank_platform_earn").append(
            "<a href= '/detail/platform/" + info.platform_name + "' target='_blank' class='list-group-item'>" + info.platform_name + "(" + info.platEarnings + ")" + "</a>"
        );
    }

    platform_sort('注册资本', '-1');
    for (var i = 0; i < rank_num; ++i) { // 逐个渲染
        var info = data_info[i];
        $("#rank_platform_volume").append(
            "<a href= '/detail/platform/" + info.platform_name + "' target='_blank' class='list-group-item'>" + info.platform_name + "(" + info.registeredCapital + "万)" + "</a>"
        );
    }

    platform_sort('上线时间', '1');
    for (var i = 0; i < rank_num; ++i) { // 逐个渲染
        var info = data_info[i];
        var time_strs = info.onlineDate.split("-")
        $("#rank_platform_time").append(
            "<a href= '/detail/platform/" + info.platform_name + "' target='_blank' class='list-group-item'>" + info.platform_name + "(" + info.onlineDate + ")" + "</a>"
        );
    }


}


// 进行排序
function platform_sort(tag, updown) {
    if (tag == '综合排名') {
        data_info.sort(
            function (d1, d2) {
                if (d1.rank.length == 0)
                    return 1;
                if (d2.rank.length == 0)
                    return -1;
                return (d1.rank - d2.rank) * updown;
            }
        );
    } else if (tag == '平均收益') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platEarnings.length == 0)
                    return 1;
                if (d2.platEarnings.length == 0)
                    return -1;
                return (d1.platEarnings - d2.platEarnings) * updown;
            }
        );
    } else if (tag == '上线时间') {
        data_info.sort(
            function (d1, d2) {
                if (d1.onlineDate.length == 0)
                    return 1;
                if (d2.onlineDate.length == 0)
                    return -1;
                str1 = d1.onlineDate.replace(/-/g, "/");
                str2 = d2.onlineDate.replace(/-/g, "/");
                var date1 = new Date(str1);
                var date2 = new Date(str2);
                var value = 1;
                if (date1 < date2)
                    value = -1;
                return value * updown;

            }
        );
    } else if (tag == "平均利率") {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_rate.length == 0)
                    return 1;
                if (d2.platform_rate.length == 0)
                    return -1;
                var r1 = d1.platform_rate.substr(0, d1.platform_rate.length - 1); // 获取子字符串
                var r2 = d2.platform_rate.substr(0, d2.platform_rate.length - 1); // 获取子字符串
                return (parseFloat(r1) - parseFloat(r2)) * updown;
            }
        );
    } else if (tag == "注册资本") {
        data_info.sort(
            function (d1, d2) {
                return (d1.registeredCapital - d2.registeredCapital) * updown;
            }
        );
    }
    return;
}

// 加载数据
$(document).ready(function () {
    $.getJSON("/detail/platforms", function (data) {
        data_info = data.platforms;
        // 整理数据
        replace_data_info();
        // 显示信息
        show_info();

    });
});


var data_info;
// 加载数据
$(document).ready(function () {
    $.getJSON("/detail/platforms", function (data) {
        data_info = data.platforms;
    });
});

var isFirst = true;

$("#submit_btn").click(function () {

    var basic_age = parseInt($("[name='basic_age']:checked").val());
    var basic_occupation = parseInt($("[name='basic_occupation']:checked").val());
    var basic_family = parseInt($("[name='basic_family']:checked").val());
    var basic_invest_year = parseInt($("[name='basic_invest_year']:checked").val());
    var basic_house = parseInt($("[name='basic_house']:checked").val());

    var attitude_age = parseInt($("[name='attitude_age']:checked").val());
    var attitude_character = parseInt($("[name='attitude_character']:checked").val());
    var attitude_target = parseInt($("[name='attitude_target']:checked").val());
    var attitude_choice = parseInt($("[name='attitude_choice']:checked").val());
    var attitude_future = parseInt($("[name='attitude_future']:checked").val());
    var attitude_decide = parseInt($("[name='attitude_decide']:checked").val())
        ;

    // 风险态度
    var fxtd = attitude_age + attitude_character + attitude_target + attitude_choice + attitude_choice + attitude_future + attitude_decide;
    //16~32 保守型 33~50 稳健性 51~66 激进型
    var fxtd_type;
    var fxtd_description;

    if (fxtd <= 32) {
        fxtd_type = "保守型";
        fxtd_description = "保守型投资者是典型的风险厌恶者，注重获得相对确定的投资回报，但不追求高额的回报，且忍受不了短期内的资产大幅波动。投资期限内，回报率的波动性较小。这种类型的投资者，能够在短期内克服风险，获得稳定收益，但从中长期来看，回报率较低。"
    } else if (fxtd <= 50) {
        fxtd_type = "稳健型";
        fxtd_description = "稳健型投资者既担忧风险也渴望收益，希望在较低风险下获取稳健的收益。理财时要对投资本金的安全性给予适当关注，主要是投资者的资产可能保持一个稳步上升的态势。"
    } else {
        fxtd_type = "激进型";
        fxtd_description = "激进型投资者或者因为财务状况十分乐观，或者因为投资期限较长。为了追求最大回报，愿意承受资产价格的短期大幅波动风险，甚至相对长时间的亏损。但承担的较高风险水平，在大多数情况下，也往往能够带来较高的收益回报。";
    }

    // 获利期待
    var hlqd = attitude_target * 3 + attitude_choice * 5 + attitude_future * 2;
    // 10~30: 稳定小额报酬 31~70：中等报酬 71~100：高额报酬
    var hlqd_type;
    // 推荐算法：根据获利期待推荐相对应平均利率的5个最热门平台 小额稳定报酬：%8以下 中等报酬：%8~%12 大额报酬：%13以上
    var platform_earn_start; // 包括
    var platform_earn_end;   // 不包括
    if (hlqd <= 30) {
        hlqd_type = "稳定小额报酬";
        platform_earn_start = 1;
        platform_earn_end = 8;
    } else if (hlqd <= 70) {
        hlqd_type = "中等报酬";
        platform_earn_start = 8;
        platform_earn_end = 13;
    } else {
        hlqd_type = "高额报酬";
        platform_earn_start = 13;
        platform_earn_end = 101;
    }

    // 风险承受能力
    var fxcs = basic_age + basic_occupation + basic_family + basic_invest_year + basic_house;

    if (isFirst) {
        $("#show_panel").append('<div class="panel-heading">' +
            '<h3 class="panel-title"><span class="glyphicon glyphicon-hand-right"></span>&nbsp;&nbsp;测试结果</h3></div> ' +
            '<div class="panel-body" id="answer" style="line-height: 200%">' +
            '</div>'
        )
        isFirst = false;
    }


    $("#answer").html(
        "<p ><span class='glyphicon glyphicon-hand-right'></span>&nbsp;&nbsp;风险态度: " + fxtd_type + "</p>" +
        "<p >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; " + fxtd_description + "</p>" +
        "<p ><span class='glyphicon glyphicon-hand-right'></span>&nbsp;&nbsp;风险承受能力: " + fxcs + " 分</p>" +
        "<p ><span class='glyphicon glyphicon-hand-right'></span>&nbsp;&nbsp;获利期待: " + hlqd_type + "</p>" +
        "<p ><span class='glyphicon glyphicon-hand-right'></span>&nbsp;&nbsp;推荐平台:<span id='show_ul'></span></p>"
    );

    // 推荐算法：根据获利期待推荐相对应平均利率的5个最热门平台 小额稳定报酬：%8以下 中等报酬：%8~%12 大额报酬：%13以上
    var show_info = [];
    for (var i = 0; i < data_info.length; ++i) { // 逐个替换
        var info = data_info[i];
        if (info.platEarnings.length == 0)
            continue;
        var earn = info.platEarnings;
        if (earn >= platform_earn_start && earn < platform_earn_end) {
            show_info.push(info);
        }
    }

    // 选出热门的五个
    show_info.sort(
        function (d1, d2) {
            if (d1.rank.length == 0)
                return 1;
            if (d2.rank.length == 0)
                return -1;
            return (d1.rank - d2.rank) * 1;
        }
    );

    var show_num = 5;
    for (var i = 0; i < show_num; ++i) {
        var info = show_info[i];
        html_str = "&nbsp;&nbsp;&nbsp;&nbsp;<a href= '/detail/platform/" + info.platform_name + "' target='_blank'>" + info.platform_name + "</a>";
        $("#show_ul").append(html_str);
    }

});
