/**
 * Created by Administrator on 2016/4/20.
 */
// 数据缓存
var data_info;

// 替换字符串
function replace_data_info() {
    for (var i = 0; i < data_info.length; ++i) { // 逐个替换
        var info = data_info[i];
        // 背景
        if (info.platform_background.length > 2) {
            info.platform_background = info.platform_background.substr(0, info.platform_background.length - 2);
        }
        // 成交量
        if (info.platform_volume.length > 2) {
            info.platform_volume = info.platform_volume.substr(0, info.platform_volume.length - 2);
        }
        // 累计代还金额
        if (info.platform_need_return.length > 2) {
            info.platform_need_return = info.platform_need_return.substr(0, info.platform_need_return.length - 2);
        }
        // 借款周期
        if (info.platform_borrowing_period.length > 1) {
            info.platform_borrowing_period = info.platform_borrowing_period.substr(0, info.platform_borrowing_period.length - 1);
        }
    }
}

// 量化评级
function rankToVal(rank) {
    if (rank == "A+")
        return 10;
    else if (rank == "A")
        return 9;
    else if (rank == "A-")
        return 8;
    else if (rank == "B+")
        return 7;
    else if (rank == "B")
        return 6;
    else if (rank == "B-")
        return 5;
    else if (rank == "C+")
        return 4;
    else if (rank == "C")
        return 3;
    else if (rank == "C-")
        return 2;
}

// 进行排序
function platform_sort(tag, updown) {
    if (tag == '人气指数') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_index.length == 0)
                    return 1;
                if (d2.platform_index.length == 0)
                    return -1;
                return (d1.platform_index - d2.platform_index) * updown;
            }
        );
    } else if (tag == '评级') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_rank.length == 0)
                    return 1;
                if (d2.platform_rank.length == 0)
                    return -1;
                var r1 = rankToVal(d1.platform_rank);
                var r2 = rankToVal(d2.platform_rank);
                return (r1 - r2) * updown;
            }
        );

    } else if (tag == '平均收益') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_earn.length == 0)
                    return 1;
                if (d2.platform_earn.length == 0)
                    return -1;
                var r1 = d1.platform_earn.substr(0, d1.platform_earn.length - 1); // 获取子字符串
                var r2 = d2.platform_earn.substr(0, d2.platform_earn.length - 1); // 获取子字符串
                return (parseFloat(r1) - parseFloat(r2)) * updown;
            }
        );
    } else if (tag == '上线时间') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_time.length == 0)
                    return 1;
                if (d2.platform_time.length == 0)
                    return -1;
                str1 = d1.platform_time.replace(/-/g, "/");
                str2 = d2.platform_time.replace(/-/g, "/");
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
    } else if (tag == "成交量") {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_volume.length == 0)
                    return 1;
                if (d2.platform_volume.length == 0)
                    return -1;
                //  var r1 = d1.platform_volume.substr(0, d1.platform_volume.length - 2); // 获取子字符串
                /// var r2 = d2.platform_volume.substr(0, d2.platform_volume.length - 2); // 获取子字符串
                return (parseFloat(d1.platform_volume) - parseFloat(d2.platform_volume)) * updown;
            }
        );
    } else if (tag == '平均借款期限') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_borrowing_period.length == 0)
                    return 1;
                if (d2.platform_borrowing_period.length == 0)
                    return -1;
                var r1 = d1.platform_borrowing_period; // 获取子字符串
                var r2 = d2.platform_borrowing_period; // 获取子字符串
                return (parseFloat(r1) - parseFloat(r2)) * updown;
            }
        );
    } else if (tag == '累计待还金额') {
        data_info.sort(
            function (d1, d2) {
                if (d1.platform_need_return.length == 0)
                    return 1;
                if (d2.platform_need_return.length == 0)
                    return -1;
                var r1 = d1.platform_need_return; // 获取子字符串
                var r2 = d2.platform_need_return; // 获取子字符串
                return (parseFloat(r1) - parseFloat(r2)) * updown;
            }
        );
    }
    $("#sort_tag").text(tag);
    if (updown > 0)
        $("#sort_updown").text("递增");
    else
        $("#sort_updown").text("递减");
    show_data(data_info);
    show_data(data_info);
    return;
}


// 展示数据
function show_data(data_info) {
    $("tbody").html(""); // 清空
    for (var i = 0; i < data_info.length; ++i) { // 逐个渲染
        var info = data_info[i];
        $("tbody").append("<tr>" +
            "<td>" + (i + 1) + "</td>" +
            "<td> " + info.platform_name + "</td>" +
            "<td>" + info.online_time + "</td>" +
            "<td>" + info.problem_time + "</td>" +
            "<td>" + info.region + "</td>" +
            "<td>" + info.registration_capital + "</td>" +
            "<td>" + info.event_type + "</td>" +
            "</tr>"
        );
    }
}


// 加载数据
$(document).ready(function () {
    $.getJSON("/detail/problem_platforms", function (data) {

        // 整理数据
        show_data(data.platforms);
        // 显示平台内容
        $("#platform_num").text(data.platforms.length);

    });
});