from django.contrib import admin
from dpi.models import *


@admin.register(BusinessType)
class BusinessTypeAdmin(admin.ModelAdmin):
    module = BusinessType
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    # 筛选器
    list_filter = ('businessType',)  # 过滤器
    search_fields = list_display  # 搜索字段

@admin.register(IdentityTypeCoding)
class IdentityTypeCodingAdmin(admin.ModelAdmin):
    module = IdentityTypeCoding
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    list_filter = list_display  # 过滤器
    search_fields = list_display  # 搜索字段

@admin.register(EnterpriseCoding)
class EnterpriseCodingAdmin(admin.ModelAdmin):
    module = EnterpriseCoding
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    list_filter = ('typeCode_id',)  # 过滤器
    search_fields = ('name', 'code', 'en')  # 搜索字段

@admin.register(NetSafetyPlatform)
class NetSafetyPlatformAdmin(admin.ModelAdmin):
    module = NetSafetyPlatform
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)

@admin.register(Multimode)
class MultimodeAdmin(admin.ModelAdmin):
    module = Multimode
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)

@admin.register(DpiConf)
class DpiConfAdmin(admin.ModelAdmin):
    module = DpiConf
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
@admin.register(DpiConfLog)
class DpiConfLogAdmin(admin.ModelAdmin):
    module = DpiConfLog
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)

@admin.register(AppProCode)
class AppProCodeAdmin(admin.ModelAdmin):
    module = AppProCode
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
    list_filter = ('platformCode',)  # 过滤器
    search_fields = ('ns_appname', 'ns_code', )  # 搜索字段


@admin.register(DpiPcap)
class DpiPcapAdmin(admin.ModelAdmin):
    module = DpiPcap
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)

@admin.register(MobileInfo)
class MobileInfoAdmin(admin.ModelAdmin):
    module = MobileInfo
    list_per_page = 50
    model_column_list = []
    params = [f for f in module._meta.fields]
    for msg in params:
        model_column_list.append(msg.name)
    list_display = tuple(model_column_list)
