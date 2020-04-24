from django.contrib import admin
from appack.models import *
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(oem_db)
class oem_dbAdmin(admin.ModelAdmin):
    "设备型号"
    module = oem_db
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(oem_dbAdmin, self).changelist_view(request, extra_context=None)

@admin.register(dev_model_db)
class dev_modelAdmin(admin.ModelAdmin):
    "设备型号"
    module = dev_model_db
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(dev_modelAdmin, self).changelist_view(request, extra_context=None)
@admin.register(map_dev_model_db)
class map_dev_model_dbAdmin(admin.ModelAdmin):
    "设备型号"
    module = map_dev_model_db
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = ('type','dev_model')  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(map_dev_model_dbAdmin, self).changelist_view(request, extra_context=None)


@admin.register(superdVersion)
class superdVersionAdmin(admin.ModelAdmin):
    "设备型号"
    module = superdVersion
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(superdVersionAdmin, self).changelist_view(request, extra_context=None)

@admin.register(build_log)
class build_logAdmin(admin.ModelAdmin):
    "构建-日志"
    module = build_log
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(build_logAdmin, self).changelist_view(request, extra_context=None)

@admin.register(release_plug_log)
class release_plug_logAdmin(admin.ModelAdmin):
    "上线插件日志"
    module = release_plug_log
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(release_plug_logAdmin, self).changelist_view(request, extra_context=None)

@admin.register(sapiloaderVersion)
class sapiloaderVersionAdmin(admin.ModelAdmin):
    "加载器版本"
    module = sapiloaderVersion
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(sapiloaderVersionAdmin, self).changelist_view(request, extra_context=None)

@admin.register(superdcfVersion)
class superdcfVersionAdmin(admin.ModelAdmin):
    "superd配置文件版本"
    module = superdcfVersion
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(superdcfVersionAdmin, self).changelist_view(request, extra_context=None)

@admin.register(superctlVersion)
class superctlVersionAdmin(admin.ModelAdmin):
    "superctl版本"
    module = superctlVersion
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(superctlVersionAdmin, self).changelist_view(request, extra_context=None)

@admin.register(supertackVersion)
class supertackVersionAdmin(admin.ModelAdmin):
    "supertack版本"
    module = supertackVersion
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(supertackVersionAdmin, self).changelist_view(request, extra_context=None)

@admin.register(version_contorl)
class version_contorlAdmin(admin.ModelAdmin):
    "版本控制表"
    module = version_contorl
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(version_contorlAdmin, self).changelist_view(request, extra_context=None)

@admin.register(pack_list_contorl)
class pack_list_contorlAdmin(admin.ModelAdmin):
    "构建结果表"
    module = pack_list_contorl
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)
    def changelist_view(self, request, extra_context=None):
        current_user_set = request.user
        if not current_user_set.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
            if current_group_set.name != '内容-管理员' and current_group_set.name != '超级管理员':
                self.readonly_fields = self.list_display
        return super(pack_list_contorlAdmin, self).changelist_view(request, extra_context=None)

@admin.register(unpack_cmd)
class unpack_cmdAdmin(admin.ModelAdmin):
    "构建结果表"
    module = unpack_cmd
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)

@admin.register(sapiloader_pack)
class sapiloader_packAdmin(admin.ModelAdmin):
    "构建结果表"
    module = sapiloader_pack
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段
    ordering = ('-update_time',)


