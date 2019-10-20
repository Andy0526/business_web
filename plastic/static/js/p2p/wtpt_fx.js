/**
 * Created by Administrator on 2016/4/20.
 */
$(document).ready(function () {
    show_bad_platform_prob_month_statistic();
});
function show_bad_platform_prob_month_statistic() {
    var bad_platform_prob_month_statistic_chart = echarts.init(document.getElementById('bad_platform_prob_month_statistic'));
    bad_platform_prob_month_statistic_option = {
        title: {
            text: '问题平台出事月分布'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                magicType: {show: true, type: ['line', 'bar']},
            }
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
                name: '问题平台数量',
                min: 0,
                max: 140,
                axisLabel: {
                    formatter: '{value} 个'
                }
            }
        ],
        series: [
            {
                name: '问题平台数量',
                type: 'line',
                data: [69, 58, 56, 52, 55, 125, 109, 81, 55, 47, 79, 106]
            }
        ]
    };
    bad_platform_prob_month_statistic_chart.setOption(bad_platform_prob_month_statistic_option);
}


$(document).ready(function () {
    show_bad_platform_registmoney_statistic();
});
function show_bad_platform_registmoney_statistic() {
    var bad_platform_registmoney_statistic_chart = echarts.init(document.getElementById('bad_platform_registmoney_statistic'));
    bad_platform_registmoney_statistic_option = {
        title: {
            text: '问题平台注册资金分布'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                magicType: {show: true, type: ['line', 'bar']},
            }
        },

        xAxis: [
            {
                type: 'category',
                data: ['500万以下', '500~1000万', '1000~2000万', '2000~5000万', '1亿以下', '1亿以上']
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '问题平台数量',
                min: 0,
                max: 350,
                axisLabel: {
                    formatter: '{value} 个'
                }
            }
        ],
        series: [
            {
                name: '问题平台个数',
                type: 'bar',
                data: [112, 338, 130, 84, 133, 86]
            }
        ]
    };
    bad_platform_registmoney_statistic_chart.setOption(bad_platform_registmoney_statistic_option);
}


$(document).ready(function () {
    show_bad_platform_event_type_statistic();
});
function show_bad_platform_event_type_statistic() {
    var bad_platform_event_type_statistic_chart = echarts.init(document.getElementById('bad_platform_event_type_statistic'));
    bad_platform_event_type_statistic_option = {
        title: {
            text: '问题平台问题类型分布'
        },

        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        /*legend: {
         left: 'left',
         data: [ "跑路","提现困难","停业", "经侦介入"]
         },*/
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: '65%',
                center: ['50%', '55%'],
                data: [
                    {name: "跑路", value: 479},
                    {name: "提现困难", value: 249},
                    {name: "停业", value: 142},
                    {name: "经侦介入", value: 10}

                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    bad_platform_event_type_statistic_chart.setOption(bad_platform_event_type_statistic_option);
}

$(document).ready(function () {
    show_bad_platform_runtime_statistic();
});
function show_bad_platform_runtime_statistic() {
    var bad_platform_runtime_statistic_chart = echarts.init(document.getElementById('bad_platform_runtime_statistic'));
    var platform_runtime_map = {
        "1": 53,
        "2": 82,
        "3": 62,
        "4": 57,
        "5": 49,
        "6": 50,
        "7": 43,
        "8": 41,
        "9": 40,
        "10": 41,
        "11": 41,
        "12": 23,
        "13": 27,
        "14": 21,
        "15": 16,
        "16": 17,
        "17": 17,
        "18": 22,
        "19": 15,
        "20": 9,
        "21": 7,
        "22": 7,
        "23": 10,
        "24": 8,
        "25": 11,
        "26": 5,
        "27": 9,
        "28": 4,
        "29": 3,
        "30": 4,
        "31": 8,
        "32": 13,
        "33": 10,
        "34": 6,
        "35": 13,
        "36": 22,
        "37": 2,
        "38": 2,
        "39": 1,
        "41": 1,
        "42": 2,
        "43": 4,
        "47": 4,
        "48": 2,
        "49": 1,
        "51": 1,
        "58": 1,
        "59": 1,
        "60": 1,
        "62": 2,
        "63": 1
    };
    //var data_x = [];
    var data_y = [];
    var num = 0;
    for (var i = 1; i <= 63; ++i) {
        if (platform_runtime_map["" + i] != null)
            num += platform_runtime_map["" + i];
        if (i % 6 == 0) {
            data_y.push(num);
            num = 0;
        }
    }
    data_y.push(num);


    bad_platform_runtime_statistic_option = {
        title: {
            text: '问题平台运营时间分布'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            feature: {
                magicType: {show: true, type: ['line', 'bar']},
            }
        },

        xAxis: [
            {
                type: 'category',
                data: ["半年", "1年", "1年半", "2年", "2年半", "3年", "3年半", "4年", "4年半", "5年", "5年半"]
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '问题平台数量',
                min: 0,
                max: 360,
                axisLabel: {
                    formatter: '{value} 个'
                }
            }
        ],
        series: [
            {
                name: '问题平台个数',
                type: 'bar',
                data: data_y
            }
        ]
    };
    bad_platform_runtime_statistic_chart.setOption(bad_platform_runtime_statistic_option);
}


$(document).ready(function () {
    industry_areas();
});
function industry_areas() {
    var data_info = {
        '贵州': {
            "问题平台": 6,
        },
        '河南': {
            "问题平台": 18,
        },
        '山东': {
            "问题平台": 190,
        },
        '四川': {
            "问题平台": 28,
        },
        '江苏': {
            "问题平台": 47,
        },
        '新疆': {
            "问题平台": 2,
        },
        '福建': {
            "问题平台": 25,
        },
        '浙江': {
            "问题平台": 84,
        },
        '湖北': {
            "问题平台": 17,
        },
        '天津': {
            "问题平台": 11,
        },
        '江西': {
            "问题平台": 9,
        },
        '黑龙江': {
            "问题平台": 2,
        },
        '广东': {
            "问题平台": 145,
        }, '云南': {
            "问题平台": 14,
        },
        '北京': {
            "问题平台": 53,
        },
        '合肥': {
            "问题平台": 1,
        }, '广西': {
            "问题平台": 13,
        },
        '陕西': {
            "问题平台": 9,
        },
        '甘肃': {
            "问题平台": 3,
        },
        '河北': {
            "问题平台": 36,
        },
        '吉林': {
            "问题平台": 6,
        },
        '重庆': {
            "问题平台": 10,
        },
        '宁夏': {
            "问题平台": 3,
        },
        '湖南': {
            "问题平台": 23,
        },
        '安徽': {
            "问题平台": 45,
        },
        '内蒙古': {
            "问题平台": 4,
        },
        '上海': {
            "问题平台": 66,
        },
        '山西': {
            "问题平台": 9,
        }, '海南': {
            "问题平台": 7,
        },
        '辽宁': {
            "问题平台": 6,
        }
    };

    var data = [];
    for (var key in data_info) {
        data.push({name: key, value: data_info[key]['问题平台']})
    }

    var industry_areas_chart = echarts.init(document.getElementById('industry_areas'));
    industry_areas_option = {
        title: {
            text: '问题平台分布',
            left: 'center'
        },
        dataRange: {
            min: 0,
            max: 190,
            x: 'left',
            y: 'bottom',
            text: ['高', '低']
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return params.name + '<br>'
                    + '问题平台数量: ' + data_info[params.name]['问题平台'] + '<br>'

            }
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['问题平台数量']
        },
        series: [
            {
                name: '问题平台数量',
                type: 'map',
                mapType: 'china',
                roam: false,

                itemStyle: {
                    normal: {label: {show: true}},
                    emphasis: {label: {show: true}}
                },
                data: data
            }
        ]
    };
    industry_areas_chart.setOption(industry_areas_option);
}