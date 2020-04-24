/*
 * A JavaScript implementation of the RSA Data Security, Inc. MD5 Message
 * Digest Algorithm, as defined in RFC 1321.
 * Copyright (C) Paul Johnston 1999 - 2000.
 * Updated by Greg Holt 2000 - 2001.
 * See http://pajhome.org.uk/site/legal.html for details.
 */

/*
 * Convert a 32-bit number to a hex string with ls-byte first
 */
var hex_chr = "0123456789abcdef";

function showHide(obj) {
    a = obj;
    console.log(a.css("display"));
    a.toggle(1000);
}

function rhex(num) {
    str = "";
    for (j = 0; j <= 3; j++)
        str += hex_chr.charAt((num >> (j * 8 + 4)) & 0x0F) +
            hex_chr.charAt((num >> (j * 8)) & 0x0F);
    return str;
}

/*
 * Convert a string to a sequence of 16-word blocks, stored as an array.
 * Append padding bits and the length, as described in the MD5 standard.
 */
function str2blks_MD5(str) {
    nblk = ((str.length + 8) >> 6) + 1;
    blks = new Array(nblk * 16);
    for (i = 0; i < nblk * 16; i++) blks[i] = 0;
    for (i = 0; i < str.length; i++)
        blks[i >> 2] |= str.charCodeAt(i) << ((i % 4) * 8);
    blks[i >> 2] |= 0x80 << ((i % 4) * 8);
    blks[nblk * 16 - 2] = str.length * 8;
    return blks;
}

function checkMacAddress(macAddress) {
    mac = macAddress.replace(/-/g, '').replace(/:/g, '').replace(/：/g, '');

    // macDom.val(mac);
    var regex = "[A-F\\d]{2}[A-F\\d]{2}[A-F\\d]{2}[A-F\\d]{2}[A-F\\d]{2}[A-F\\d]{2}";
    var regexp = new RegExp(regex);
    if (!regexp.test(mac)) {
        return false;
    }
    return true;
}

/*
 * Add integers, wrapping at 2^32. This uses 16-bit operations internally
 * to work around bugs in some JS interpreters.
 */
function add(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF);
}

/*
 * Bitwise rotate a 32-bit number to the left
 */
function rol(num, cnt) {
    return (num << cnt) | (num >>> (32 - cnt));
}

/*
 * These functions implement the basic operation for each round of the
 * algorithm.
 */
function cmn(q, a, b, x, s, t) {
    return add(rol(add(add(a, q), add(x, t)), s), b);
}

function ff(a, b, c, d, x, s, t) {
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
}

function gg(a, b, c, d, x, s, t) {
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
}

function hh(a, b, c, d, x, s, t) {
    return cmn(b ^ c ^ d, a, b, x, s, t);
}

function ii(a, b, c, d, x, s, t) {
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
}

/*
 * Take a string and return the hex representation of its MD5.
 */
function calcMD5(str) {
    x = str2blks_MD5(str);
    a = 1732584193;
    b = -271733879;
    c = -1732584194;
    d = 271733878;

    for (i = 0; i < x.length; i += 16) {
        olda = a;
        oldb = b;
        oldc = c;
        oldd = d;

        a = ff(a, b, c, d, x[i + 0], 7, -680876936);
        d = ff(d, a, b, c, x[i + 1], 12, -389564586);
        c = ff(c, d, a, b, x[i + 2], 17, 606105819);
        b = ff(b, c, d, a, x[i + 3], 22, -1044525330);
        a = ff(a, b, c, d, x[i + 4], 7, -176418897);
        d = ff(d, a, b, c, x[i + 5], 12, 1200080426);
        c = ff(c, d, a, b, x[i + 6], 17, -1473231341);
        b = ff(b, c, d, a, x[i + 7], 22, -45705983);
        a = ff(a, b, c, d, x[i + 8], 7, 1770035416);
        d = ff(d, a, b, c, x[i + 9], 12, -1958414417);
        c = ff(c, d, a, b, x[i + 10], 17, -42063);
        b = ff(b, c, d, a, x[i + 11], 22, -1990404162);
        a = ff(a, b, c, d, x[i + 12], 7, 1804603682);
        d = ff(d, a, b, c, x[i + 13], 12, -40341101);
        c = ff(c, d, a, b, x[i + 14], 17, -1502002290);
        b = ff(b, c, d, a, x[i + 15], 22, 1236535329);

        a = gg(a, b, c, d, x[i + 1], 5, -165796510);
        d = gg(d, a, b, c, x[i + 6], 9, -1069501632);
        c = gg(c, d, a, b, x[i + 11], 14, 643717713);
        b = gg(b, c, d, a, x[i + 0], 20, -373897302);
        a = gg(a, b, c, d, x[i + 5], 5, -701558691);
        d = gg(d, a, b, c, x[i + 10], 9, 38016083);
        c = gg(c, d, a, b, x[i + 15], 14, -660478335);
        b = gg(b, c, d, a, x[i + 4], 20, -405537848);
        a = gg(a, b, c, d, x[i + 9], 5, 568446438);
        d = gg(d, a, b, c, x[i + 14], 9, -1019803690);
        c = gg(c, d, a, b, x[i + 3], 14, -187363961);
        b = gg(b, c, d, a, x[i + 8], 20, 1163531501);
        a = gg(a, b, c, d, x[i + 13], 5, -1444681467);
        d = gg(d, a, b, c, x[i + 2], 9, -51403784);
        c = gg(c, d, a, b, x[i + 7], 14, 1735328473);
        b = gg(b, c, d, a, x[i + 12], 20, -1926607734);

        a = hh(a, b, c, d, x[i + 5], 4, -378558);
        d = hh(d, a, b, c, x[i + 8], 11, -2022574463);
        c = hh(c, d, a, b, x[i + 11], 16, 1839030562);
        b = hh(b, c, d, a, x[i + 14], 23, -35309556);
        a = hh(a, b, c, d, x[i + 1], 4, -1530992060);
        d = hh(d, a, b, c, x[i + 4], 11, 1272893353);
        c = hh(c, d, a, b, x[i + 7], 16, -155497632);
        b = hh(b, c, d, a, x[i + 10], 23, -1094730640);
        a = hh(a, b, c, d, x[i + 13], 4, 681279174);
        d = hh(d, a, b, c, x[i + 0], 11, -358537222);
        c = hh(c, d, a, b, x[i + 3], 16, -722521979);
        b = hh(b, c, d, a, x[i + 6], 23, 76029189);
        a = hh(a, b, c, d, x[i + 9], 4, -640364487);
        d = hh(d, a, b, c, x[i + 12], 11, -421815835);
        c = hh(c, d, a, b, x[i + 15], 16, 530742520);
        b = hh(b, c, d, a, x[i + 2], 23, -995338651);

        a = ii(a, b, c, d, x[i + 0], 6, -198630844);
        d = ii(d, a, b, c, x[i + 7], 10, 1126891415);
        c = ii(c, d, a, b, x[i + 14], 15, -1416354905);
        b = ii(b, c, d, a, x[i + 5], 21, -57434055);
        a = ii(a, b, c, d, x[i + 12], 6, 1700485571);
        d = ii(d, a, b, c, x[i + 3], 10, -1894986606);
        c = ii(c, d, a, b, x[i + 10], 15, -1051523);
        b = ii(b, c, d, a, x[i + 1], 21, -2054922799);
        a = ii(a, b, c, d, x[i + 8], 6, 1873313359);
        d = ii(d, a, b, c, x[i + 15], 10, -30611744);
        c = ii(c, d, a, b, x[i + 6], 15, -1560198380);
        b = ii(b, c, d, a, x[i + 13], 21, 1309151649);
        a = ii(a, b, c, d, x[i + 4], 6, -145523070);
        d = ii(d, a, b, c, x[i + 11], 10, -1120210379);
        c = ii(c, d, a, b, x[i + 2], 15, 718787259);
        b = ii(b, c, d, a, x[i + 9], 21, -343485551);

        a = add(a, olda);
        b = add(b, oldb);
        c = add(c, oldc);
        d = add(d, oldd);
    }
    return rhex(a) + rhex(b) + rhex(c) + rhex(d);
}


function getLocalTime(nS) {
    //时间戳转时间
    return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ');
}

function getTimeStamp() {
    // 毫秒级时间戳
    return timestamp = new Date().getTime();
}

function sign(timestamp) {
    key = "234$#SDLSKDJAHFJLJL%SDFJLLJ38581312LLSDFJKKJ";
    st = key.toString() + timestamp.toString();
    sign_data = calcMD5(st);
    return sign_data;
}


function getadvertising(type, location, eleId, father_id) {
    ts = getTimeStamp();
    data = {'type': type, 'location': location, 'ts': ts, 'sign': sign(ts)};
    $.get("/api/getadvertising/", data, function (res) {
        html = '';
        ele = $("#" + eleId);
        father = $("#" + father_id);
        ele.empty();
        rdata = res.data;
        $.each(rdata, function (index, item) {
            if (item.id) {
                father.show();
            }
            conntent = item.content.replace("\r\n", "<br/>");
            ele.append('<div id=' + item.id + '>' + conntent + '</div>');
        });
    });
}

function pop_up_windows(title, htm) {
    $(".win_head_title").val('').html(title);
    $(".win_detail").val('').html(htm);
    $('.win_backgroud').toggle()
}

function ReplaceSeperator(mobiles) {
    result = "";
    for (i = 0; i < mobiles.length; i++) {
        c = mobiles.substr(i, 1);
        if (c === "\n")
            result = result + "<br/>";
        else if (c != "\r")
            result = result + c;
    }
    return result;
}

function loading_show() {
    $(".loading_").show()
}

function loading_hide() {
    $(".loading_").hide()
}

function replce_hg(str) {
    console.log(str);

}

function toggle(ele) {
    $(ele).toggle()
}

function show(ele, time = 500) {
    $(ele).show(time)
}

function hide(ele, time = 500) {
    $(ele).hide(time)
}
function show_hide(show_ele,hide_ele) {
    show(show_ele);
    hide(hide_ele);

}
function setNull(ele = '.input') {
    var vdefault = $(ele).val();
    $(ele).focus(function () {
        //获得焦点时，如果值为默认值，则设置为空
        if ($(this).val() === vdefault) {
            $(this).val("");
        }
    });
    $(ele).blur(function () {
        //失去焦点时，如果值为空，则设置为默认值
        if ($(this).val() === "") {
            $(this).val(vdefault);

        }
    });
}

function show_message(ele = '.main-msg', comment = '查询中...', title = '提示：',sw=1, sty = 'col-md-12') {
       switch (sw){
        case 1:
            lclass ='box-success';
            break;
        default:
            lclass ='box-danger';
    }
     html = '<div class="row"><div class="'+ sty +'"><div class="box '+lclass+'">' +
         '<div class="box-header">' +
         '<h3 class="box-title">' + title + '</h3></div>' +
         '<div class="box-body">' + comment + '</div></div> </div></div></div>';
    $(ele).html('').html(html);
    show(ele);
    return html
}
function show_part_loading(ele = '.main-msg', comment = '查询中...', title = '提示：', sty = 'col-md-12') {

    html = "<div class=\"row\"><div class=\"" + sty + "\">" +
        "          <div class=\"box box-danger\">" +
        "            <div class=\"box-header\">" +
        "              <h3 class=\"box-title\">" + title + "</h3>" +
        "            </div>" +
        "            <div class=\"box-body\">" +
        "              " + comment + "" +
        "            </div>" +
        "            <!-- /.box-body -->" +
        "            <!-- Loading (remove the following to stop the loading)-->" +
        "            <div class=\"overlay\">" +
        "              <i class=\"fa fa-refresh fa-spin\"></i>" +
        "            </div>" +
        "            <!-- end loading -->" +
        "          </div>" +
        "          <!-- /.box -->" +
        "        </div>" +
        "        <!-- /.col -->" +
        "      </div></div>";
    $(ele).html('').html(html);
    show(ele);
    return html
}

function hide_part_loading(ele='.main-msg') {
    hide(ele)
}
function isArray(o) {
    return Object.prototype.toString.call(o) === '[object Array]';
}
function is_null(exp) {
    is_null_res = false;
    if (isArray(exp)) {
        if (exp.length === 0) {
            is_null_res = true;
        }
    } else {
        if (!exp || typeof(exp) === "undefined" || exp === 0) {
            is_null_res = true;
        }
    }
    return is_null_res
}
function part_alert(sw, msg, ele, time = 0) {
    isok_html = "<div class=\"alert alert-success alert-dismissible\">" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>" +
        "                <h4><i class=\"icon fa fa-check\"></i> 通过!</h4>" +
        "                " + msg + "" +
        "              </div>";
    isfail_html = "<div class=\"alert alert-danger alert-dismissible\">" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>" +
        "                <h4><i class=\"icon fa fa-ban\"></i> 失败!</h4>" +
        "                " + msg + "" +
        "              </div>";
    iswarning_html = "<div class=\"alert alert-warning alert-dismissible\">" +
        "                <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>" +
        "                <h4><i class=\"icon fa fa-warning\"></i> 提示!</h4>" +
        "                " + msg + "" +
        "              </div>";
    if (sw === 1) {
        html = isok_html
    } else if (sw === 2) {
        html = isfail_html
    } else if (sw === 3) {
        html = iswarning_html
    }
    $(ele).html('').html(html);
    show(ele);
    if (time !== 0) {
        hide_delay(ele, time)
    }
}

function hide_delay(ele, time) {
    setTimeout(function () {
        $(ele).hide(300);
    }, time);
}

function is_array(array) {
    if(Array.isArray(array)){
        return true;
    }else {
        return false;
    }
}
function is_null_array(arrary) {
    if (Array.isArray(arrary) && arrary.length === 0) {
        console.log('空数组');
        return true
    }
    return false
}

function getTablebox(table_box_title, array) {
    // 组装完弹出后，并渲染到页面上，然后显示这个弹窗
    table_box_heard_title = '';
    table_box_body = '';
    if (is_null_array(array)) {
        table_box_heard_title = '<li class="active" id="custom_tabs_title_0"><a href="#custom_tabs_body_0" data-toggle="tab">加载中</a></li>'
        table_box_body = '<div class="tab-pane active" id="custom_tabs_body_0"><div class="chart" id="custom_tabs_body_chart_0"></div></div>';
    } else {

        $.each(array, function (k, v) {
            // 每个li标签的id
            li_id = 'custom_tabs_title_' + k;
            // 每个li标签上跟body中每个体对应的id
            li_href = '#custom_tabs_body_' + k;
            // 每个bady体的id
            d_body_title_id = 'custom_tabs_body_' + k;
            // 每个li标签的标题名称
            li_text = v;

            d_body_id = 'custom_tabs_body_chart_' + k;
            if(k===0){
                line_html = '<li class="active" id="' + li_id + '"><a href="' + li_href + '" data-toggle="tab">' + li_text + '</a></li>';
                b_line_html = '<div class="tab-pane active" id="' + d_body_title_id + '"><div class="chart" id="' + d_body_id + '"></div></div>';

            }else {
                line_html = '<li id="' + li_id + '"><a href="' + li_href + '" data-toggle="tab">' + li_text + '</a></li>';
                b_line_html = '<div class="tab-pane" id="' + d_body_title_id + '"><div class="chart" id="' + d_body_id + '"></div></div>';
            }

            table_box_heard_title = table_box_heard_title + line_html;
            table_box_body = table_box_body + b_line_html;

        });
    }
    table_box = '<div class="col-md-12">\n' +
        '             <div class="box box-info">\n' +
        '                <div class="box-header with-border">\n' +
        '                    <h3 class="box-title table-box-title">' + table_box_title + '</h3>\n' +
        '                    <div class="box-tools pull-right">\n' +
        '                        <button type="button" class="btn btn-box-tool" data-widget="collapse"><i\n' +
        '                                class="fa fa-minus"></i>\n' +
        '                        </button>\n' +
        '                        <button type="button" class="btn btn-box-tool" onclick="hide(\'#row-main\')"><i class="fa fa-times"></i>\n' +
        '                        </button>\n' +
        '                    </div>\n' +
        '                </div>\n' +
        '                <div class="box-body chart-responsive">\n' +
        '            <!-- Custom Tabs -->\n' +
        '            <div class="nav-tabs-custom">\n' +
        '                <ul class="nav nav-tabs custom-tabs-title">' + table_box_heard_title +
        '                </ul>\n' +
        '                <div class="tab-content custom-tabs-body">\n' +
        table_box_body +
        '                    <!-- /.tab-pane -->\n' +
        '                </div>\n' +
        '                <!-- /.tab-content -->\n' +
        '            </div>\n' +
        '            <!-- nav-tabs-custom -->\n' +
        '        </div>\n' +
        '        </div>\n' +
        '        </div>';
    $('#row-main').html(table_box);
    show('#row-main');
    show_part_loading('#custom_tabs_body_chart_0', '加载中');
}
function openUrl(url) {
            window.open(url);
}

function alert_makesure(title,body) {
    // 确认弹窗
    html = '                <div class="modal fade" id="modal-default">\n' +
        '                    <div class="modal-dialog">\n' +
        '                        <div class="modal-content">\n' +
        '                            <div class="modal-header">\n' +
        '                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n' +
        '                                    <span aria-hidden="true">&times;</span></button>\n' +
        '                                <h4 class="modal-title">'+title+'</h4>\n' +
        '                            </div>\n' +
        '                            <div class="modal-body">\n' +
        '                                <p>'+body+'</p>\n' +
        '                            </div>\n' +
        '                            <div class="modal-footer">\n' +
        '                                <button type="button" class="btn btn-default pull-left" data-dismiss="modal">取消\n' +
        '                                </button>\n' +
        '                                <button type="button" class="btn btn-primary">确认</button>\n' +
        '                            </div>\n' +
        '                        </div>\n' +
        '                        <!-- /.modal-content -->\n' +
        '                    </div>\n' +
        '                    <!-- /.modal-dialog -->\n' +
        '                </div>\n';
    $('#row-main').html('').html(html);
    return html
}

function checkmpauth(code) {
    // {#"检查小程序登录是否异常"#}
    if (code === 401) {
        $(location).attr('href', 'http://support.superhcloud.com/dsm/mplogin');
    } else {
        return true;
    }

}
function add_box(ele,title,body,footer) {

    html = "<div class=\"box\">\n" +
        "        <div class=\"box-header with-border\">\n" +
        "          <h3 class=\"box-title\">"+title+"</h3>\n" +
        "\n" +
        "          <div class=\"box-tools pull-right\">\n" +
        "            <button type=\"button\" class=\"btn btn-box-tool\" data-widget=\"collapse\" data-toggle=\"tooltip\" title=\"Collapse\">\n" +
        "              <i class=\"fa fa-minus\"></i></button>\n" +
        "            <button type=\"button\" class=\"btn btn-box-tool\" data-widget=\"remove\" data-toggle=\"tooltip\" title=\"Remove\">\n" +
        "              <i class=\"fa fa-times\"></i></button>\n" +
        "          </div>\n" +
        "        </div>\n" +
        "        <div class=\"box-body\">\n" +body+
        "        </div>\n";
    if(footer){
        foot = "<div class=\"box-footer\">\n" +footer+"</div>\n";
    }else {
        foot =''
    }
    rhtml = html+foot+"</div>";
    $(ele).empty().html(rhtml);
    return rhtml
}

function show_global_box(title,htm) {
    $(".win_head_title").val('').html(title);
    $(".win_detail").val('').html(htm);
    $('.win_backgroud').show();
}
function hide_global_box() {
    hide('.win_backgroud')
}

 //生成从minNum到maxNum的随机数
function randomNum(minNum, maxNum) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * minNum + 1, 10);
        case 2:
            return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
        default:
            return 0;
    }
}

function show_fuceng(sw, title, body, width = '', foot_left, foot_right, attr) {

    if (sw === 1) {
        $('.identifier_save').modal('show');
        $(".identifier_save_title").html('').html(title);
        $(".identifier_save_body").html('').html(body);
        $("#fuceng_footer_left").html('').html(foot_left);
        ffr = $("#fuceng_footer_right");
        ffr.html('').html(foot_right);
        ffr.attr('id', attr);

    } else {
        $('.identifier_no_footer').modal('show');
        $(".identifier_no_footer_title").html('').html(title);
        $(".identifier_no_footer_body").html('').html(body);
    }
    if (width) {
        $('.modal-dialog').css('width', width)
    }
}
function hide_fuceng() {
    $('.identifier_save').modal('hide');
}
function getfcWidth(width='80%') {
    scrollWidth = document.body.scrollWidth;
    if (scrollWidth > 1000) {
        fc_width = width
    } else {
        fc_width = ''
    }
    return fc_width
}

function getCheckBoxVal(){ //jquery获取所有选中的复选框的值 
    chk_value =[]; 
    $(".input_checkbox:checked").each(function(){ //遍历，将所有选中的值放到数组中
        chk_value.push($(this).val()); 
    }); 
    v = chk_value.join();
    return v;
} 

function png_result_ok_do() {
    $('.png_result_ok').append('<img src="/static/images/run_ok.png" width="20" height="20"/>');
}
function png_result_err_do() {
    $('.png_result_err').append('<img src="/static/images/run_err.png" width="20" height="20"/>');

}
function addClass(ele,className) {
    $(ele).addClass(className)
}

function html_encode(str)
    {
        var s = "";
        if (str.length === 0) return "";
        s = str.replace(/&/g, "&amp;");
        s = s.replace(/</g, "&lt;");
        s = s.replace(/>/g, "&gt;");
        s = s.replace(/ /g, "&nbsp;");
        s = s.replace(/\'/g, "&#39;");
        s = s.replace(/\"/g, "&quot;");
        s = s.replace(/\n/g, "<br/>");
        return s;
    }

function html_decode(str)
{
    var s = "";
    if (str.length === 0) return "";
    s = str.replace(/&amp;/g, "&");
    s = s.replace(/&lt;/g, "<");
    s = s.replace(/&gt;/g, ">");
    s = s.replace(/&nbsp;/g, " ");
    s = s.replace(/&#39;/g, "\'");
    s = s.replace(/&quot;/g, "\"");
    s = s.replace(/<br\/>/g, "\n");
    return s;
}