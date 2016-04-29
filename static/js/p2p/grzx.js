/**
 * Created by Administrator on 2016/4/19.
 */
// 列表相关 -----------------------------------------------
var platform_name_list; // 全局的
var last_str = "";

var selecet_platform_names_list;
var show_name ;
var username;

// 重新设置
function reset_selecet_platform_names_list(new_selecet_platform_names_list,show_first){
     selecet_platform_names_list =  new_selecet_platform_names_list
     if (selecet_platform_names_list.length == 0) {
        show_name = ""
        $("#selecet_platform_names").html("");
         return
    }

    if(show_first) {
        show_name = selecet_platform_names_list[0];
    }else{
        show_name = selecet_platform_names_list[selecet_platform_names_list.length-1];
    }
    show_platform();

}


// 列表点击事件
function slecet_name(object) {
    $("#input_name")[0].value = object.text;
    update_show_list();
}
// 更新列表
function update_show_list() {
    var input_name = $("#input_name")[0].value;
    // 字符串相同不更新列表
    if (input_name == last_str)
        return;
    last_str = input_name;
    // 更新列表
    $("#platform_name_list").html("");
    for (var i = 0; i < platform_name_list.length; ++i) {
        platform_name = platform_name_list[i];
        if (platform_name.indexOf(input_name) >= 0) {
            $("#platform_name_list").append("<a class='list-group-item' onclick='slecet_name(this)'>" + platform_name + "</a>")
        }
    }
}

// 添加列表
function add_interested_platform() {
    if (selecet_platform_names_list.length >= 3) {
        my_alert("最多只能添加三个！")
        return;
    }

    var input_name = $("#input_name")[0].value;
    // 检查输入
    if (input_name.length == 0) {
        my_alert("添加的平台名称不能为空！");
        return;
    }
    // 是否存在
    var is_existed = false;
    for (var i = 0; i < platform_name_list.length; ++i) {
        platform_name = platform_name_list[i];
        if (platform_name == input_name) {
            is_existed = true;
            break;
        }
    }
    if (!is_existed) {
        my_alert("系统无该平台数据，请输入列表中的平台名称！");
        return;
    }

    var index = selecet_platform_names_list.indexOf(input_name);
    if (index < 0) {
        $.getJSON("/user/platform/add/username="+username+"&platform_name="+input_name, function (data) {
            if(data.result==1){
                reset_selecet_platform_names_list(data.platform_names,false)
                my_alert('添加成功！')
            }else{
                my_alert('添加失败！')
            }
        });
    } else {
        my_alert("已经存在！")
    }
}

// 列表显示相关 ----------------------------------------------

// 点击事件
function btn_click(name) {
    show_name = name;
    show_platform();
}

// 刷新
function show_platform() {
    $("#selecet_platform_names").html("");
    for (var i = 0; i < selecet_platform_names_list.length; ++i) {
        platform_name = selecet_platform_names_list[i];
        $("#selecet_platform_names").append(
            "<button value=" + platform_name + " class='btn btn-lg btn-info' type='button' style='opacity: 0.85' onclick='btn_click(this.value)'>" +
            platform_name +
            "</button>&nbsp;" +
            "<button class='btn btn-lg btn-info' style='opacity: 0.85' type='button'>" +
            "<span title=" + platform_name + " class='glyphicon glyphicon-minus' onclick='remove_platform_name(this)'> " + "</span>" +
            "</button>&nbsp;&nbsp;&nbsp;&nbsp;"
        )
    }
    if (show_name != "") {
        $("#selecet_platform_names").append("<br><br>")
        show_paltform_info(show_name)
    }
}

// 删除一个平台
function remove_platform_name(object) {
    var platform_name = object.title;
     $.getJSON("/user/platform/remove/username="+username+"&platform_name="+platform_name, function (data) {
            if(data.result==1){
                reset_selecet_platform_names_list(data.platform_names,true)
                my_alert('删除成功！')
            }else{
                my_alert('删除失败！')
            }
    });
}


$(document).ready(function () {

     username = $.cookie('username')
     if( username == null) {  // 未登录
         window.location.href = "/sign_in";
         return
     }

     $('#welcome_username').html(username)

     $.getJSON("/user/"+username, function (data) {
         selecet_platform_names_list = data.platform_names
          if(selecet_platform_names_list.length==0)
              show_name = ""
         else
              show_name = selecet_platform_names_list[0]
         show_platform();
    });

    $.getJSON("/ptpx/platform_name_list", function (data) {
        platform_name_list = data.platform_name_list;
        for (var i = 0; i < platform_name_list.length; ++i) {
            platform_name = platform_name_list[i];
            $("#platform_name_list").append("<a class='list-group-item'  onclick='slecet_name(this)'>" + platform_name + "</a>")
        }
    });
});

function show_paltform_info(platform_name) {

    $("#selecet_platform_names").append(
        '<a id="chart_div_title" class="list-group-item list-group-item-info"> ' +
        '<span class="glyphicon glyphicon-hand-right"></span>&nbsp&nbsp' + platform_name + '的数据</a>' +
        '<div id="chart_dropdown" class="dropdown"  style="border:1px solid lightgrey;border-top: none;border-bottom: none">' +
        '<button class="btn btn-info dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true' +
        'style="margin-left: 15px;margin-top: 15px;"> ' +
        '<span id="show_chart_title"> 利率信息</span> ' +
        '<span class="caret"></span> </button> ' +
        '<ul class="dropdown-menu" aria-labelledby="dropdownMenu1"> ' +
        '<li> <a onclick="show_chart(\'chart_div\', \'利率信息\', \'0\',\'x\',\'y1\', \'百分比(%)\')">利率信息</a> </li>' +
        '<li> <a onclick="show_chart(\'chart_div\', \'成交量信息\', \'0\',\'x\',\'y2\', \'成交量(万)\')">成交量信息</a> </li>' +
        '<li> <a onclick="show_chart(\'chart_div\', \'待还款信息\', \'1\',\'x\',\'y1\', \'代还款(万)\')">待还款信息</a> </li>' +
        '<li> <a onclick="show_chart(\'chart_div\', \'资金净流入\', \'1\',\'x\',\'y2\', \'净流入资金(万)\')">资金净流入</a> </li> ' +
        '<li> <a onclick=" show_chart(\'chart_div\', \'投资人数\',\'2\',\'x\', \'y1\', \'投资人数(人)\')">投资人数</a> </li> ' +
        '<li> <a onclick="show_chart(\'chart_div\', \'借款人数\', \'2\',\'x\',\'y2\', \'借款人数(人)\')">借款人数</a> </li> </ul> </div> ' +
        '<div id="chart_div" style="width:100%;margin: 0 auto;border:1px solid lightgrey;border-top: none"> </div>' +
        '<div id="yq_div"> ' +
        '<a class="list-group-item list-group-item-info"> ' +
        '<span class="glyphicon glyphicon-hand-right"></span>&nbsp&nbsp舆情关键词 </a> ' +
        '<div id="yq_keyword" style="width:100%;border:1px solid lightgrey;border-top: none;"> </div>' +
        '</div>' +
        '<a  id ="comment_div_title"class="list-group-item list-group-item-info">' +
        '<span class="glyphicon glyphicon-hand-right"></span>&nbsp&nbsp' + platform_name + '用户评价 </a>' +
        '<div id="comment_div" style="width:100%;margin: 0 auto;border:1px solid lightgrey;border-top: none;">' +
        '</div>')

    div_object = $("#chart_div");
    div_object.height(Math.round(div_object.width() * 0.6))

    div_object = $("#yq_keyword");
    div_object.height(Math.round(div_object.width() * 0.382))

    div_object = $("#comment_div");
    div_object.height(Math.round(div_object.width() * 0.6))

    // 显示
    $.getJSON("/detail/platform/" + platform_name + "/info", function (data) {

        // 初始化和配置图表数据
        init_and_show_chart(data);
        // 显示热点词云
        show_hot_word(data);

        var frequent_label = data['frequent_label']
        if (frequent_label.length > 0) {
            show_frequent_label(platform_name, frequent_label)
            // show_hot_word(frequent_label,'pl_keyword')
        } else {
            $('#comment_div_title').hide();
            $('#comment_div').hide();
        }

    });
}


// 显示热点词汇
function createRandomItemStyle() {
    var base = 240;
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

function show_hot_word(data) {

    if (data.keyword.length == 0) {
        $('#yq_div').hide();
        return;
    }

    var word_data = data.keyword;
    var div_id = 'yq_keyword';

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
    var cy_chart = echarts.init(document.getElementById(div_id));
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

// 初始化和配置图表数据
var data_chart_json;
function init_and_show_chart(data) {
    if (data['chart_json']['0'] == null) {
        $("#chart_div_title").hide();
        $("#chart_dropdown").hide();
        $("#chart_div").hide();
    } else {
        data_chart_json = data['chart_json'];
        show_chart('chart_div', '利率信息', '0', 'x', 'y1', '百分比(%)');
    }
}

// 动态显示图表
function show_chart(div_id, data_text, index, x_index, y_index, y_name) {

    $("#show_chart_title").text(data_text);

    data_x = data_chart_json[index][x_index];
    data_y = data_chart_json[index][y_index];

    var chart = echarts.init(document.getElementById(div_id));
    var option = {
        tooltip: {
            trigger: 'axis'
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: data_x
            }
        ],
        yAxis: [
            {
                name: y_name,
                type: 'value'
            }
        ],
        series: [
            {
                name: data_text,
                type: 'line',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                },
                areaStyle: {normal: {}},
                data: data_y
            }
        ]
    };

    chart.setOption(option);
}
function show_frequent_label(platform_name, frequent_label) {
    var comment_chart = echarts.init(document.getElementById('comment_div'));
    var comment_option = {
        tooltip: {
            trigger: 'item',
            formatter: "{b} : {d}%"
        },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: '60%',
                center: ['50%', '50%'],
                data: frequent_label,
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
    comment_chart.setOption(comment_option);
}
