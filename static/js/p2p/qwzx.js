/**
 * Created by Administrator on 2016/4/19.
 */

var day_hot_keywords;
var week_hot_keywords;
var month_hot_keywords;

$(document).ready(function () {
    $.getJSON("/info/hot", function (data, textStatus, jqXHR) {
        day_hot_keywords = data.day_hot_keywords;
        week_hot_keywords = data.week_hot_keywords;
        month_hot_keywords = data.month_hot_keywords;
        show_hot_word(data.day_hot_keywords)
    });
});

// 设置点击事件
$("#hot_day").click(function () {
    $("#hot_day").attr("class", "active");
    $("#hot_week").attr("class", "");
    $("#hot_month").attr("class", "");
    show_hot_word(day_hot_keywords);
});

$("#hot_week").click(function () {
    $("#hot_day").attr("class", "");
    $("#hot_week").attr("class", "active");
    $("#hot_month").attr("class", "");
    show_hot_word(week_hot_keywords);
});

$("#hot_month").click(function () {
    $("#hot_day").attr("class", "");
    $("#hot_week").attr("class", "");
    $("#hot_month").attr("class", "active");
    show_hot_word(month_hot_keywords);
});

function createRandomItemStyle() {
    var base = 225;
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * base),
                Math.round(Math.random() * base),
                Math.round(Math.random() * base)
            ].join(',') + ')'
        }
    };
}

// 显示热点词汇
function show_hot_word(word_data) {

    $("#hot_content").html("");
    var size = 50;
    var show_data = [];
    //alert(word_data.length)
    for (var i = 0; i < word_data.length; ++i) {
        var word = word_data[i];
        if (size > 40)
            size -= 4;
        else if (size > 24)
            size -= 2;
        else if (size > 8)
            size -= 1;

        var item = {};
        item['name'] = word['name'];
        item['value'] = size;
        item['itemStyle'] = createRandomItemStyle();
        show_data.push(item);
    }

    var cy_chart = echarts.init(document.getElementById('hot_content'));
    option = {
        series: [{
            type: 'wordCloud',
            size: ['100%', '100%'],
            textRotation: [0, 45, -45, 90],
            textPadding: 1,
            autoSize: {
                enable: true,
                minSize: 40
            },
            data: show_data
        }]
    };
    cy_chart.setOption(option);
}


// 根据返回信息添加元素
function append_info(div_id, type) {
    var num = 6;
    if (type == 'ugc') {
        num = 10;
    }
    $.getJSON("/info/" + type + "/list/" + num, function (data) {
        var items = data.type_list;
        for (var i = 0; i < items.length; ++i) {
            if (type == 'ugc') {
                $(div_id).append(
                    "<a href='/info/" + type + "/" + items[i]._id + "' class='list-group-item'>" +
                    "<div class='row'>" +
                    "<div class='col-md-12'   style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color: #2b669a'>" +
                    "<strong>Q: </strong>&nbsp&nbsp" + items[i].title + "</div>" +
                    "</div>" +
                    "<div class='row' style='margin-top:5px'>" +
                    "<div class='col-md-9' style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" +
                    "<strong>A: </strong>&nbsp&nbsp" + items[i].content + "</div>" +
                    "<div class='col-md-3'  style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" + items[i].author + "&nbsp;&nbsp; " + items[i].item_pub_time + "</div>" +
                    "</div>" +
                    "</a>"
                );
            } else {
                var title = items[i].title;
                if (title.length == 0) {
                    var content = items[i].content
                    title = content;
                }

                var head_str = '&nbsp;<span class="label label-default">';
                if (type == 'news') {
                    head_str = '&nbsp;<span class="label label-danger">';
                } else if (type == 'policy') {
                    head_str = '&nbsp;<span class="label label-warning">';
                } else if (type == 'opinion') {
                    head_str = '&nbsp;<span class="label label-success">';
                }

                var tags_str = "";
                var tags = items[i].tags;
                if (tags.length > 0) {
                    var tags_list = tags.split(',');
                    for (var j = 0; j < tags_list.length; ++j) {
                        tag = tags_list[j]
                        tags_str += head_str + tag + '</span>';
                    }
                }

                $(div_id).append(
                    "<a href='/info/" + type + "/" + items[i]._id + "' class='list-group-item '>"
                    + "<div class='row'>"
                    + "<div class='col-md-12'>"
                    + "<div style='font-size: large;width:95%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" + title + "</div>"
                    + "<div style='margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" + items[i].item_pub_time + "&nbsp;&nbsp;&nbsp;&nbsp;" + items[i].author + tags_str + "</div>"
                    + "</div>"
                    + "</div>"
                    + "</a>"
                );
            }
        }
        $(div_id).append(
            "<a href='/info/" + type + "' class='list-group-item' style='text-align:center;'>点击查看更多</a>"
        );
    });
}

// 加载数据
$(document).ready(function () {
    append_info("#show_xw", "news");
    append_info("#show_zc", "policy");
    append_info("#show_gd", "opinion");
    append_info("#show_dp", "ugc");
});


$(document).ready(function () {
    show_source_summary();
});
function show_source_summary() {
    var source_summary_chart = echarts.init(document.getElementById('source_summary'));
    source_summary_option = {
        tooltip: {
            trigger: 'item',
            formatter: "{b}:{d}%"
        },
        legend: {
            left: 'left',
            data: ["知乎", "微信", "微博", "融360", "网贷之家", "P2P观察网", "P2P理财", "金评媒", "中申网",]
        },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: ['45%', '65%'],
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
                    {name: "知乎", value: 14486},
                    {name: "微信", value: 9457},
                    {name: "微博", value: 2313},
                    {name: "融360", value: 1736},
                    {name: "网贷之家", value: 266},
                    {name: "P2P观察网", value: 222},
                    {name: "P2P理财", value: 101},
                    {name: "金评媒", value: 381},
                    {name: "中申网", value: 155}
                ]
            }
        ]
    };
    source_summary_chart.setOption(source_summary_option);
}

