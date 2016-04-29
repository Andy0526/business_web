/**
 * Created by Administrator on 2016/4/20.
 */

$(document).ready(function () {
    show_chart_platform_background();
});
function show_chart_platform_background() {
    var chart_platform_background_chart = echarts.init(document.getElementById('chart_platform_background'));
    chart_platform_background_option = {
        title: {
            x: 'left',
            text: '热门平台背景统计'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{b}<br/>{d}%"
        },
        legend: {
            orient: 'vertical',
            x: 'right',
            data: ["无背景", "上市公司", "VC/PE", "国资"]
        },
        calculable: true,
        series: [
            {
                name: '背景',
                type: 'pie',
                radius: ['55%', '70%'],
                itemStyle: {
                    normal: {
                        label: {
                            show: false
                        },
                        labelLine: {
                            show: false
                        }
                    },
                    emphasis: {
                        label: {
                            show: true,
                            position: 'center',
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    }
                },
                data: [
                    {name: "无背景", value: 41},
                    {name: "上市公司", value: 22},
                    {name: "VC/PE", value: 29},
                    {name: "国资", value: 10},
                ]
            }
        ]
    };
    chart_platform_background_chart.setOption(chart_platform_background_option);
}


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
    $("#sort_tag").text(tag);
    if (updown > 0)
        $("#sort_updown").text("递增");
    else
        $("#sort_updown").text("递减");
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
            "<td>" + info.platform_name + "</a></td>" +
            "<td>" + info.rank + "</td>" +
            "<td>" + info.platEarnings + "%</td>" +
            "<td>" + info.registeredCapital + "万</td>" +
            "<td>" + info.onlineDate + "</td>" +
            "<td>" + info.locationAreaName + info.locationCityName + "</td>" +

            "<td style='text-align:center'> <a href= '/detail/platform/" + info.platform_name + "' target='_blank'>查看详情</a></td>" +
            "</tr>"
        );
    }
}


function show_syjg() {
    data_info.sort(
        function (d1, d2) {
            if (d1.platEarnings.length == 0)
                return 1;
            if (d2.platEarnings.length == 0)
                return -1;
            return (d1.platEarnings - d2.platEarnings) * -1;
        }
    );
    var rank_num = 10;
    for (var i = 0; i < rank_num; ++i) { // 逐个渲染
        var info = data_info[i];
        $("#rank_platform_earn").append(
            "<a href= '/detail/platform/" + info.platform_name + "' target='_blank' class='list-group-item'><strong>" + (i + 1) + "</strong>&nbsp;&nbsp;" + info.platform_name + "(" + info.platEarnings + "%)" + "</a>"
        );
    }
}

var recent_reviews_list;
function init_recent_reviews(in_recent_reviews_list) {
    recent_reviews_list = in_recent_reviews_list;
}

var show_index = -1;
function show_recent_reviews() {

    show_index++;
    if (show_index >= recent_reviews_list.length) {
        show_index = 0;
    }
    var show_num = 5;
    $("#recent_reviews").html("");
    for (var i = 0; i < show_num; ++i) {
        var index = (show_index + i) % recent_reviews_list.length;
        var recent_review = recent_reviews_list[index];

        var attitude = "";
        var head_str = "";
        if (recent_review.evaluation == 0 || recent_review.evaluation == 1) {
            attitude = "不推荐"
            head_str = '&nbsp;<span class="label label-danger">'

        } else {
            attitude = "推荐"
            head_str = '&nbsp;<span class="label label-success">'
        }

        var labels_list = recent_review.label;
        var tags_str = "";
        for (var j = 0; j < labels_list.length; ++j) {
            tags_str += head_str + labels_list[j] + '</span>';
        }

        var show_str =
            "<div class='panel-body'>" +
            recent_review.reviewUserName +
            "&nbsp;" +
            "<strong>" + attitude + "</strong>" +
            "&nbsp;" +
            "<span>" + recent_review.platName + "</span>" +
            "<br>" +
            tags_str +
            "</div>";
        $("#recent_reviews").append(show_str);
    }
}

// 加载数据
$(document).ready(function () {
    $.getJSON("/detail/platforms", function (data) {
        data_info = data.platforms
        // 整理数据
        replace_data_info();

        // 显示收益较高列表
        show_syjg();

        // 显示网友最新评论
        init_recent_reviews(data.recent_reviews_list);
        show_recent_reviews()

        setInterval(show_recent_reviews, 2500);// 注意函数名没有引号和括弧！

        // 显示平台内容
        $("#platform_num").text(data_info.length);
        platform_sort('综合排名', '1');
        show_data(data_info);
    });
});


