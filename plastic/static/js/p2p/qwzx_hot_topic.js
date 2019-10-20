/**
 * Created by Administrator on 2016/4/19.
 */
// 根据返回信息添加元素
function append_info(topic_id, items) {
    for (var i = 0; i < items.length; ++i) {
        $('#show').append(
            "<a href='/info/hot/topic/news/detail/" + topic_id + "/" + items[i]._id + "' target='_blank' class='list-group-item'>" +
            "<div class='row'>" +
            "<div class='col-md-9 ' style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" + items[i].title + "</div>" +
            "<div class='col-md-3' style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>" + items[i].item_pub_time + "</div>" +
            "</div>" +
            "</a>"
        );
    }
}

// 显示热点词汇
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


function show_hot_word(word_data) {

    $("#hot_content").html("");
    var size = 50;
    var show_data = [];
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

// 显示热点趋势
function show_hot_trend(hot_map) {
    div_object = $("#hot_trend");
    div_object.height(Math.round(div_object.width() * 0.45))
    var hot_trend_chart = echarts.init(document.getElementById('hot_trend'));
    hot_trend_option = {
        tooltip: {
            trigger: 'axis'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: hot_map.x
            }
        ],
        yAxis: [
            {
                name: '热度值',
                type: 'value'
            }
        ],
        series: [
            {
                name: '热度',
                type: 'line',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: hot_map.y
            }
        ]
    };
    hot_trend_chart.setOption(hot_trend_option);
}

// 加载数据
$(document).ready(function () {

    var topic_id = $("#topic_id").text();
    if (topic_id == 1) {
        $("#title").text("e租宝涉嫌违法经营分崩离析");
    } else if (topic_id == 2) {
        $("#title").text("P2P监管办法征求意见稿发布");

    } else if (topic_id == 3) {
        $("#title").text("宜人贷上市");

    } else if (topic_id == 4) {
        $("#title").text("翼龙贷3.7亿豪夺央视标王");
    }

    $.getJSON("/info/hot/topic/preview/" + topic_id, function (data) {
        show_hot_word(data.keyword_list);
        append_info(topic_id, data.item_list);
        show_hot_trend(data.hot_map)

    });

});