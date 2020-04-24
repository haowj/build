function onlyShowHide(sw, is_show) {
    class_list = ['.main_btn', '.createDpiConf', '.createDpiPcap', '.searchDpiConf'];
    for (i = 0; i < class_list.length; i++) {
        if (is_show === true) {
            if (sw === class_list[i]) {
                show(sw)
            } else {
                hide(class_list[i])
            }
        } else {
            if (sw === class_list[i]) {
                hide(sw)
            } else {
                show(class_list[i])
            }
        }

    }
}

function createDPIPcap() {
    pacp_vi_type_id = $("#pacp_vi_type_id").val();
    taget_account = $("#taget_account").val();
    selectmi = $("#selectmi").val();
    app_version = $("#app_version").val();
    selectAppType = $("#selectAppType").val();
    file = $(".file")[0].files[0];
    pcap_comment = $("#pcap_comment").val();

    if (is_null(pacp_vi_type_id) || pacp_vi_type_id.length !== 7) {
        part_alert(3, '请输入虚拟身份ID', main_msg);
        return;
    }
    if (is_null(taget_account)) {
        part_alert(3, '请输入检索账号', main_msg);
        return;
    }
    if (is_null(selectmi)) {
        part_alert(3, '请输入手机具体型号', main_msg);
        return;
    }
    if (is_null(selectAppType)) {
        part_alert(3, '请选择应用类型', main_msg);
        return;
    }
    if (is_null(app_version)) {
        part_alert(3, '请输入app/web版本', main_msg);
        return;
    }

    if (is_null(file)) {
        part_alert(3, '请选择文件', main_msg);
        return;
    }

    form_data = new FormData();
    form_data.append('file', file);
    form_data.append('pacp_vi_type_id', pacp_vi_type_id);
    form_data.append('app_type', selectAppType);
    form_data.append('taget_account', taget_account);
    form_data.append('mobileinfo_id', selectmi);
    form_data.append('app_version', app_version);
    form_data.append('pcap_comment', pcap_comment);
    show_part_loading();
    $.ajax({
        url: "/dpi/api_createDpiPcap/",
        type: 'post',
        cache: false,
        fileElementId: "file",
        data: form_data,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        dataType: "json",
        success: function (data) {    //后端返回数据，是列表形式的
            if (data.code === 200) {
                part_alert(1, '提交成功', main_msg, 5000);
                location.reload();
            }
            else {
                html = "删除失败,原因:" + data.msg;
                part_alert(3, html, main_msg, 5000);
            }
        }
    });
}

function createDPIConf() {
    rule_name = $("#rule_name").val();
    vi_type_id = $("#vi_type_id").val();
    multimode_id = $("#selectm").val();
    rule_data = $("#rule_data").val();
    rule_begin_match = $("#rule_begin_match").val();
    rule_end_match = $("#rule_end_match").val();
    dpipcap_id = $("#selectp").val();
    comment = $("#comment").val();
    if (is_null(rule_name)) {
        part_alert(3, '请输入规则名称', main_msg);
        return;
    }
    if (is_null(vi_type_id)) {
        part_alert(3, '请输入虚拟身份ID', main_msg);
        return;
    }
    if (is_null(multimode_id)) {
        part_alert(3, '请输入多模ID', main_msg);
        return;
    }
    if (is_null(rule_data)) {
        part_alert(3, '请输入规则', main_msg);
        return;
    }
    if (is_null(rule_begin_match)) {
        part_alert(3, '请输入规则匹配头', main_msg);
        return;
    }
    if (is_null(rule_end_match)) {
        part_alert(3, '请输入规则匹配尾', main_msg);
        return;
    }
    if (is_null(dpipcap_id)) {
        part_alert(3, '请选择命中的pcapID', main_msg);
        return;
    }
    if (comment.indexOf("]") !== -1) {
        comment = '';
    }
    show_part_loading();
    $.ajax({
        type: 'get',
        url: '/dpi/api_createDPIConf',
        data: {
            'rule_name': rule_name,
            'vi_type_id': vi_type_id,
            'multimode_id': multimode_id,
            'rule_data': rule_data,
            'rule_begin_match': rule_begin_match,
            'rule_end_match': rule_end_match,
            'dpipcap_id': dpipcap_id,
            'comment': comment,
        },
        contentType: 'application/json',
        success: function (data) {    //后端返回数据，是列表形式的
            if (data.code === 200) {
                part_alert(1, data.data, main_msg, 5000);
                location.reload();
            }
            else {
                html = "删除失败,原因:" + data.msg;
                part_alert(3, html, main_msg, 5000);
            }
        }
    });
}

function load_dpi_conf() {
    url = '/dpi/api_getDpiConfAll';
    show_part_loading('.con_msg');
    $.get(url, function (dict) {
        data = dict.data;
        table_data = [];
        if (data) {
            $.each(data, function (index, i) {
                op_html = '<div class="btn btn-sm btn-primary btn-xs" onclick="getRuleInfo(this)" id="' + i.id + '">修改</div><div class="btn btn-sm btn-primary btn-xs" style="margin-left: 1%;" onclick="delRule(this)" id="' + i.id + '">删除</div>';
                a = [i.id, i.weight,'<a class="pointer" onclick="getPcap(this)" id="' + i.dpipcap_id + '">' + i.dpipcap_id + '</a>', i.rule_name, i.vi_type_id, i.type_value + '[' + i.type_id + ']', html_encode(i.rule_data), '【' + html_encode(i.rule_begin_match) + '】【' + html_encode(i.rule_end_match) + '】', i.comment, getLocalTime(i.update_time), i.user, op_html];
                table_data.push(a);
            });
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
        $('#table_ide').DataTable({
            "destroy": true,
            // {#scrollY: 300,#}
            scrollX: true,
            scrollCollapse: true,
            bPaginate: true,
            bLengthChange: true,
            "bAutoWidth": true,
            "aaSorting": [],
            "order": [[0, "desc"]],
            data: table_data,
            columns: [
                {title: "规则ID"},
                {title: "权重ID"},
                {title: "命中ID"},
                {title: "规则名称"},
                {title: "身份ID"},
                {title: "多模类型[code]"},
                {title: "规则内容"},
                {title: "匹配头-尾"},
                {title: "备注"},
                {title: "更新日期 "},
                {title: "操作人 "},
                {title: "操作 "},
            ],
            "initComplete": function (settings, json) {
                hide_part_loading('.con_msg');

            }
        });
    });
}

function load_dpi_m() {
    url = '/dpi/api_getDpiMultimodeAll';
    $.get(url, function (dict) {
        data = dict.data;
        table_data = [];
        m_data = [{'id': '', 'text': '请选择多模类型'}];
        if (data) {
            $.each(data, function (index, i) {
                b = {'id': i.id, 'text': '多模code:' + i.type_id + ' 多模类型:' + i.type_value};
                m_data.push(b);
            });
            selectm.html('');
            selectm.select2({
                data: m_data
            });
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
    });
}

function load_dpi_NSP() {
    url = '/dpi/api_getNSPAll';
    $.get(url, function (dict) {
        data = dict.data;
        m_data = [{'id': '', 'text': '请选择网安平台'}, {'id': '0', 'text': '智云平台'}];
        if (data) {
            $.each(data, function (index, i) {
                b = {'id': i.id, 'text': i.wname};
                m_data.push(b);
            });
            selectsvi.html('');
            selectsvi.select2({
                data: m_data
            });
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
        // {#hide_part_loading(main_msg);#}
    });
}

function delRule(obj) {
    if (!confirm('确认要删除吗？')) {
        return;
    }
    id = obj.id;
    url = '/dpi/api_delDpiConf?status=0&id=' + id;
    show_part_loading();
    $.get(url, function (dict) {
        data = dict.data;
        if (data) {
            part_alert(1, '删除成功', main_msg)
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
    });
}

function getRuleInfo(obj) {
    onlyShowHide('.createDpiConf', true);
    id = obj.id;
    url = '/dpi/api_getDpiConf?id=' + id;
    show_part_loading();
    $.get(url, function (dict) {
        data = dict.data;
        if (data) {
            i = data[0];
            rule_name = $("#rule_name").val('').val(i.rule_name);
            vi_type_id = $("#vi_type_id").val('').val(i.vi_type_id);
            multimode_id = $("#selectm").val(i.multimode_id).select2();
            rule_data = $("#rule_data").val('').val(i.rule_data);
            rule_begin_match = $("#rule_begin_match").val('').val(i.rule_begin_match);
            rule_end_match = $("#rule_end_match").val('').val(i.rule_end_match);
            dpipcap_id = $("#selectp").val(i.dpipcap_id).select2();
            comment = $("#comment").val('').val(i.comment);
            hide_part_loading();
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
    });
}

function getPcap(obj) {
    if (obj.id === '0') {
        part_alert(3, '命中ID为空', main_msg);
        return;
    }
    url = '/dpi/api_getDpiPcapAll?id=' + obj.id;
    show_part_loading();
    $.get(url, function (dict) {
        data = dict.data;
        hide_part_loading();
        if (data) {
            i = data[0];
            table_html = '<table class="table table-bordered"><tr><th>类别</th><th>数据</th>';
            mzinfo = table_html + '<tr><td>序号</td><td>' + i.id + '</td></tr><tr><td>检索账号</td><td>' + i.taget_account + '</td></tr><tr><td>应用类型</td><td>' + i.app_type + '</td></tr><tr><td>应用版本</td><td>' + i.app_version + '</td></tr><tr><td>手机型号</td><td>' + i.oem+'-'+i.oem_os_name+'-' +i.oem_os_version+ '</td></tr><tr><td>手机操作系统版本</td><td>' + i.os_name+'-'+i.os_version + '</td></tr><tr><td>虚拟身份ID</td><td>' + i.vi_type_id + '</td></tr><tr><td>备注</td><td>' + i.comment + '</td></tr><tr><td>操作人</td><td>' + i.user + '</td><td></tr></table>';
            show_fuceng(2, '命中文件详情:', mzinfo, getfcWidth())
        }
    })
}

function load_dpi_p() {
    selectp = $("#selectp");
    url = '/dpi/api_getDpiPcapAll';
    // {#show_part_loading('.pcapcon_msg');#}
    $.get(url, function (dict) {
        data = dict.data;
        table_data = [];
        p_data = [{'id': '', 'text': '请选择该规则命中的pcap文件'}];
        if (data) {
            $.each(data, function (index, i) {
                a = [i.id, i.vi_type_id, i.taget_account, i.app_type, i.app_version, i.oem, i.os_name + '[' + i.os_version + ']', i.oem_os_name + '[' + i.oem_os_version + ']', i.comment, i.user, getLocalTime(i.update_time)];
                table_data.push(a);
                pdata.push({'vi_type_id':i.vi_type_id,'id':i.id})
            });
            for (m = data.length; m > 0; m--) {
                i = data[m - 1];
                b = {
                    'id': i.id,
                    'text': '序号:' + i.id + ';检索账号:' + i.taget_account + ';手机型号:' + i.oem_os_name + ';备注:' + i.comment + ';操作人:' + i.user
                };
                p_data.push(b);
            }
            selectp.html('');
            selectp.select2({
                data: p_data
            });
        } else {
            part_alert(3, '配置信息为空', main_msg)
        }
        $('#table_ide_p').DataTable({
            "destroy": true,
            // {#scrollY: 300,#}
            scrollX: true,
            scrollCollapse: true,
            bPaginate: true,
            bLengthChange: true,
            "bAutoWidth": true,
            "aaSorting": [],
            "order": [[0, "desc"]],
            data: table_data,
            columns: [
                {title: "ID"},
                {title: "虚拟身份ID"},
                {title: "检索账号"},
                {title: "应用类型"},
                {title: "应用版本"},
                {title: "手机厂商"},
                {title: "手机系统[版本]"},
                {title: "手机型号名称[版本]"},
                {title: "备注"},
                {title: "操作人"},
                {title: "更新日期 "},
            ]
        });
    });
}

function searchDpiConf() {
    table_vip = $('#table_vip');
    show(".table_vip_class");
    nsp_id = selectsvi.val();
    if (is_null(nsp_id)) {
        part_alert(3, '请选择网安平台', main_msg);
        return;
    }
    show_part_loading();
    url = '/dpi/api_getPlatformViType?id=' + nsp_id;
    $.get(url, function (dict) {
        data = dict.data;
        if (nsp_id === '0') {
            table_data = [];
            if (data) {
                $.each(data.rdata, function (index, i) {
                    c = [i.vi_type_id, i.bdata.businessType, i.edata.name, i.idata.identityType,'不涉及'];
                    table_data.push(c);
                });
            } else {
                part_alert(3, '配置信息为空', main_msg)
            }
            table_vip.html('');
            table_vip.DataTable({
                "destroy": true,
                scrollY: 300,
                // scrollX: true,
                scrollCollapse: true,
                bPaginate: true,
                bLengthChange: true,
                "aaSorting": [],
                "order": [[0, "desc"]],
                data: table_data,
                columns: [
                    {title: "身份ID"},
                    {title: "业务类型"},
                    {title: "应用名称"},
                    {title: "身份类型"},
                    {title: "网安平台编码"},
                ],
                "initComplete": function (settings, json) {
                    hide_part_loading();
                }
            });
        } else {
            if (data) {
                table_data = [];
                $.each(data.rdata, function (index, i) {
                    $.each(i.adata, function (index, j) {
                        a = [i.vi_type_id, i.bdata.businessType, i.edata.name, i.idata.identityType,j.ns_code];
                        table_data.push(a);
                    });
                });
                inList = data.allmap;

                $(".sviInfo").html('<span onclick="showVIInfo()"><a>支持虚拟身份总数:'+inList.length+'</a></span>')
            } else {
                part_alert(3, '配置信息为空', main_msg)
            }
            table_vip.DataTable({
                "destroy": true,
                scrollY: 300,
                // scrollX: true,
                scrollCollapse: true,
                bPaginate: true,
                bLengthChange: true,
                "bAutoWidth": true,
                "aaSorting": [],
                "order": [[0, "desc"]],
                data: table_data,
                columns: [
                    {title: "身份ID"},
                    {title: "业务类型"},
                    {title: "应用名称"},
                    {title: "身份类型"},
                    {title: "网安平台编码"},
                ],
                "initComplete": function (settings, json) {
                    hide_part_loading();
                }
            });
        }

    });
}
function showVIInfo() {
    table_html = '<table class="table table-bordered"><tr><th>智云虚拟身份ID</th><th>网安平台虚拟身份ID</th>';
    line_table_html = '';
    $.each(inList, function (index, i) {
        $.each(i.vi_type_id_ns_code_list, function (index, j) {
            line_table_html = line_table_html+'<tr><td>' + i.vi_type_id +'</td><td>'+ j+'</td></tr>';
        });
    });
    show_fuceng(2, '支持虚拟身份详情', table_html+line_table_html+'</table>', getfcWidth())
}
function onSelect() {
    selectp = $("#selectp");
    selectp.on("select2:select", function (e) {
        id = selectp.val();
        $.each(pdata, function (index, i) {
              if (i.id === id){
                $('#vi_type_id').val('').val(i.vi_type_id)
              }
        })

    });
}