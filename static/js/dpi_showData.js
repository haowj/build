url = '/dpi/api_getAllEC';
show_part_loading();
$.get(url, function (dict) {
    data = dict.data;
    hide_part_loading(main_msg);
    table_data = [];
    if (data) {
        $.each(data, function (index, i) {
            a = ['<span class="ec_id_' + i.id + '">' + i.id + '</span>', '<span class="ec_name_' + i.id + '">' + i.name + '</span>', '<span class="ec_en_' + i.id + '">' + i.en + '</span>', '<span class="ec_code_' + i.id + '">' + i.code + '</span>', '<span class="ec_typeCode_id' + i.id + '">' + i.businessType + '</span>', '<a id="' + i.id + '" onclick="updateEC(this)" class="pointer">修改</a>'];
            table_data.push(a);
        });
    } else {
        part_alert(3, '版本概览数据为空')
    }
    $('#table_ide').DataTable({
        "destroy": true,
        // {#scrollY: 300,#}
        // {#scrollX: true,#}
        scrollCollapse: true,
        bPaginate: true,
        bLengthChange: true,
        "bAutoWidth": true,
        "aaSorting": [],
        "order": [[0, "desc"]],
        data: table_data,
        columns: [
            {title: "ID"},
            {title: "企业名称"},
            {title: "EN"},
            {title: "CODE"},
            {title: "业务类型"},
            {title: "操作"},
        ]
    });
});