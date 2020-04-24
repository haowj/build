from django.contrib import admin
from django.contrib.auth.models import Group
from strategy.models import *


@admin.register(O_E_M_DB)
class OemMd(admin.ModelAdmin):
    "厂商数据"
    module = O_E_M_DB
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
        return super(OemMd, self).changelist_view(request, extra_context=None)


@admin.register(D_M_DB)
class DeviceModel(admin.ModelAdmin):
    "设备型号"
    module = D_M_DB
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
        return super(DeviceModel, self).changelist_view(request, extra_context=None)


@admin.register(M_D_M_DB)
class ModelDeviceMd(admin.ModelAdmin):
    "设备型号构建映射表"
    module = M_D_M_DB
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
        return super(ModelDeviceMd, self).changelist_view(request, extra_context=None)



@admin.register(S_D_C_F_DB)
class SuperDataConf(admin.ModelAdmin):
    "SuperD 配置文件数据"
    module = S_D_C_F_DB
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
        return super(SuperDataConf, self).changelist_view(request, extra_context=None)


@admin.register(S_D_DB)
class SuperData(admin.ModelAdmin):
    "SuperD 插件版本数据"
    module = S_D_DB
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
        return super(SuperData, self).changelist_view(request, extra_context=None)


@admin.register(S_T_V_DB)
class SuperTask(admin.ModelAdmin):
    "连接器"
    module = S_T_V_DB
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
        return super(SuperTask, self).changelist_view(request, extra_context=None)


@admin.register(S_A_L_DB)
class SuperApiLoader(admin.ModelAdmin):
    "加载器"
    module = S_A_L_DB
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
        return super(SuperApiLoader, self).changelist_view(request, extra_context=None)


@admin.register(R_P_DB)
class Proxy(admin.ModelAdmin):
    "反向代理"
    module = R_P_DB
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
        return super(Proxy, self).changelist_view(request, extra_context=None)


@admin.register(B_T_L_DB)
class BuildToolsLog(admin.ModelAdmin):
    "构建日志"
    module = B_T_L_DB
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
        return super(BuildToolsLog, self).changelist_view(request, extra_context=None)


@admin.register(B_P_R_DB)
class BuildPackageResult(admin.ModelAdmin):
    "Build Package Result Data Base"
    module = B_P_R_DB
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
        return super(BuildPackageResult, self).changelist_view(request, extra_context=None)


@admin.register(S_A_L_P_DB)
class SuperApiLoaderPackage(admin.ModelAdmin):
    "super Api Loader Package Data Base"
    module = S_A_L_P_DB
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
        return super(SuperApiLoaderPackage, self).changelist_view(request, extra_context=None)


@admin.register(S_O_T_DB)
class SuperOperatingTag(admin.ModelAdmin):
    "SuperD Operating Tag Data Base"
    module = S_O_T_DB
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
        return super(SuperOperatingTag, self).changelist_view(request, extra_context=None)


@admin.register(R_O_P_L_DB)
class ReleaseOnlinePackageLog(admin.ModelAdmin):
    "Release Online Package Log Data Base"
    module = R_O_P_L_DB
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
        return super(ReleaseOnlinePackageLog, self).changelist_view(request, extra_context=None)


@admin.register(PackDefaultConfigure)
class PackDefaultConf(admin.ModelAdmin):
    "Release Online Package Log Data Base"
    module = PackDefaultConfigure
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
        return super(PackDefaultConf, self).changelist_view(request, extra_context=None)
