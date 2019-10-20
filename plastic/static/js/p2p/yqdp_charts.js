/**
 * Created by Administrator on 2016/4/19.
 */
var rate = 0.7;
$(document).ready(function () {
    div_object = $("#month_summary");
    div_object.height(Math.round(div_object.width() * 0.45))
    show_month_summary();
});
function show_month_summary() {
    var month_summary_chart = echarts.init(document.getElementById('month_summary'));
    month_summary_option = {
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: ['政策', '新闻', '用户评论']
        },
        xAxis: [
            {
                type: 'category',
                data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '文章数',
                min: 0,
                max: 1250,
                interval: 250,
                axisLabel: {
                    formatter: '{value} 篇'
                }
            },
            {
                type: 'value',
                name: '评论数',
                min: 0,
                max: 35000,
                interval: 7000,
                axisLabel: {
                    formatter: '{value} 条'
                }
            }
        ],
        series: [
            {
                name: '政策',
                type: 'bar',
                data: [20, 22, 35, 10, 14, 12, 31, 17, 11, 12, 15, 24]
            },
            {
                name: '新闻',
                type: 'bar',
                data: [467, 319, 472, 561, 597, 608, 799, 842, 903, 778, 1018, 1176]
            },
            {
                name: '用户评论',
                type: 'line',
                yAxisIndex: 1,
                data: [6968, 7817, 9918, 14039, 14264, 12357, 17655, 20388, 22736, 29731, 34460, 34222]
            }
        ]
    };
    month_summary_chart.setOption(month_summary_option);
}


$(document).ready(function () {
    div_object = $("#industry_areas");
    div_object.height(Math.round(div_object.width() * rate))
    industry_areas();
});
function industry_areas() {
    var data_info = {
        '广东': {
            "成交量": "369.5亿元",
            "运营平台": "461",
            "问题平台": "241家",
            "综合利率": "11.89%"
        },
        '北京': {
            "成交量": "305.74亿元",
            "运营平台": "213",
            "问题平台": "87家",
            "综合利率": "10.83%"
        },
        '上海': {
            "成交量": "142.42亿元",
            "运营平台": "213",
            "问题平台": "116家",
            "综合利率": "10.4%"
        },
        '浙江': {
            "成交量": "137.42亿元",
            "运营平台": "292",
            "问题平台": "157家",
            "综合利率": "11.44%"
        },
        '山东': {
            "成交量": "43.6亿元",
            "运营平台": "311",
            "问题平台": "266家",
            "综合利率": "16.5%"
        },
        '江苏': {
            "成交量": "26.55亿元",
            "运营平台": "127",
            "问题平台": "84家",
            "综合利率": "15.72%"
        },
        '四川': {
            "成交量": "26.27亿元",
            "运营平台": "83",
            "问题平台": "45家",
            "综合利率": "13.18%"
        },
        '湖北': {
            "成交量": "12.31亿元",
            "运营平台": "83",
            "问题平台": "50家",
            "综合利率": "16.31%"
        },
    };

    var names = [];
    for (var key in data_info) {
        names.push(key)
    }

    var industry_areas_chart = echarts.init(document.getElementById('industry_areas'));
    industry_areas_option = {
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return params.name + '<br>'
                    + '运营平台: ' + data_info[params.name]['运营平台'] + '家<br>'
                    + '成交量: ' + data_info[params.name]['成交量'] + '<br>'
                    + '问题平台: ' + data_info[params.name]['问题平台'] + '<br>'
                    + '综合利率: ' + data_info[params.name]['综合利率'] + '<br>'
            }
        },
        dataRange: {
            min: 0,
            max: 470,
            x: 'left',
            y: 'bottom',
            text: ['高', '低']
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['运营平台数量']
        },
        series: [
            {
                name: '运营平台数量',
                type: 'map',
                mapType: 'china',
                roam: false,
                itemStyle: {
                    normal: {label: {show: true}},
                    emphasis: {label: {show: true}}
                },
                data: names.map(function (d) {
                    return {name: d, value: data_info[d]['运营平台']}
                })
            }
        ]
    };
    industry_areas_chart.setOption(industry_areas_option);
}

$(document).ready(function () {
    div_object = $("#industry_hot_people");
    div_object.height(Math.round(div_object.width() * rate))
    show_industry_hot_people();
});
function show_industry_hot_people() {
    var industry_hot_people_chart = echarts.init(document.getElementById('industry_hot_people'));
    industry_hot_people_option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['借款人数', '投资人数']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
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
                data: [
                    '2015/1/1', '2015/2/1', '2015/3/1', '2015/4/1', '2015/5/1', '2015/6/1',
                    '2015/7/1', '2015/8/1', '2015/9/1', '2015/10/1', '2015/11/1', '2015/12/1'
                ]
            }
        ],
        yAxis: [
            {
                name: '人数(万人)',
                type: 'value'
            }
        ],
        series: [
            {
                name: '借款人数',
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: [19.1, 16.18, 18.17, 22.69, 27.84, 33.04, 44.13, 54.94, 56.91, 58.09, 71.94, 78.49]
            },
            {
                name: '投资人数',
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: [88.22, 80.86, 96.16, 113, 126.79, 154.36, 179.31, 204.28, 240.41, 247.34, 300.62, 298.02]
            }
        ]
    };
    industry_hot_people_chart.setOption(industry_hot_people_option);
}

$(document).ready(function () {
    div_object = $("#industry_hot_money");
    div_object.height(Math.round(div_object.width() * rate))
    show_industry_hot_money();
});
function show_industry_hot_money() {
    var industry_hot_money_chart = echarts.init(document.getElementById('industry_hot_money'));
    industry_hot_money_option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['人均投资', '人均借款']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
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
                data: [
                    '2015/1/1', '2015/2/1', '2015/3/1', '2015/4/1', '2015/5/1', '2015/6/1',
                    '2015/7/1', '2015/8/1', '2015/9/1', '2015/10/1', '2015/11/1', '2015/12/1'
                ]
            }
        ],
        yAxis: [
            {
                name: '金额(元)',
                type: 'value'
            }
        ],
        series: [
            {
                name: '人均投资',
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: [40559, 41446, 51227, 48801, 48081, 42729,
                    46015, 47710, 47913, 48374, 44282, 44878]
            },
            {
                name: '人均借款',
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: [187340, 207132, 271106, 243037, 218973, 199649,
                    186987, 177398, 202419, 205974, 185061, 170391]
            }
        ]
    };
    industry_hot_money_chart.setOption(industry_hot_money_option);
}

$(document).ready(function () {
    div_object = $("#industry_interest");
    div_object.height(Math.round(div_object.width() * rate))
    show_industry_interest();
});
function show_industry_interest() {
    var industry_interest_chart = echarts.init(document.getElementById('industry_interest'));
    industry_interest_option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['综合利率']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
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
                data: [
                    '2015/3/1', '2015/4/1', '2015/5/1', '2015/6/1', '2015/7/1', '2015/8/1', '2015/9/1', '2015/10/1', '2015/11/1', '2015/12/1', '2016/1/1', '2016/2/1'
                ]
            }
        ],
        yAxis: [
            {
                name: '百分比(%)',
                type: 'value'
            }
        ],
        series: [
            {
                name: '综合利率',
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: [15.02, 14.46, 14.57, 14.17, 13.58, 12.98, 12.63, 12.38, 12.25, 12.45, 12.18, 11.86]
            }
        ]
    };
    industry_interest_chart.setOption(industry_interest_option);
}